from typing import Annotated, List

from aiohttp.web_routedef import delete
from fastapi.params import Body, Depends
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database.models import Base, User, Queue
from database.database import engine
from database.schemas import User as dbUser, QueueCreate, Queue as dbQueue
from service import get_db, add_to_queue, del_from_queue

app = FastAPI()

Base.metadata.create_all(bind=engine)
user_name = "{{sensitive data}}"





@app.get("/users/", response_model=List[dbUser])
async def get_users(db: Session = Depends(get_db)) -> List[User] | List:
    db_users = db.query(User).all()
    return db_users

@app.get("/registration")
async def get_registration(username: str):
    global user_name
    user_name = username
    return {"name": user_name}

@app.get("/queue", response_model=List[dbQueue])
async def get_queue(db: Session = Depends(get_db)) -> List[dbQueue] | List:
    db_queue = db.query(Queue).all()
    return db_queue


@app.post("/queue/add")
async def update_queue(queue: Annotated[QueueCreate, Body(..., exempl={
    "title": "test1"
})], db: Session = Depends(get_db)) -> dbQueue:
    db_queue = await add_to_queue(queue, db, user_name=user_name)
    return db_queue

@app.delete("/queue/del")
async def quit_queue(db: Session = Depends(get_db)):
    await del_from_queue(db, user_name=user_name)


