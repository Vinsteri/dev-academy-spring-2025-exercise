from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import electricity


app = FastAPI(title="Electricity Data API")


origins = [
    "http://localhost:5173",    # for local development
    "http://localhost:8080"     # when deployed as container
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Include the router
app.include_router(electricity.router, prefix="/api", tags=["Electricity"])
