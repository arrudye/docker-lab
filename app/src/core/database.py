from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "library")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MAX_RETRIES = 100
RETRY_DELAY = 3

def create_engine_with_retry():
    retries = 0
    last_exception = None
    
    while retries < MAX_RETRIES:
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Успешное подключение к PostgreSQL")
            return engine
        except OperationalError as e:
            last_exception = e
            retries += 1
            if retries < MAX_RETRIES:
                logger.warning(f"Попытка подключения к PostgreSQL {retries}/{MAX_RETRIES} не удалась. Повтор через {RETRY_DELAY} сек...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Не удалось подключиться к PostgreSQL после {MAX_RETRIES} попыток")
                raise last_exception

engine = create_engine_with_retry()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()