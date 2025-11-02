from app import database
from app.core.config import settings
from app.auth import routes as auth_routes
from app.users import routes as user_routes
from app.api import routes as api_routes

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Connecting to MongoDB: {settings.MONGO_URI} / DB: {settings.MONGO_DB}")

    yield

    database.client.close()
    print("MongoDB connection closed")

#development only
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI(title="Sweet Shop Management System",lifspan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(api_routes.router)

@app.get("/health")
def health():
    return {"status": "ok"}