from fastapi import APIRouter
from db import get_db_connection
    
import json
router = APIRouter()

# ADD STUDENT (ADMIN)
@router.post("/students")
def add_student(data: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO students_placed (student_name, company_name, job_role, salary_lpa,department)
        VALUES (%s, %s, %s, %s,%s)
        """

        cursor.execute(query, (
            data.get("student_name"),
            data.get("company_name"),
            data.get("job_role"),
            data.get("salary_lpa"),
            data.get("department")
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Student added successfully"}

    except Exception as e:
        return {"error": str(e)}


# ✅ GET ALL PLACED STUDENTS
@router.get("/students")
def get_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students_placed ORDER BY salary_lpa DESC")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    except Exception as e:
        return {"error": str(e)}
@router.get("/students")
def get_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students_placed")
        students = cursor.fetchall()

        cursor.close()
        conn.close()

        return students

    except Exception as e:
        return {"error": str(e)}
    
@router.get("/students/{user_id}")
def get_student(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM student_profiles WHERE user_id=%s", (user_id,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return student


@router.get("/profile/{user_id}")
def get_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM student_profiles WHERE user_id=%s",
        (user_id,)
    )

    profile = cursor.fetchone()

    cursor.close()
    conn.close()

    if profile:
        return profile
    else:
        return {"error": "Profile not found"}

@router.post("/profile")
def save_profile(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO student_profiles 
    (user_id, full_name, email, phone, address, linkedin,
     university, degree, specialization, graduation_year, cgpa, coursework,
     skills, experience, projects, resume_url,profile_image)

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    ON DUPLICATE KEY UPDATE
    full_name=%s, phone=%s, address=%s, linkedin=%s,
    degree=%s, cgpa=%s, skills=%s, experience=%s, projects=%s,profile_image="%s"
    """

    cursor.execute(query, (
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
        data["profile_image"],

        data["full_name"],
        data["phone"],
        data["address"],
        data["linkedin"],
        data["degree"],
        data["cgpa"],
        data["skills"],
        json.dumps(data["experience"]),
        json.dumps(data["projects"]),
        data["profile_image"] 
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Profile saved"}