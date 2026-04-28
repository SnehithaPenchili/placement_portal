from fastapi import APIRouter
from db import get_db_connection
import json

router = APIRouter()


# ✅ ADD STUDENT (ADMIN)
@router.post("/students")
def add_student(data: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students_placed 
            (student_name, company_name, job_role, salary_lpa, department)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data.get("student_name"),
            data.get("company_name"),
            data.get("job_role"),
            data.get("salary_lpa"),
            data.get("department")
        ))

        conn.commit()
        conn.close()

        return {"message": "Student added successfully"}

    except Exception as e:
        return {"error": str(e)}


# ✅ GET ALL PLACED STUDENTS
@router.get("/students")
def get_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students_placed ORDER BY salary_lpa DESC")
        rows = cursor.fetchall()

        data = [dict(row) for row in rows]

        conn.close()

        return data

    except Exception as e:
        return {"error": str(e)}


# ✅ GET SINGLE STUDENT PROFILE
@router.get("/students/{user_id}")
def get_student(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student_profiles WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else {"error": "Not found"}


# ✅ GET PROFILE
@router.get("/profile/{user_id}")
def get_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM student_profiles WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else {"error": "Profile not found"}


# ✅ SAVE / UPDATE PROFILE (SQLite FIX)
@router.post("/profile")
def save_profile(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔥 Check if profile exists
    cursor.execute(
        "SELECT * FROM student_profiles WHERE user_id=?",
        (data["user_id"],)
    )
    existing = cursor.fetchone()

    if existing:
        # ✅ UPDATE
        cursor.execute("""
            UPDATE student_profiles SET
            full_name=?, email=?, phone=?, address=?, linkedin=?,
            university=?, degree=?, specialization=?, graduation_year=?,
            cgpa=?, coursework=?, skills=?, experience=?, projects=?,
            resume_url=?, profile_image=?
            WHERE user_id=?
        """, (
            data["full_name"],
            data["email"],
            data["phone"],
            data["address"],
            data["linkedin"],
            data["university"],
            data["degree"],
            data["specialization"],
            data["graduation_year"],
            data["cgpa"],
            data["coursework"],
            data["skills"],
            json.dumps(data["experience"]),
            json.dumps(data["projects"]),
            data["resume_url"],
            data["profile_image"],
            data["user_id"]
        ))

    else:
        # ✅ INSERT
        cursor.execute("""
            INSERT INTO student_profiles 
            (user_id, full_name, email, phone, address, linkedin,
             university, degree, specialization, graduation_year, cgpa,
             coursework, skills, experience, projects, resume_url, profile_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["user_id"],
            data["full_name"],
            data["email"],
            data["phone"],
            data["address"],
            data["linkedin"],
            data["university"],
            data["degree"],
            data["specialization"],
            data["graduation_year"],
            data["cgpa"],
            data["coursework"],
            data["skills"],
            json.dumps(data["experience"]),
            json.dumps(data["projects"]),
            data["resume_url"],
            data["profile_image"]
        ))

    conn.commit()
    conn.close()

    return {"message": "Profile saved"}