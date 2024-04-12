from django.test import TestCase
from books.models import Book, UserLibrary
from django.contrib.auth.models import User


class TestUserLibrary(TestCase):
    def test_with_valid_values(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        user_library = UserLibrary.objects.create(user=user, book=book)
        self.assertIsNotNone(user_library)

        self.assertEqual(user_library.user_id, user.id)
        self.assertEqual(user_library.book_id, book.id)


def make_book(**kwargs):

    default_book = {
        "title": "Iron Flame",
        "author": "Rebbeca Yaroos",
        "publication_year": 2023,
        "genre": "Fiction",
        "isbn": "7374952-1y48",
        "publisher": "test_publisher",
        "language": "English",
        "num_pages": 615,
        "summary": "it is a fantasy fiction about dragons",
    }

    return default_book | dict(kwargs)
