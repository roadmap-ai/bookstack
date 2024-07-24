from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from books.models.profile import Profile
from social_auth.clients import GoogleClient
from social_auth.models import Token
from social_auth.serializers import GoogleLoginCallbackSerializer


# Create your views here.
@api_view(["POST"])
def google_callback(request):
    serializers = GoogleLoginCallbackSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)

    code = serializers.validated_data["code"]
    code_verifier = serializers.validated_data["code_verifier"]
    token_response = GoogleClient.get_token_or_raise(code, code_verifier)
    user_details = GoogleClient.get_user_details_or_raise(token_response.access_token)

    user, created = User.objects.get_or_create(
        username=user_details.email,
        email=user_details.email,
        first_name=user_details.first_name,
        last_name=user_details.last_name,
    )
    if created:
        user.set_unusable_password()
        user.save()

    profile, _ = Profile.objects.get_or_create(user=user)

    token = Token(user=user).generate()

    return Response({"token": token.key})
