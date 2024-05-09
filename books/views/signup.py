import json

from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from books.serializers.signup import SignupSerializer
from books.exceptions import UserAlreadyExistException


@api_view(["POST"])
def create_user(request):
    data = json.loads(request.body)
    signup_serializer = SignupSerializer(data=data)

    if not signup_serializer.is_valid():
        return Response(signup_serializer.errors, status=400)
    try:
        signup_serializer.save()
    except IntegrityError:
        raise UserAlreadyExistException
    return Response(signup_serializer.data, status=201)
