from rest_framework.exceptions import APIException


class UserAlreadyExistException(APIException):
    status_code = 400
    default_detail = "Username already taken. choose another"
    default_code = "username_unavailable"
