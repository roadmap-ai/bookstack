from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from books.models.book import Book
from books.tests.models.test_book import make_book


class TestBooksView(APITestCase):
    def test_post_with_valid_values(self):
        body = make_book()
        user = User.objects.create_user(**make_user())
        self.client.login(username="mahi", password="1234")
        response = self.client.post(
            "/bookstack/books/", data=body, format="json", follow=True
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "title": "Iron Flame",
                "author": "Rebbeca Yaroos",
                "publication_year": 2023,
                "genre": "Fiction",
                "language": "English",
            },
        )
        self.client.logout()

    def test_post_should_not_let_user_in_without_login(self):
        body = make_book()
        user = User.objects.create_user(**make_user())
        response = self.client.post(
            "/bookstack/books/", data=body, format="json", follow=True
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )

    def test_post_should_not_allow_when_username_is_not_present(self):
        body = make_book()
        body.pop("title")
        user = User.objects.create_user(**make_user())
        self.client.login(username="mahi", password="1234")
        response = self.client.post(
            "/bookstack/books/", data=body, format="json", follow=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"title": ["This field is required."]})
        self.client.logout()

    def test_get_with_valid_request(self):
        User.objects.create_user(**make_user())
        book1 = make_book()
        book2 = make_book(title="Fourth Wing")
        book3 = make_book(title="Ram", author="Amish")
        Book.objects.create(**book1)
        Book.objects.create(**book2)
        Book.objects.create(**book3)
        self.client.login(username="mahi", password="1234")
        response = self.client.get("/bookstack/books/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "title": "Iron Flame",
                    "author": "Rebbeca Yaroos",
                    "publication_year": 2023,
                    "genre": "Fiction",
                    "language": "English",
                },
                {
                    "title": "Fourth Wing",
                    "author": "Rebbeca Yaroos",
                    "publication_year": 2023,
                    "genre": "Fiction",
                    "language": "English",
                },
                {
                    "title": "Ram",
                    "author": "Amish",
                    "publication_year": 2023,
                    "genre": "Fiction",
                    "language": "English",
                },
            ],
        )
        self.client.logout()

    def test_get_should_not_let_user_in_without_login(self):
        User.objects.create_user(**make_user())
        Book.objects.create(**make_book())
        response = self.client.get("/bookstack/books/", follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )


class TestBookView(APITestCase):
    def test_get_for_valid_request(self):
        User.objects.create_user(**make_user())
        book1 = Book.objects.create(**make_book())
        book2 = Book.objects.create(**make_book(title="Fourth Wing"))
        self.client.login(username="mahi", password="1234")
        response1 = self.client.get(f"/bookstack/books/{book1.id}", follow=True)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(
            response1.json(),
            {
                "title": "Iron Flame",
                "author": "Rebbeca Yaroos",
                "publication_year": 2023,
                "genre": "Fiction",
                "language": "English",
            },
        )
        response2 = self.client.get(f"/bookstack/books/{book2.id}", follow=True)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            response2.json(),
            {
                "title": "Fourth Wing",
                "author": "Rebbeca Yaroos",
                "publication_year": 2023,
                "genre": "Fiction",
                "language": "English",
            },
        )

        self.client.logout()

    def test_get_should_not_let_user_in_without_login(self):
        User.objects.create_user(**make_user())
        book = Book.objects.create(**make_book())
        response = self.client.get(f"/bookstack/books/{book.id}", follow=True, pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )


def make_user(**kwargs):
    default_user = {
        "username": "mahi",
        "first_name": "mahima",
        "last_name": "choudhary",
        "email": "mahi87mnit@x.in",
        "password": "1234",
    }

    return default_user | dict(kwargs)
