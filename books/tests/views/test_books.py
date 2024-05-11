from django.contrib.auth.models import User
from rest_framework.test import APITestCase

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


def make_user(**kwargs):
    default_user = {
        "username": "mahi",
        "first_name": "mahima",
        "last_name": "choudhary",
        "email": "mahi87mnit@x.in",
        "password": "1234",
    }

    return default_user | dict(kwargs)
