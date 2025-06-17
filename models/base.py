from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///monster_collection.db', echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_session():
    return SessionLocal()
