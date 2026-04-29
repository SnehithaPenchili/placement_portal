import sqlite3

conn = sqlite3.connect("placement.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    college TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS student_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    linkedin TEXT,
    university TEXT,
    degree TEXT,
    specialization TEXT,
    graduation_year INTEGER,
    cgpa REAL,
    coursework TEXT,
    skills TEXT,
    experience TEXT,
    projects TEXT,
    resume_url TEXT,
    profile_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_role TEXT,
    company_name TEXT,
    salary_lpa REAL,
    industry TEXT,
    description TEXT,
    eligibility TEXT,
    deadline TEXT,
    application_type TEXT,
    apply_url TEXT,
    status TEXT DEFAULT 'active'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    student_name TEXT,
    email TEXT,
    phone TEXT,
    cgpa REAL,
    resume_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students_placed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    company_name TEXT,
    job_role TEXT,
    salary_lpa REAL,
    department TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO admins (id, email, password)
VALUES (1, 'admin@uohyd.ac.in', 'admin123')
""")

conn.commit()
conn.close()

print(" SQLite DB ready")