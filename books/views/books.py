import json
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from books.forms import BookForm

from books.models.book import Book


class BooksView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        book_form = BookForm(data=data)

        if not book_form.is_valid():
            return Response(book_form.errors, status=400)

        book_form.save()
        return Response(book_form.data, status=201)

    def get(self, request):
        books = Book.objects.all()
        book_form = BookForm(books, many=True)
        return Response(book_form.data, status=200)


class BookView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

        book_form = BookForm(book)
        return Response(book_form.data, status=200)
