from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase

from social_auth.models import Token


class TokenTestCase(TestCase):
    def setUp(self) -> None:
        return cache.clear()

    def tearDown(self) -> None:
        return cache.clear()

    def test_add_user_id_on_create_token(self):
        user = User.objects.create(username="test_user")
        token = Token().create(user)

        cache_value = Token().get_user_id(token)

        self.assertEqual(user.id, cache_value)

    def test_returns_none_if_token_malformed(self):
        cache_value = Token().get_user_id("foobar")
        self.assertIsNone(cache_value)

    def test_returns_none_if_token_is_not_found(self):
        user = User.objects.create(username="test_user")
        token = Token().create(user)

        cache.clear()
        cache_value = Token().get_user_id(token)

        self.assertIsNone(cache_value)

    @patch.object(cache, "set")
    def test_sets_timeout_on_token_creation(self, mock_cache_set):
        user = User.objects.create(username="test_user")
        token = Token().create(user)
        _, user_id_arg = mock_cache_set.call_args.args

        self.assertEqual(mock_cache_set.call_count, 1)
        self.assertEqual(user_id_arg, user.id)
        self.assertEqual(
            mock_cache_set.call_args.kwargs, {"timeout": settings.TOKEN_EXPIRY_SEC}
        )
