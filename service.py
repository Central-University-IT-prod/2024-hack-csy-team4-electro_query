from typing import Annotated

from fastapi import Body, Depends
from sqlalchemy.orm import Session

from database.database import session_local
from database.schemas import QueueCreate, Queue as dbQueue
from database.models import Queue, User
from fastapi import HTTPException


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def find_id_by_name(db: Session, user_name: str):
    user_id = db.query(User).filter(User.name == user_name).first()
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id.telegram_id


async def add_to_queue(queue: Annotated[QueueCreate, Body(..., exempl={
    "title": "test1"
})], db: Session, user_name: str) -> dbQueue:
    user_id = find_id_by_name(db, user_name)
    existing_entry = db.query(Queue).filter_by(userId=user_id).first()
    if existing_entry is None:
        db_queue = Queue(userId=user_id, title=queue.title)
        db.add(db_queue)
        db.commit()
        db.refresh(db_queue)
        return db_queue
    print("bad user")
    raise HTTPException(status_code=404, detail="Queue already exists")


async def del_from_queue(db: Session, user_name: str):
    user_id = find_id_by_name(db, user_name)
    queue_delete = db.query(Queue).filter_by(userId=user_id).first()
    if queue_delete:
        print("del!")
        db.delete(queue_delete)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Queue not found")
