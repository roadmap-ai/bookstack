from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.exceptions import BookAlreadyExistInLibraryException
from books.models import ProfileLibrary
from books.permissions import IsOwner
from books.serializers.profile_library import ProfileLibrarySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsOwner])
def get_profile_library(request, profile_id):
    state = request.query_params.get("state")
    profile_libraries = ProfileLibrary.objects.filter(
        state=state, profile_id=profile_id
    )

    profile_libraries_serializer = ProfileLibrarySerializer(
        profile_libraries, many=True
    )

    return Response(profile_libraries_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwner])
def add_book_to_profile_library(request, profile_id, book_id):
    serializer = ProfileLibrarySerializer(data=request.data)
    serializer.initial_data["book_id"] = book_id
    serializer.initial_data["profile_id"] = profile_id

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        serializer.save()
    except IntegrityError:
        raise BookAlreadyExistInLibraryException

    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
