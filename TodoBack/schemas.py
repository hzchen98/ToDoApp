from typing import Union, Optional

from pydantic import BaseModel, Field, constr, ConfigDict


class ItemBaseSchema(BaseModel):
    title: constr(max_length=50)
    description: constr(max_length=500)


class ItemCreateSchema(ItemBaseSchema):
    pass

class ItemSchema(ItemBaseSchema):
    uuid: str
    done: bool

    class Config:
        from_attributes = True

class ItemUpdateSchema(ItemBaseSchema):
    done: bool


class ItemListSchema(BaseModel):
    total: int
    pages: int
    count: int
    items: list[ItemSchema]


class SessionSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
