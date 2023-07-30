import uuid as uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func, Boolean, Date
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    last_activity = Column(Date(), nullable=True, default=None)



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=uuid.uuid4)
    title = Column(String(50), nullable=False)
    description = Column(String(500))

    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    session = relationship(Session, backref="items")

    done = Column(Boolean, default=False)
