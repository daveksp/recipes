from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, LetterCase
from pydantic import BaseModel


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Recipe(BaseModel):
    id: Optional[int] = None
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
