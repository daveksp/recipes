from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from flask import abort
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Api
from flask_restful import Resource

from app.api.adapters.entrypoints.rest.v1.models.recipe import CreateRecipeV1Response
from app.api.adapters.entrypoints.rest.v1.models.recipe import CreateRecipeV1ListResponse
from app.api.adapters.entrypoints.rest.v1.models.recipe import CreateRecipeV1Request
from app.api.recipes.schema import RecipeSchema
from app.extensions import db
from app.api.messages import recipe_details
from app.api.messages import recipe_created
from app.api.messages import recipe_not_found
from app.api.messages import recipe_removed
from app.api.messages import recipe_updated
from app.api.domain.models.recipe import Recipe
from app.api.domain.ports.recipe import RecipePort
from app.models import Recipe
#from app.models import Filters


blueprint = Blueprint('recipes', __name__, url_prefix='api/v1/recipes')
api = Api(blueprint)


@api.resource('/', '/<recipe_id>', endpoint="get recipe")
@api.resource('')
class AccountsResource(Resource):

    @inject
    def post(self, recipe_port: RecipePort):
        """ Create a recipe """
        recipe = Recipe(**request.json)
        recipe_port = None
        recipe = recipe_port.create_recipe(recipe)

        return CreateRecipeV1Response(
            **recipe
        ), 201


    def get(self, recipe_port: RecipePort, recipe_id=None):
        """retrieves a list of recipes"""
        response = None

        if request.path.endswith('/'):
            recipe_id = 1

        if recipe_id:
            recipe = recipe_port.get_recipe_by_id(recipe_id)
            if not recipe:
                current_app.logger.exception(f"Recipe with id={recipe_id} not found")
                return make_response(jsonify({}), 200)
            else:
                response = {
                    "message": recipe_details,
                    "recipe": [recipe]
                }
                
        else:
            recipes = recipe_port.get_all_recipes()
            response = {
                "recipes": recipes
            }
        return make_response(jsonify(response), 200)


    def patch(self, recipe_port: RecipePort, recipe_id=None):
        """updates a specific recipe"""
        recipe_schema = RecipeSchema()

        if request.path.endswith('/'):
            recipe_id = 1

        recipe = recipe_port.get_recipe_by_id(recipe_id)
        if not recipe:
            current_app.logger.exception(f"Recipe with id={recipe_id} not found")
            return make_response(jsonify({}), 200)

        data = request.json 
        updated_recipe = recipe_port.update_recipe(recipe, data)

        response = {
            "message": recipe_updated,
            "recipe": [updated_recipe]
        }
        return make_response(jsonify(response), 200)
    

    def delete(self, recipe_port: RecipePort, recipe_id):
        """deletes a specific recipe"""

        recipe = recipe_port.get_recipe_by_id(recipe_id)
        if not recipe:
            current_app.logger.exception(f"Recipe with id={recipe_id} not found")
            response = {
                "message": recipe_not_found,
            }
            return make_response(jsonify(response), 200)
        
        recipe_port.delete_recipe(recipe)  
        response = {
            "message": recipe_removed,
        }
        return make_response(jsonify(response), 200)
