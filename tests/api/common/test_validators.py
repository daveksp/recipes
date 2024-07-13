from unittest import TestCase

from app.api import messages
from app.api.common.failures import Failures as CommonFailures
from app.api.common.validators import validate_monetary_value
from app.api.exceptions import RequestDataException


class ValidatorsTests(TestCase):
        

    def test_validate_monetary_value(self):
        """ validate_monetary_value: check if no exception is raised when
        positive value is provided.
        """
        # given
        field_name = 'my_monetary_field'
        valid_value = int("20")

        # when
        response = validate_monetary_value(valid_value, field_name)

        # then
        self.assertIsNone(response)

    def test_validate_monetary_value_negative_value(self):
        """ validate_monetary_value: check if exception is raised when
        negative value is provided.
        """
        # given
        field_name = 'my_monetary_field'
        valid_value = int("-20")
        expected_msg = messages.monetary_field_error.format(field_name)

        # when
        with self.assertRaises(RequestDataException) as error_context:
            validate_monetary_value(valid_value, field_name)

        # then
        exception = error_context.exception

        self.assertEqual(exception.errors['details'], expected_msg)
        exception.errors['details'] = None
        self.assertEqual(
            exception.errors, CommonFailures.inconsistent_information
        )
