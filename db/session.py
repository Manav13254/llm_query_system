from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from urllib.parse import quote_plus

password = quote_plus(settings.DB_PASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
