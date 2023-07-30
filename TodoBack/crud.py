import datetime
import logging

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

import models
from schemas import ItemCreateSchema, ItemUpdateSchema


def get_session(db: Session, session_uuid: str):
    return db.query(models.Session).filter(models.Session.uuid == session_uuid).first()


def create_session(db: Session, session_uuid: str, name: str):
    db_session = models.Session(name=name, uuid=session_uuid, last_activity=datetime.datetime.today())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_item_by_uuid(db: Session, item_uuid: str, raise_error: bool = False) -> models.Item:
    item = db.query(models.Item).filter(models.Item.uuid == item_uuid).first()
    if not item and raise_error:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def get_items(db: Session, session_uuid: str, skip: int = 0, limit: int = 0, search: str = '') -> list[models.Item]:
    filters = [models.Session.uuid == session_uuid,
               models.Item.session_id == models.Session.id]
    if search:
        filters.append(or_(models.Item.title.ilike(f"%{search}%"), models.Item.description.ilike(f"%{search}%")))
    if limit:
        return db.query(models.Item).filter(*filters).offset(skip).limit(limit).all()
    return db.query(models.Item).filter(*filters).all()


def get_items_count(db: Session, session_uuid: str, search: str = '') -> int:
    filters = [models.Session.uuid == session_uuid,
               models.Item.session_id == models.Session.id]
    if search:
        filters.append(or_(models.Item.title.ilike(f"%{search}%"), models.Item.description.ilike(f"%{search}%")))
    return db.query(models.Item).filter(*filters).count()


def create_session_item(db: Session, item: ItemCreateSchema, session_uuid: str):
    session: models.Session = get_session(db, session_uuid)
    db_item = models.Item(**item.model_dump(), session=session)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    update_session_last_actity(db, session_uuid)
    return db_item


def update_session_item(db: Session, item: ItemUpdateSchema, existing_item: models.Item,
                        session_uuid: str) -> models.Item:
    for key, value in item.model_dump().items():
        setattr(existing_item, key, value)

    db.add(existing_item)
    db.commit()
    db.refresh(existing_item)
    update_session_last_actity(db, session_uuid)
    return existing_item


def delete_session_item(db: Session, item_uuid: str, session_uuid: str):
    db.query(models.Item).filter(models.Item.uuid == item_uuid).delete()
    db.commit()
    update_session_last_actity(db, session_uuid)


def delete_session(db: Session, session_uuid: str):
    db.query(models.Session).filter(models.Session.uuid == session_uuid).delete()
    db.commit()


def update_session_last_actity(db: Session, session_uuid: str):
    session: models.Session = get_session(db, session_uuid)
    if session:
        session.last_activity = datetime.datetime.today()
        db.add(session)
        db.commit()
        db.refresh(session)


def remove_session_no_activity(db: Session, remove_before_day: datetime.date):

    db.query(models.Session).filter(models.Session.last_activity < remove_before_day).delete()
    db.commit()
