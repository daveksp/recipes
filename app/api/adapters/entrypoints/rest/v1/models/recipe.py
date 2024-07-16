from datetime import datetime

from pydantic import BaseModel


class CreateRecipeV1Request(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int


class CreateRecipeV1Response(BaseModel):
    id: int 
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int
    created_at: datetime
    update_at: datetime


class CreateRecipeV1ListResponse(BaseModel):
    recipes: list[CreateRecipeV1Response]
