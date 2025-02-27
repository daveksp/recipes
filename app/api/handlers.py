from flask import current_app
from flask import jsonify

from app.api.exceptions import ApiException
from app.api.exceptions import RequestDataException
from app.api.utils import request_ids


def setup_handlers(app):

    @app.after_request
    def add_request_ids_to_header(response):
        display_id, original_request_id = request_ids()
        if original_request_id:
            display_id = '{},{}'.format(original_request_id, display_id)

        response.headers.extend({'Request-Id': display_id})
        return response

    @app.errorhandler(ApiException)
    def bad_request(e):
        return jsonify({'error': e.errors}), 400

    @app.errorhandler(RequestDataException)
    def request_data_error(e):
        error = e.errors[0] if type(e.errors) == list else e.errors
        #response = {'error': error}
        response = {
            "message": "Recipe creation failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }
        return jsonify(response), 400

    @app.errorhandler(Exception)
    def internal_server_error(e):
        current_app.logger.exception(e)
        return jsonify({
            'message': "Apologies, there's been an unexpected error."}), 500

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(
            {'message':
                "The request resource was not found. "
                "Please check the URL."}), 404
