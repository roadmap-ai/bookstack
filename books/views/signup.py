from rest_framework import status
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from books.exceptions import UserAlreadyExistException
from books.serializers.signup import SignupSerializer


@api_view(["POST"])
def create_user(request):
    serializer = SignupSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        serializer.save()
    except IntegrityError:
        raise UserAlreadyExistException

    return Response(serializer.data, status=status.HTTP_201_CREATED)
