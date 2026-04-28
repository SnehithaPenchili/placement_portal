
from fastapi import FastAPI
from db import get_db_connection
from routes.job_routes import router as job_router
from routes.login_routes import router as login_router
from fastapi.middleware.cors import CORSMiddleware
from routes.register_routes import router as register_router
from routes.student_routes import router as student_router
from routes.application_routes import router as application_router
app = FastAPI()

app.include_router(job_router)
app.include_router(login_router)
app.include_router(register_router)
app.include_router(student_router)
app.include_router(application_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Backend running "}