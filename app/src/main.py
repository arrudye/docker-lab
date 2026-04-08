from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from src.core.database import get_engine
from src.routers import books, loans, readers

app = FastAPI(
    title="Library API",
    description="API для управления библиотекой",
    version="1.0.0"
)

app.include_router(books.router)
app.include_router(readers.router)
app.include_router(loans.router)

@app.get("/")
def root():
    return {
        "message": "Library API is running",
        "docs": "/docs",
        "endpoints": {
            "books": "/books",
            "readers": "/readers",
            "loans": "/loans"
        }
    }

@app.get("/health")
def health_check():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except OperationalError as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
