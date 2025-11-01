from app import database
from app.core.config import settings
from app.auth import routes as auth_routes
from app.users import routes as user_routes

from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Connecting to MongoDB: {settings.MONGO_URI} / DB: {settings.MONGO_DB}")

    yield

    database.client.close()
    print("MongoDB connection closed")

app = FastAPI(title="Sweet Shop Management System",lifspan=lifespan)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)

@app.get("/health")
def health():
    return {"status": "ok"}