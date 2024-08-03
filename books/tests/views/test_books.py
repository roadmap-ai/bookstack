from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APITestCase

from books.models.book import Book
from books.tests.models.test_book import make_book
from books.tests.views.test_signup import make_user
from social_auth.models import Token


class TestBookCreateView(APITestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def set_client_token(self, user_args=make_user()):
        user = User.objects.create_user(**user_args)
        token = Token().create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="token " + token)

    def test_post_with_valid_values(self):
        body = make_book()
        self.set_client_token()
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
        response = self.client.post(
            "/bookstack/books/", data=body, format="json", follow=True
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )

    def test_post_should_not_allow_when_title_is_not_present(self):
        body = make_book()
        body.pop("title")
        self.set_client_token()
        response = self.client.post(
            "/bookstack/books/", data=body, format="json", follow=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"title": ["This field is required."]})

    def test_get_with_valid_request(self):
        user_args = make_user()
        book1 = make_book()
        book2 = make_book(title="Fourth Wing")
        book3 = make_book(title="Ram", author="Amish")
        Book.objects.create(**book1)
        Book.objects.create(**book2)
        Book.objects.create(**book3)

        self.set_client_token(user_args)
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

    def test_get_should_not_let_user_in_without_login(self):
        response = self.client.get("/bookstack/books/", follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )
        User.objects.create_user(**make_user())
        Book.objects.create(**make_book())


class TestBookGetView(APITestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def set_client_token(self, user_args=make_user()):
        user = User.objects.create_user(**user_args)
        token = Token().create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="token " + token)

    def test_get_for_valid_request(self):
        user_args = make_user()
        book1 = Book.objects.create(**make_book())
        book2 = Book.objects.create(**make_book(title="Fourth Wing"))

        self.set_client_token(user_args)
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

    def test_get_should_not_let_user_in_without_login(self):
        book = Book.objects.create(**make_book())
        response = self.client.get(f"/bookstack/books/{book.id}", follow=True, pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )
