from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.db import init_db
import os

app = FastAPI(title="Summary API", docs_url="/docs", redoc_url="/redoc")
"""FastAPI application for summarizing long-form content using OpenAI GPT-4."""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    """Initialize the database on application startup."""
    await init_db()

app.include_router(router) 