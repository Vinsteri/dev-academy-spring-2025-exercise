from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import electricity


app = FastAPI(title="Electricity Data API")


origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost",
    "http://dev-academy.westeurope.cloudapp.azure.com/"
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
