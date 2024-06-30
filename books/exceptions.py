from rest_framework.exceptions import APIException


class UserAlreadyExistException(APIException):
    status_code = 400
    default_detail = "Username already taken. choose another"
    default_code = "username_unavailable"


class BookAlreadyExistInLibraryException(APIException):
    status_code = 400
    default_detail = "Book is present in profile library"
    default_code = "already_present"
