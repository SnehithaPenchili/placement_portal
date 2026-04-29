from fastapi import APIRouter
from db import get_db_connection
import uuid

router = APIRouter()   #  MUST be defined BEFORE using @router

# CREATE JOB
@router.post("/jobs")
def create_job(job: dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO jobs 
        (company_name, job_role, industry, salary_lpa, deadline, description, eligibility, apply_url,application_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """

        cursor.execute(query, (
            job.get("company_name"),
            job.get("job_role"),
            job.get("industry"),
            job.get("salary_lpa"),
            job.get("deadline"),
            job.get("description"),
            job.get("eligibility"),
            job.get("apply_url"),
            job.get("application_type"),
            "active"
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Job created successfully"}

    except Exception as e:
        return {"error": str(e)}


# GET JOBS
@router.get("/jobs")
def get_jobs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()

        cursor.close()
        conn.close()

        return jobs

    except Exception as e:
        return {"error": str(e)}
    
@router.get("/admin/dashboard")
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT company_name) AS total_companies FROM jobs")
    total_companies = cursor.fetchone()["total_companies"]

    cursor.execute("SELECT COUNT(*) AS upcoming FROM jobs WHERE deadline >= DATE('now')")
    upcoming = cursor.fetchone()["upcoming"]

    students_placed = 312  # can improve later

    return {
        "total_companies": total_companies,
        "students_placed": students_placed,
        "upcoming": upcoming
    }