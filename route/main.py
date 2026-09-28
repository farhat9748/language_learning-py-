from flask import Blueprint, render_template, url_for, redirect, flash, request
from model import db


# Import Student if it exists, otherwise set to None
try:
    from model import Student
except ImportError:
    Student = None


main_bp = Blueprint("main", __name__)


@main_bp.route("/home")
def home():
    # Get all students from database if Student model exists
    students = []
    if Student:
        students = Student.query.all()
    
    # Calculate stats
    stats = {
        "total_students": len(students),
        "languages": 6,
        "lessons": "25+",
        "avg_progress": "85%"
    }
    
    return render_template(
        "index.html",
        students=students,
        stats=stats,
        page="home"
    )


@main_bp.route("/add-student", methods=["GET", "POST"])
def add_student():
    if not Student:
        flash("Student model not available", "error")
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        language = request.form.get("language")
        level = request.form.get("level")
        
        # Create new student
        new_student = Student(
            name=name,
            email=email,
            language=language,
            level=level
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        flash("Student added successfully!", "success")
        return redirect(url_for("main.home"))
    
    return render_template("index.html", page="add_student")


@main_bp.route("/edit-student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    if not Student:
        flash("Student model not available", "error")
        return redirect(url_for("main.home"))
    
    student = Student.query.get_or_404(student_id)
    
    if request.method == "POST":
        student.name = request.form.get("name")
        student.email = request.form.get("email")
        student.language = request.form.get("language")
        student.level = request.form.get("level")
        
        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for("main.home"))
    
    return render_template("index.html", page="edit_student", student=student)


@main_bp.route("/delete-student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if not Student:
        flash("Student model not available", "error")
        return redirect(url_for("main.home"))
    
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    
    flash("Student deleted successfully!", "success")
    return redirect(url_for("main.home"))


@main_bp.route("/lesson/<language>")
def lesson_detail(language):
    action = request.args.get("action", "start")
    
    if action == "pay":
        return redirect(url_for("pay_language", language=language))
    
    return redirect(url_for("start_learning", language=language))