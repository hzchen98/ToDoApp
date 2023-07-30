from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.environ.get('MYSQL_USER', 'app')
DB_PASS = os.environ.get('MYSQL_PASSWORD', "app")
DB_HOST = os.environ.get('MYSQL_HOST', 'localhost')
DB_PORT = os.environ.get('MYSQL_PORT', 5002)
DB_NAME = os.environ.get('MYSQL_DB', "basf-todo-app")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
