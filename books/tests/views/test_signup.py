from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from books.models.profile import Profile


class TestSignup(APITestCase):
    def test_create_user_for_valid_request(self):
        response = self.client.post(
            "/bookstack/signup/", data=make_user(), format="json", follow=True
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "username": "mahi",
                "first_name": "mahima",
                "last_name": "choudhary",
                "email": "mahi87mnit@x.in",
            },
        )
        user = User.objects.get(username=response.json()["username"])
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)

    def test_should_not_let_create_user_without_username(self):
        body = make_user()
        body.pop("username")
        response = self.client.post(
            "/bookstack/signup/", data=body, format="json", follow=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"username": ["This field is required."]})


def make_user(**kwargs):
    default_user = {
        "username": "mahi",
        "first_name": "mahima",
        "last_name": "choudhary",
        "email": "mahi87mnit@x.in",
        "password": "1234",
    }

    return default_user | dict(kwargs)
