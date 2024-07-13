from decimal import Decimal

from flask_testing import TestCase

from app import create_app
from app.extensions import db
from app.tools.database import create_tables
from tests.factories import RecipeFactory


class BaseTest(TestCase):

    def create_app(self):
        """
        Creates the test app
        """
        self.app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': 'sqlite://'
        })
        self.app.config['TESTING'] = True
        self.header = {'Content-Type': 'application/json'}
        return self.app

    def setUp(self):
        with self.app.app_context():
            create_tables(db)

    def create_recipe(self, **kwargs):
        """
        Creates a test recipe with some basic data
        :param balance:
        :param transactions:
        :param kwargs:
        :return: Account object
        """
        recipe = RecipeFactory(
            **kwargs
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe
