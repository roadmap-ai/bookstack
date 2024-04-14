from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from books.models import Book, UserLibrary
from books.tests.models.test_book import make_book


class TestUserLibrary(TestCase):
    def test_with_valid_values(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        user_library_args = make_user_library()
        user_library = UserLibrary.objects.create(
            user=user, book=book, **user_library_args
        )
        self.assertIsNotNone(user_library)

        self.assertEqual(user_library.user_id, user.id)
        self.assertEqual(user_library.book_id, book.id)

    def test_allows_notes_to_be_null(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        user_library_args = make_user_library(notes=None)
        user_library = UserLibrary.objects.create(
            user=user, book=book, **user_library_args
        )
        self.assertIsNotNone(user_library)

        self.assertEqual(user_library.user_id, user.id)
        self.assertEqual(user_library.book_id, book.id)

    def test_allows_price_to_be_null(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        user_library_args = make_user_library(price=None)
        user_library = UserLibrary.objects.create(
            user=user, book=book, **user_library_args
        )
        self.assertIsNotNone(user_library)

        self.assertEqual(user_library.user_id, user.id)
        self.assertEqual(user_library.book_id, book.id)

    def test_does_not_allows_ownership_type_to_be_null(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)
        user = User.objects.create(username="user", password="password")
        user_library_args = make_user_library(ownership_type=None)
        with self.assertRaisesMessage(
            IntegrityError, 'null value in column "ownership_type"'
        ):
            UserLibrary.objects.create(user=user, book=book, **user_library_args)


def make_user_library(**kwargs):

    default_user_library = {
        "price": 1500,
        "notes": "it is a fantasy fiction about dragons",
        "ownership_type": "Audio Book",
    }

    return default_user_library | dict(kwargs)
