import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from src.core.database import Base, get_db  # убрали _engine, _SessionLocal
from src.main import app

# Тестовая БД (SQLite в памяти)
TEST_DATABASE_URL = "sqlite:///:memory:?check_same_thread=False"

@pytest.fixture(scope="session")
def engine():
    """Создает тестовый engine"""
    engine = create_engine(
        TEST_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(engine):
    """Создает сессию БД для каждого теста"""
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """TestClient с подменой БД"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_book_data():
    """Данные для тестовой книги"""
    return {
        "title": "Тестовая книга",
        "author": "Тестовый автор",
        "genre": "Тестовый жанр",
        "year": 2024
    }


@pytest.fixture
def sample_reader_data():
    """Данные для тестового читателя"""
    return {
        "name": "Тестовый читатель",
        "email": "test@example.com"
    }