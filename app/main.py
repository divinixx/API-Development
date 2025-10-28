from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models
app = FastAPI()

#title: str What data we want from the post request--> 
#Schema...

models.Base.metadata.create_all(bind=engine)


    
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    return {"data": posts}


@app.get("/posts")

def get_posts():
    cur.execute(""" SELECT * FROM posts """)
    posts = cur.fetchall()
    cur.close()
    print(posts)
    return {"data": posts}


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    # post convert pydantic model into dict
    # post_dict = post.model_dump() #dict--> model_dump
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                (post.title, post.content , post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")  #Structure Matters while designing the API
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}



@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # id is passed in string format not in int format so, we have to typecast 
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    test_post = cur.fetchone()
    # post = find_post(id)
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post_detail": test_post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find the index in the array that has required ID
    cur.execute(""" DELETE  FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()
    
    if deleted_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)  #special One to encounter the Warning


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))

    updated_post = cur.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    return {"data": updated_post}

    

# @app.post("/createpost") #Extract the Data from the JSON and Converting into Dictionary
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}



#Why We need Schema?
# It's a pain to get all the values from the Body
# The client can send whatever data they want
# The data isn't getting validated
# We ultimately want to force the client to send data in a schema that we expect 