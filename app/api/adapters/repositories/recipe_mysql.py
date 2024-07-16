from datetime import datetime, timezone
from typing import Dict, List

import sqlalchemy as sqlalchemy
import sqlalchemy.orm as orm

from app.extensions import db
from app.api.domain.models.recipe import Recipe
from app.api.domain.ports.recipe import RecipePort


class RecipeModel(db.Model):
    __tablename__ = "recipes"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    making_time: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    serves: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    ingredients: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100), nullable=False)
    cost: orm.Mapped[int] = orm.mapped_column(sqlalchemy.INTEGER, nullable=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at: orm.Mapped[datetime] = orm.mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False, onupdate=lambda: datetime.now(timezone.utc))


class RecipeRepository(RecipePort):

    def __init__(self, db_engine):
        self.db_engine = db_engine


    def get_recipe_by_id(self, recipe_id: int) -> List[Recipe] | None:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            return Recipe.model_validate(recipe._mapping)

        return None


    def get_all_recipes(self, recipe_id: int) -> List[Recipe] | None:
        pass


    def create_recipe(self, recipe: Recipe) -> Recipe:
        self.db_engine.session.add(recipe)
        self.db_engine.session.commit()
        return Recipe.model_validate(recipe._mapping)


    def update_recipe(self, recipe: Recipe, updated_data: Dict) -> Recipe | None:
        for attribute in updated_data:
            setattr(recipe, attribute, updated_data[attribute])

        self.db_engine.session.add(recipe)
        self.db_engine.session.commit()

        return Recipe.model_validate(recipe._mapping)


    def delete_recipe(self, recipe: Recipe):
        self.db_engine.session.delete(recipe)
        self.db_engine.session.commit()        
