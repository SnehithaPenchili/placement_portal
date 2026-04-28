from fastapi import APIRouter
from db import get_db_connection
import pandas as pd
from fastapi.responses import FileResponse
import os

router = APIRouter()

#  APPLY JOB
@router.post("/apply")
def apply_job(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO applications
    (job_id, student_name, email, phone, cgpa, resume_link)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (
        data.get("job_id"),
        data.get("student_name"),
        data.get("email"),
        data.get("phone"),
        data.get("cgpa"),
        data.get("resume_link")
    ))

    conn.commit()
    print("INSERTED SUCCESSFULLY") 
    cursor.close()
    conn.close()

    return {"message": "Applied successfully"}


#  GET APPLICATIONS PER JOB
@router.get("/applications/{job_id}")
def get_applications(job_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE job_id=?", (job_id,))
    data = [dict(row) for row in data]

    cursor.close()
    conn.close()

    return data


#  EXPORT TO EXCEL
@router.get("/applications/export/{job_id}")
def export_excel(job_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE job_id=?", (job_id,))
    data = [dict(row) for row in data]

    df = pd.DataFrame(data)

    file_path = f"applications_{job_id}.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(
        path=file_path,
        filename=file_path,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )



@router.get("/export-placements")
def export_placements():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch placed students
    cursor.execute("SELECT * FROM students_placed")
    data = [dict(row) for row in data]

    cursor.close()
    conn.close()

    if not data:
        return {"error": "No data found"}

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save file
    file_path = "placements_report.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(
        path=file_path,
        filename="placements_report.xlsx",
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )