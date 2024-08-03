from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase

from books.models.profile import Profile
from social_auth.clients import GoogleClient
from social_auth.models import Token
from social_auth.services import UserAuthService


class TestUserAuthService(TestCase):
    def setUp(self):
        cache.clear()
        self.authclient = MagicMock(spec=GoogleClient)

    def tearDown(self):
        cache.clear()

    def test_create_new_user(self):
        self.authclient.get_token_or_raise.return_value = GoogleClient.TokenResponse(
            access_token="test_token"
        )
        self.authclient.get_user_details_or_raise.return_value = (
            GoogleClient.UserInfoResponse(
                email="test@example.com", first_name="Test", last_name="User"
            )
        )

        token = UserAuthService.token_sign_in(
            "test_code", "test_code_verifier", self.authclient
        )

        user = User.objects.get(username="test@example.com")
        profile = Profile.objects.get(user=user)
        self.assertEqual(user.id, Token().get_user_id(token))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertIsNotNone(profile)

    def test_existing_user(self):
        self.authclient.get_token_or_raise.return_value = GoogleClient.TokenResponse(
            access_token="test_token"
        )
        self.authclient.get_user_details_or_raise.return_value = (
            GoogleClient.UserInfoResponse(
                email="test1@example.com", first_name="Test", last_name="User"
            )
        )
        User.objects.create_user(
            username="test1@example.com",
            email="test1@example.com",
            password="test",
            first_name="Foo",
            last_name="bar",
        )

        token = UserAuthService.token_sign_in(
            "test_code", "test_code_verifier", self.authclient
        )

        user = User.objects.get(username="test1@example.com")
        profile = Profile.objects.get(user=user)
        self.assertEqual(user.id, Token().get_user_id(token))
        self.assertEqual(user.first_name, "Foo")
        self.assertEqual(user.last_name, "bar")
        self.assertIsNotNone(profile)

    def test_get_token_error(self):
        self.authclient.get_token_or_raise.side_effect = Exception("Test error")
        with self.assertRaises(Exception):
            UserAuthService.token_sign_in(
                "test_code", "test_code_verifier", self.authclient
            )

    def test_get_user_details_error(self):
        self.authclient.get_user_details_or_raise.side_effect = Exception("Test error")
        with self.assertRaises(Exception):
            UserAuthService.token_sign_in(
                "test_code", "test_code_verifier", self.authclient
            )

    @patch("social_auth.services.Profile.objects.get_or_create")
    def test_user_does_not_get_created_if_profile_creation_fails(
        self, mock_profile_create
    ):
        self.authclient.get_token_or_raise.return_value = GoogleClient.TokenResponse(
            access_token="test_token"
        )
        self.authclient.get_user_details_or_raise.return_value = (
            GoogleClient.UserInfoResponse(
                email="test@example.com", first_name="Test", last_name="User"
            )
        )
        mock_profile_create.side_effect = Exception("something failed")

        with self.assertRaises(Exception):
            UserAuthService.token_sign_in(
                "test_code", "test_code_verifier", self.authclient
            )

        self.assertIsNone(User.objects.filter(username="test@example.com").first())
