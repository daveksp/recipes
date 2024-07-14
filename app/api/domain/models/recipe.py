from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Recipe:
    id = int
    title = str
    making_time = datetime
    serves = str
    ingredients = str
    cost = int