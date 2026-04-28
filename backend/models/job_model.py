from pydantic import BaseModel

class Job(BaseModel):
    company_name: str
    job_role: str
    industry: str
    salary_lpa: float
    deadline: str
    description: str
    eligibility: str
    apply_url: str