import json

from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models.book import Book
from books.serializers import BookSerializer


class BooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        book_serializer = BookSerializer(data=data)

        if not book_serializer.is_valid():
            return Response(book_serializer.errors, status=400)

        book_serializer.save()
        return Response(book_serializer.data, status=201)

    def get(self, request):
        books = Book.objects.all()
        book_serializer = BookSerializer(books, many=True)
        return Response(book_serializer.data, status=200)


class BookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

        book_serializer = BookSerializer(book)
        return Response(book_serializer.data, status=200)
