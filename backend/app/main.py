from fastapi import FastAPI
from backend.app.api import endpoints

# Initialize the application
app = FastAPI(
    title="Gear Hunter API",
    description="The backend engine for finding used climbing gear.",
    version="1.0.0"
)

# Plug in the router we just built
app.include_router(endpoints.router, prefix="/api")

# A simple root check to make sure the server is alive
@app.get("/")
def read_root():
    return {"status": "success", "message": "Gear Hunter API is running!"}
