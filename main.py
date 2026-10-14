from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Job Processing API",
    version="1.0.0",
    description="Backend service for managing asynchronous jobs"
)

@app.get("/")
def home():
    return {"message": "Enterprise Job Processing API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
