import factory
from factory.fuzzy import FuzzyInteger
from factory.fuzzy import FuzzyText

from app.models import Recipe


class RecipeFactory(factory.Factory):
    class Meta:
        model = Recipe

    title = FuzzyText(length=60)
    serves = FuzzyText(length=60)
    making_time = FuzzyText(length=60)
    ingredients = FuzzyText(length=60)
    cost = FuzzyInteger(low=1, high=100)
