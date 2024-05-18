import json

from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from books.exceptions import BookAlreadyExistInLibraryException
from books.models import ProfileLibrary
from books.serializers.profile_library import ProfileLibrarySerializer


@api_view(["GET"])
def get_profile_library(request, profile_id):
    profile_library = ProfileLibrary.objects.all().filter(state="to_be_read")
    profile_serializer = ProfileLibrarySerializer(profile_library, many=True)
    return Response(profile_serializer.data, status=200)


@api_view(["POST"])
def add_book_to_profile_library(request, profile_id, book_id):
    data = json.loads(request.body)
    data["book_id"] = book_id
    data["profile_id"] = profile_id
    profile_serializer = ProfileLibrarySerializer(data=data)

    if not profile_serializer.is_valid():
        return Response(profile_serializer.errors, status=400)

    try:
        profile_serializer.save()
    except IntegrityError:
        raise BookAlreadyExistInLibraryException

    return Response(data=profile_serializer.data, status=201)
