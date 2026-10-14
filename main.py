
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI(
    title="Enterprise Job Processing API",
    version="1.0.0"
)

# Temporary in-memory storage
jobs = {}


class JobCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    job_type: str = Field(min_length=3, max_length=50)


class JobResponse(JobCreate):
    id: str
    status: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/jobs",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_job(job: JobCreate):
    job_id = str(uuid4())

    new_job = JobResponse(
        id=job_id,
        name=job.name,
        job_type=job.job_type,
        status="pending"
    )

    jobs[job_id] = new_job
    return new_job


@app.get("/jobs", response_model=list[JobResponse])
def list_jobs():
    return list(jobs.values())


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str):
    job = jobs.get(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job
