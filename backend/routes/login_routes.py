from fastapi import APIRouter
from db import get_db_connection

router = APIRouter()

@router.post("/login")
def login(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    email = data.get("email")
    password = data.get("password")
    #  Check in students table
    cursor.execute(
        "SELECT * FROM students WHERE email=? AND password=?",
        (email, password)
    )
    student = cursor.fetchone()

    # Check in admins table
    cursor.execute(
        "SELECT * FROM admins WHERE email=? AND password=?",
        (email, password)
    )
    admin = cursor.fetchone()

    cursor.close()
    conn.close()
    if admin:
        return {
            "success": True,
            "role": "admin",
            "user_id": admin["id"]
        }

    elif student:
        return {
            "success": True,
            "role": "student",
            "user_id": student["id"]
        }

    else:
        return {
            "success": False,
            "message": "Invalid credentials"
        }
    
@router.get("/check-profile/{user_id}")
def check_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM student_profiles WHERE user_id=?", (user_id,))
    result = dict(result)

    cursor.close()
    conn.close()

    return {"exists": bool(result)}