from django.test import TestCase
from django.db.utils import IntegrityError
from pkg_resources import require
from books.models import Book
from djmoney.money import Money


# Create your tests here.
class TestBook(TestCase):
    def test_with_valid_values(self):
        book_args = make_book()
        book = Book.objects.create(**book_args)

        self.assertIsNotNone(book)

    def test_with_incorrect_data_type(self):
        with self.assertRaises(ValueError):
            book_args = make_book(publication_year="foobar")
            Book.objects.create(**book_args)

    def test_missing_author_raises_error(self):
        with self.assertRaises(IntegrityError):
            book_args = make_book(author=None)
            Book.objects.create(**book_args)

    def test_allows_notes_to_be_nullable(self):
        book_args = make_book(notes=None)
        book = Book.objects.create(**book_args)

        self.assertIsNotNone(book)


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
        "price": Money(1600, "INR"),
        "summary": "it is a fantasy fiction about dragons",
        "ownership_type": "E-Book",
        "notes": "some notes",
    }

    return default_book | dict(kwargs)
