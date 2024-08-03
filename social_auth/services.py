from django.contrib.auth.models import User
from django.db import transaction

from books.models.profile import Profile
from social_auth.models import Token


class UserAuthService:
    def token_sign_in(code, code_verifier, authclient):
        token_response = authclient.get_token_or_raise(code, code_verifier)
        user_details = authclient.get_user_details_or_raise(token_response.access_token)

        user = UserAuthService._get_or_create_user_profile(user_details)
        token = Token().create(user=user)

        return token

    @transaction.atomic
    def _get_or_create_user_profile(user_details):
        user, created = User.objects.get_or_create(
            username=user_details.email,
            email=user_details.email,
            defaults={
                "first_name": user_details.first_name,
                "last_name": user_details.last_name,
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        return user
