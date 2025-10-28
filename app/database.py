from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLModel = 'postgresql://postgres:root@localhost/fastapi'

engine = create_engine(SQLModel )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()   #Session is responsible for the Connection
    try: 
        yield db
    finally:
        db.close()
