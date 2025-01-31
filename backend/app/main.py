from fastapi import FastAPI
from app.routers import electricity


app = FastAPI(title="Electricity Data API")

# Include the router
app.include_router(electricity.router, prefix="/api", tags=["Electricity"])
