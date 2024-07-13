from app.api.common.failures import Failures
from app.api.messages import monetary_field_error
from app.api.exceptions import RequestDataException


def validate_monetary_value(value, field_name):
    """Check if monetary value is negative.
    :param value:
    :param field_name: field name to be included in the error message
    :raises: RequestDataException
    :return:
    """
    if value < 0:
        response = Failures.inconsistent_information
        response['details'] = monetary_field_error.format(field_name)

        raise RequestDataException(response)
