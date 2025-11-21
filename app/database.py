from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()   #Session is responsible for the Connection
    try: 
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='root', cursor_factory = RealDictCursor)
#     cur = conn.cursor()
#     print("Database Connection Successful")
# except Exception as error:
#         print('Connecting to Database Failed')
#         print("Error", error)
#         time.sleep(2)