from flask import Blueprint, render_template, request, session, flash, jsonify, redirect, url_for
from db import get_department_connection,get_department_connection


department_bp = Blueprint("department", __name__)

def fetch_departments(institute_code):
   conn = get_department_connection()
   cursor = conn.cursor(dictionary=True)
   query = """
       SELECT id, department_name, total_seats, available_seats
       FROM departments
       WHERE institute_code = %s
   """
   cursor.execute(query, (institute_code,))
   departments = cursor.fetchall()
   conn.close()
   return departments

@department_bp.route("/seat-update", methods=["GET"])
def seat_update():
    institute_code = session.get("institute_code")
    departments = fetch_departments(institute_code)
    return render_template("seat_update.html", departments=departments)

@department_bp.route("/add-department", methods=["POST", "GET"])
def add_department():
    institute_code = session.get("institute_code") # logged-in institute
    names = request.form.getlist("department_name") # multiple names from form
    total_seats = request.form.get("total_seats")
    available_seats = request.form.get("available_seats")

    # Validations
    if int(total_seats) <= 0:
        flash("Total seats must be greater than zero.", "error")
        return redirect(url_for("department.seat_update"))
    if int(available_seats) > int(total_seats):
        flash("Available seats cannot exceed total seats.", "error")
        return redirect(url_for("department.seat_update"))
    if int(total_seats) > 200:
        flash("Total seats cannot exceed 200 per class.", "error")
        return redirect(url_for("department.seat_update"))

    # Insert each department as a separate row
    for name in names:
        add_department_to_db(institute_code, name, total_seats, available_seats)
    flash("Departments added successfully!", "success")
    return redirect(url_for("department.seat_update"))



def add_department_to_db(institute_code, new_department, total_seats, available_seats):
    conn = get_department_connection()
    cursor = conn.cursor()
    # Always insert a new row for each department
    cursor.execute(
        """
        INSERT INTO departments (institute_code, department_name, total_seats, available_seats)
        VALUES (%s, %s, %s, %s)
        """,
        (institute_code, new_department, total_seats, available_seats),
    )
    conn.commit()
    conn.close()

@department_bp.route("/update-seats/<string:institute_code>/<int:department_id>", methods=["POST"])
def update_seats(institute_code, department_id):
    new_available = request.form.get("available_seats")
    if new_available is None or not new_available.isdigit() or int(new_available) < 0:
        flash("Please enter a valid number of available seats.", "error")
        return redirect(url_for("department.seat_update"))
    
    conn = get_department_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE departments SET available_seats = %s WHERE institute_code = %s AND id = %s",
        (new_available, institute_code, department_id),
    )
    conn.commit()
    conn.close()
    flash("Seats updated successfully!", "success")
    return redirect(url_for("department.seat_update"))



@department_bp.route("/delete_department/<string:institute_code>", methods=["POST"])
def delete_department(institute_code):
    conn = get_department_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM departments WHERE institute_code = %s",
        (institute_code,),
    )
    conn.commit()
    conn.close()
    flash("Department deleted successfully!", "success")
    return redirect(url_for("department.seat_update"))

@department_bp.route("/edit_department_name/<string:institute_code>", methods=["POST"])
def edit_department_name(institute_code):
    new_name = request.form.get("new_name")
    if not new_name:
        flash("Please enter a department name", "error")
        return redirect(url_for("department.seat_update"))
    conn = get_department_connection()
    cur = conn.cursor()
    cur.execute("UPDATE departments SET department_name=%s WHERE institute_code=%s", (new_name, institute_code))
    conn.commit()
    conn.close()
    flash("Department name updated successfully!", "success")
    return redirect(url_for("department.seat_update"))
