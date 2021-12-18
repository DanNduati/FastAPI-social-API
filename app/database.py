from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_uri

#create sqlalchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#SessionLocal class -> instances of this class are database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base class -> To be inherited when creating database ORM models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print('Error: ' + str(e))
    finally:
        db.close()