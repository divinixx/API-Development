from fastapi import Body, FastAPI, Depends
from .database import engine
from . import models
from  .routers import user, post, auth, vote
from . import config
from fastapi.middleware.cors import CORSMiddleware

# print(settings.database_username)
app = FastAPI()


origins = ["*"]
# models.Base.metadata.create_all(bind=engine)  -- CREATE THE DATABASE USING SQL ALCHEMY

@app.get("/")
def root():
    return {"message" : "Divinixx Here! Karan Aujla"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





