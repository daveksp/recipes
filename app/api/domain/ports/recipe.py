from abc import ABC, abstractmethod
from typing import List

from app.api.domain.models.recipe import Recipe


class RecipePort(ABC):

    @abstractmethod
    async def get_recipe_by_id(self, recipe_id: int) -> List[Recipe] | None:
        pass

    @abstractmethod
    async def get_all_recipes(self) -> List[Recipe] | None:
        pass

    @abstractmethod
    async def create_recipe(self, recipe: Recipe) -> Recipe:
        pass

    @abstractmethod
    async def update_recipe(self, recipe: Recipe) -> Recipe | None:
        pass

    @abstractmethod
    async def delete_recipe(self, recipe: Recipe):
        pass
