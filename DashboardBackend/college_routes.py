from flask import Blueprint, request, jsonify
from firebase_setup import db

college_bp = Blueprint("college", __name__)

@college_bp.route("/CollegeInformation", methods=["POST"])
def college_info():
    try:
        data = request.get_json(force=True)
        institute_code = data.get("institute_code")

        if not institute_code:
            return jsonify({"error": "Institute code required"}), 400

        ref = db.reference(f"colleges/{institute_code}")

        # Fetch existing data only
        if data.get("fetchOnly"):
            existing_data = ref.get() or {}
            return jsonify({"success": True, "collegeData": existing_data})

        # Update college information
        ref.update(data)
        return jsonify({"success": True, "collegeData": data})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
