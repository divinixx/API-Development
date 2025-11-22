from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts" ,
    tags = ['Posts']
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user),
               limit: int  = 10, skip: int = 0, search: Optional[str] = ""):
    # cur.execute(""" SELECT * FROM posts """)
    # posts = cur.fetchall()
    # cur.close()
    print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #.filter(models.Post.owner_id == current_user.id)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).offset(skip).all()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post convert pydantic model into dict
    # post_dict = post.model_dump() #dict--> model_dump
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)

    # cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #             (post.title, post.content , post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    
    
    # print(**post.model_dump())
    
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):

    # id is passed in string format not in int format so, we have to typecast 

    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # test_post = cur.fetchone()
    # post = find_post(id)

    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #.filter(models.Post.owner_id == current_user.id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return  post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the array that has required ID
    # cur.execute(""" DELETE  FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    post = delete_post.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  #special One to encounter the Warning


@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    
    # cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))

    # updated_post = cur.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

    

# @app.post("/createpost") #Extract the Data from the JSON and Converting into Dictionary
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}
