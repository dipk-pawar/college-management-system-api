from rest_framework.response import Response
from rest_framework import status
import sys
import traceback


class RequiredParameterValidator:
    def __init__(self, request, required_parameters, api_class_name):
        self.request = request
        self.required_parameters = required_parameters
        self.api_class_name = api_class_name.lower()

    def validate(self):
        if missing_parameters := [
            parameter
            for parameter in self.required_parameters
            if parameter not in self.request.data
        ]:
            return False, missing_parameters
        return True, None


def track_error(validate_api_parameters=None):
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            api_class_name = self.__class__.__name__
            try:
                if validate_api_parameters:
                    validator = RequiredParameterValidator(
                        request, validate_api_parameters, api_class_name
                    )
                    is_valid, missing_parameters = validator.validate()
                    if not is_valid:
                        return Response(
                            data={
                                "error": True,
                                "data": [],
                                "message": f"Missing parameters: {', '.join(missing_parameters)}",
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
                return view_func(self, request, *args, **kwargs)

            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])
                error_file, error_line, function_name, text = tb[-1]
                error_message = "An error occurred in file '{}' at line {}: '{}' in function '{}'".format(
                    error_file, error_line, str(e), function_name
                )
                if "/query.py" in error_message:
                    error_message = traceback.format_exc()

                return Response(
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                    data={
                        "error": True,
                        "data": [],
                        "message": str(e),
                        "exc_message": error_message,
                    },
                )

        return wrapper

    return decorator
