from multiprocessing import synchronize
from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor

from app.routers import auth
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils
from  .routers import user, post



app = FastAPI()


#title: str What data we want from the post request--> 
#Schema...



models.Base.metadata.create_all(bind=engine)


    


try:
    conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='root', cursor_factory = RealDictCursor)
    cur = conn.cursor()
    print("Database Connection Successful")
except Exception as error:
    print('Connecting to Database Failed')
    print("Error", error)


my_posts = [{"title:": "title of Post 1 ", "content": "content of post 1", "id": 1}, 
           {"title":"favorite foods", "content": "I like pizza", "id": 2}]

@app.get("/")
def root():
    return {"message" : "Divinixx Here! Karan Aujla"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return  posts




def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
#Why We need Schema?
# It's a pain to get all the values from the Body
# The client can send whatever data they want
# The data isn't getting validated
# We ultimately want to force the client to send data in a schema that we expect 



