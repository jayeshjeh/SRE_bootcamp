import logging
from flask import Blueprint, request, jsonify
from .models import Student
from . import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

student_bp = Blueprint("students", __name__)

# ➕ Add new student
@student_bp.route("/", methods=["POST"])
def add_student():
    data = request.get_json()
    logging.info(f"POST /students - Payload: {data}")

    if not data or not all(k in data for k in ("name", "age", "grade")):
        logging.warning("Invalid input for creating student")
        return jsonify({"error": "Invalid input"}), 400

    new_student = Student(name=data["name"], age=data["age"], grade=data["grade"])
    db.session.add(new_student)
    db.session.commit()
    logging.info(f"Student created: {new_student.to_dict()}")

    return jsonify(new_student.to_dict()), 201

# 📋 Get all students
@student_bp.route("/", methods=["GET"])
def get_all_students():
    logging.info("GET /students - Fetching all students")
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

# 🔍 Get a student by ID
@student_bp.route("/<int:id>", methods=["GET"])
def get_student(id):
    logging.info(f"GET /students/{id} - Fetching student")
    student = Student.query.get(id)
    if student:
        return jsonify(student.to_dict()), 200
    logging.error(f"Student with ID {id} not found")
    return jsonify({"error": "Student not found"}), 404

# ✏️ Update a student
@student_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()
    logging.info(f"PUT /students/{id} - Payload: {data}")

    student = Student.query.get(id)
    if not student:
        logging.error(f"Student with ID {id} not found for update")
        return jsonify({"error": "Student not found"}), 404

    student.name = data.get("name", student.name)
    student.age = data.get("age", student.age)
    student.grade = data.get("grade", student.grade)
    db.session.commit()
    logging.info(f"Student updated: {student.to_dict()}")

    return jsonify(student.to_dict()), 200

# ❌ Delete a student
@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):
    logging.info(f"DELETE /students/{id} - Attempting to delete student")
    student = Student.query.get(id)
    if not student:
        logging.error(f"Student with ID {id} not found for deletion")
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    logging.info(f"Student with ID {id} deleted")

    return jsonify({"message": "Student deleted"}), 200
