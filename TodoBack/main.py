import datetime
import logging
import uuid
from typing import Annotated, Union

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import models, schemas, crud
from crud import get_session, create_session, get_items
from db import SessionLocal, engine
from schemas import SessionSchema

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

logger = logging.getLogger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable session management
SESSION_REQUEST_KEY = 'session_uuid'
SESSION_COOKIE_NAME = 'todo-session-cookie'
app.add_middleware(SessionMiddleware, secret_key="todo-session",
                   session_cookie=SESSION_COOKIE_NAME,
                   max_age=None, )

ITEM_DOCS_TAG = "Item"


# Dependency for start a session of DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Dependency to check enabled session when requesting to resources
# Cloud use middleware, but not found a way to exclude specific route when setting up a middleware
async def check_session(request: Request):
    session_uuid = request.session.get(SESSION_REQUEST_KEY, None)
    if not session_uuid:
        raise HTTPException(status_code=403, detail="Session must be started before")
    return session_uuid


@app.post("/")
async def start_session(request: Request, user: SessionSchema, db: Session = Depends(get_db)):
    session_uuid = request.session.get(SESSION_REQUEST_KEY, None)
    if session_uuid:
        session: models.Session = get_session(db, session_uuid=session_uuid)
        if session:
            return {"message": f"Hi again {session.name}"}

    session_uuid = str(uuid.uuid4())
    create_session(db, session_uuid=session_uuid, name=user.name)

    request.session[SESSION_REQUEST_KEY] = session_uuid
    return {"message": f"Welcome {user.name}!"}


@app.delete("/me")
async def finish_session(request: Request, session_uuid: Annotated[str, Depends(check_session)],
                         db: Session = Depends(get_db)):
    crud.delete_session(db, session_uuid)
    del request.session[SESSION_REQUEST_KEY]
    return {'message': "Bye!"}


@app.get("/me")
async def me(request: Request, session_uuid: Annotated[str, Depends(check_session)], db: Session = Depends(get_db)) -> \
Union[SessionSchema, None]:
    session: models.Session = get_session(db, session_uuid=session_uuid)
    if not session:
        del request.session[SESSION_REQUEST_KEY]
        raise HTTPException(status_code=403, detail="Session must be started before")
    return session


@app.get("/items", tags=[ITEM_DOCS_TAG])
async def get_items(session_uuid: Annotated[str, Depends(check_session)], db: Session = Depends(get_db),
                    limit: int = Query(20, ge=0),
                    page: int = Query(1, ge=1), search: str = Query('')) -> schemas.ItemListSchema:
    items: list[models.Item] = crud.get_items(db, session_uuid=session_uuid, skip=(page - 1) * limit, limit=limit,
                                              search=search)
    total_items: int = crud.get_items_count(db, session_uuid=session_uuid, search=search)
    item_list_schema = schemas.ItemListSchema(count=len(items), items=items, total=total_items,
                                              pages=(total_items // limit) + 1)

    return item_list_schema


@app.post("/items", tags=[ITEM_DOCS_TAG])
async def post_item(body: schemas.ItemCreateSchema, session_uuid: Annotated[str, Depends(check_session)],
                    db: Session = Depends(get_db)) -> schemas.ItemSchema:
    item: models.Item = crud.create_session_item(db, body, session_uuid)
    return item


@app.put("/items/{item_uuid}", tags=[ITEM_DOCS_TAG])
async def put_item(item_uuid: str, body: schemas.ItemUpdateSchema, session_uuid: Annotated[str, Depends(check_session)],
                   db: Session = Depends(get_db)) -> schemas.ItemSchema:
    existing_item: models.Item = crud.get_item_by_uuid(db, item_uuid, raise_error=True)
    item: models.Item = crud.update_session_item(db, body, existing_item, session_uuid)
    return item


@app.delete("/items/{item_uuid}", tags=[ITEM_DOCS_TAG])
async def delete_item(item_uuid: str, session_uuid: Annotated[str, Depends(check_session)],
                      db: Session = Depends(get_db)):
    item: models.Item = crud.delete_session_item(db, item_uuid, session_uuid)


@app.get("/liveliness", tags=["Health"], summary="Endpoint for check system is still alive")
async def liveliness():
    return


@app.get("/readiness", tags=["Health"], summary="Endpoint for check DB connection is alive")
async def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()



def check_list_len():
    logger.info("************** Start Scheduled task: check expired sessions **************")
    db = next(get_db())
    delete_before_date = datetime.datetime.today() - datetime.timedelta(days=30)
    crud.remove_session_no_activity(db, delete_before_date)
    logger.info("************** End Scheduled task: check expired sessions **************")


@app.on_event('startup')
def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_list_len, 'cron', day='*/1')
    scheduler.start()

if __name__ == 'ToDoBack.main':

    # Create DB tables
    models.Base.metadata.create_all(bind=engine)