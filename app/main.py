from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items

app = FastAPI(
    title="Inventory API",
    description="FastAPI application connected to MySQL",
    version="1.0.0"
)

# Enable CORS so frontend apps running on different ports/hosts can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints from routers
app.include_router(items.router)

@app.get("/")
def root():
    return {"status": "online", "message": "FastAPI MySQL server is running"}