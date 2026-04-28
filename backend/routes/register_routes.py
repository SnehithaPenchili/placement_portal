from fastapi import APIRouter
from db import get_db_connection

router = APIRouter()

@router.post("/register")
def register(data: dict):
    try:
        email = data.get("email")

        #  1. EMAIL DOMAIN VALIDATION
        if not email.endswith("@uohyd.ac.in"):
            return {"success": False, "message": "Use institutional email only"}

        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. CHECK IF EMAIL EXISTS
        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return {"success": False, "message": "Email already registered"}

        #3. INSERT
        query = """
        INSERT INTO students (full_name, email, password, college)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (
            data.get("full_name"),
            email,
            data.get("password"),
            data.get("college")
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"success": True}

    except Exception as e:
        return {"success": False, "message": str(e)}