from flask import abort
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Api
from flask_restful import Resource

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

    def post(self):
        """ Create a recipe """
        recipe = Recipe(**request.json)
        #book = await book_port.create_book(book)

        response.status_code = status.HTTP_201_CREATED
        response.headers[
            http.HEADER_CONTENT_TYPE
        ] = http.HEADER_CONTENT_TYPE_APPLICATION_JSON
        return CreateBookV1Response(
            book_isbn=book.isbn,
        )

        recipe_schema = RecipeSchema()
        recipe = recipe_schema.load(request.json or {})

        db.session.add(recipe)
        db.session.commit()

        response = {
            "message": recipe_created,
            "recipe": []
        }
        response['recipe'].append(recipe_schema.dump(recipe))
        return make_response(jsonify(response), 200)

    def get(self, recipe_id=None):
        """retrieves a list of recipes"""
        recipe_schema = RecipeSchema()
        response = None

        if request.path.endswith('/'):
            recipe_id = 1

        if recipe_id:
            recipe = Recipe.query.get(recipe_id)
            if not recipe:
                current_app.logger.exception(f"Recipe with id={recipe_id} not found")
                return make_response(jsonify({}), 200)
            else:
                response = {
                    "message": recipe_details,
                    "recipe": [recipe_schema.dump(recipe)]
                }
                
        else:
            recipes = Recipe.query.all()
            response = {
                "recipes": recipe_schema.dump(recipes, many=True)
            }
            #response = 

        return make_response(jsonify(response), 200)

    def patch(self, recipe_id=None):
        """updates a specific recipe"""
        recipe_schema = RecipeSchema()

        if request.path.endswith('/'):
            recipe_id = 1

        recipe = Recipe.query.get(recipe_id)
        data = request.json 
        
        if not recipe:
            current_app.logger.exception(f"Recipe with id={recipe_id} not found")
            return make_response(jsonify({}), 200)
            #abort(404)

        for attribute in data:
            setattr(recipe, attribute, data[attribute])

        db.session.add(recipe)
        db.session.commit()

        response = {
            "message": recipe_updated,
            "recipe": [recipe_schema.dump(recipe)]
        }
        #response = recipe_schema.dump(recipe)
        return make_response(jsonify(response), 200)
    
    def delete(self, recipe_id):
        """deletes a specific recipe"""

        recipe = Recipe.query.get(recipe_id)
        
        if not recipe:
            current_app.logger.exception(f"Recipe with id={recipe_id} not found")
            response = {
                "message": recipe_not_found,
            }
            return make_response(jsonify(response), 200)
        
        db.session.delete(recipe)
        db.session.commit()
        
        response = {
            "message": recipe_removed,
        }
        return make_response(jsonify(response), 200)