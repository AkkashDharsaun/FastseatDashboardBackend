from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_admin import db

auth_bp = Blueprint("auth", __name__)

# Check if email exists
def is_email_exists(email):
    ref = db.reference("colleges")
    all_colleges = ref.get() or {}
    for key, val in all_colleges.items():
        if val.get("email") == email:
            return True
    return False

# Register college using institute_code as key
def register_college(institute_code, name, email, hashed_password, place, phone, website, totalDepartments, totalStaffs):
    ref = db.reference("colleges")
    
    # Check duplicate
    if ref.child(institute_code).get():
        return None, "Institute already registered!"

    ref.child(institute_code).set({
        "institute_code": institute_code,
        "name": name,
        "email": email,
        "password": hashed_password,
        "place": place,
        "contactNo": phone,
        "website": website,
        "totalDepartments": totalDepartments,
        "totalStaffs": totalStaffs,
        
    })
    return institute_code, "Registration successful!"

# -------------------- Routes --------------------

@auth_bp.route("/do_register", methods=["POST"])
def do_register():
    data = request.get_json(force=True)
    institute_code = data.get("institute_code")
    password = data.get("password")
    name = data.get("name")
    email = data.get("email")
    place = data.get("place")
    contactNo = data.get("phone")
    website = data.get("website")
    totalDepartments = data.get("total_departments")
    totalStaffs = data.get("total_staffs")
    if not all([institute_code, password, name, email, place]):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    if is_email_exists(email):
        return jsonify({"success": False, "message": "Email already registered"}), 409

    hashed_password = generate_password_hash(password)

    try:
        new_id, msg = register_college(
            institute_code, name, email, hashed_password, place, contactNo, website, totalDepartments, totalStaffs
        )
        if not new_id:
            return jsonify({"success": False, "message": msg}), 409

        session["institute_code"] = institute_code
        return jsonify({"success": True, "message": msg, "institute_code": institute_code}), 201
    except Exception as e:
        print("Register Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500


@auth_bp.route("/do_login", methods=["POST"])
def do_login():
    data = request.get_json(force=True)
    institute_code = data.get("institute_code")
    password = data.get("password")

    if not institute_code or not password:
        return {"success": False, "message": "Institute code & password are required."}, 400

    ref = db.reference("colleges")
    college_data = ref.child(institute_code).get()

    if college_data:
        if check_password_hash(college_data["password"], password):
            # Store institute_code in session
            session["institute_code"] = institute_code

            data_to_send = {
                "institute_code": college_data["institute_code"],
                "imageUrl": college_data.get("imageUrl"),
                "name": college_data["name"],
                "email": college_data["email"],
                "contactNo": college_data["contactNo"],
                "place": college_data["place"],
                "website": college_data["website"],
                "totalDepartments": college_data.get("totalDepartments"),
                "totalStaffs": college_data.get("totalStaffs"),
                "address": college_data.get("address"),
                "established": college_data.get("established"),
                "affiliatedTo": college_data.get("affiliatedTo"),
                "totalStudents": college_data.get("totalStudents"),
                "description": college_data.get("description"),

            }
            return {"success": True, "message": "Login successful", "dbdata": data_to_send}, 200
        else:
            return {"success": False, "message": "Invalid password"}, 401
    else:
        return {"success": False, "message": "Institute not found. Please register first."}, 404
