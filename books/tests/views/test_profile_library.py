from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from books.models import Book, Profile, ProfileLibrary
from books.tests.views.test_books import make_book
from books.tests.views.test_signup import make_user


class TestProfileLibraryView(APITestCase):
    def set_client_token(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="token " + token.key)

    def test_get_with_valid_values(self):
        user = User.objects.create_user(**make_user())
        book1 = Book.objects.create(**make_book())
        book2 = Book.objects.create(**make_book(title="Fourth Wing"))
        profile = Profile.objects.create(user_id=user.id)
        ProfileLibrary.objects.create(profile_id=profile.id, book_id=book1.id)
        ProfileLibrary.objects.create(profile_id=profile.id, book_id=book2.id)

        self.set_client_token(user)
        response = self.client.get(
            f"/bookstack/profile/{profile.id}/library/?state=to_be_read", follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "profile_id": profile.id,
                    "book_id": book1.id,
                    "ownership_type": "Owned Physical Book",
                    "price": None,
                    "notes": None,
                },
                {
                    "profile_id": profile.id,
                    "book_id": book2.id,
                    "ownership_type": "Owned Physical Book",
                    "price": None,
                    "notes": None,
                },
            ],
        )
