from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from social_auth.models import Token


class SocialTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorise_header = request.META.get("HTTP_AUTHORIZATION")
        if authorise_header is None:
            return None

        token = authorise_header.split(" ")[1]
        user_id = Token().get_user_id(token)

        if user_id is None:
            raise AuthenticationFailed("User not logged in")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist")

        return user, None
