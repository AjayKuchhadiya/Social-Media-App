# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from config import setting


password = setting.database_password
encoded_password = quote_plus(password)

SQLALCHEMY_DATABASE_URL = f"postgresql://{setting.database_username}:{encoded_password}@{setting.database_hostname}/{setting.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
