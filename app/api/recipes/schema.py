from marshmallow import post_load
from marshmallow import validates
import simplejson

from app.api.common.failures import Failures as CommonFailures
from app.api.common.validators import validate_monetary_value
from app.api.exceptions import RequestDataException
from app.api.extensions import schemas
from app.models import Recipe


class RecipeSchema(schemas.Schema):
    id = schemas.Integer(required=True, dump_only=True)
    title = schemas.String(required=True)
    making_time = schemas.String(required=True)
    serves = schemas.String(required=True)
    ingredients = schemas.String(required=True)
    cost = schemas.Integer(required=True)
    
    #created_at = schemas.Date(required=True, dump_only=True)
    #update_at = schemas.Date(required=True, dump_only=True)

    class Meta:
        json_module = simplejson

    def handle_error(self, exc, data, many, partial):
        response = CommonFailures.information_missing
        response['details'] = exc.messages
        raise RequestDataException(response)
    
    @validates('cost')
    def validate_transaction_value(self, value):
        validate_monetary_value(value, 'cost')

    @post_load
    def make_recipe(self, data, many, partial):
        return Recipe(**(data or {}))
