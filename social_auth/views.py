from rest_framework.decorators import api_view
from rest_framework.response import Response

from social_auth.clients import GoogleClient
from social_auth.serializers import GoogleLoginCallbackSerializer
from social_auth.service import UserAuthService


# Create your views here.
@api_view(["POST"])
def google_callback(request):
    serializers = GoogleLoginCallbackSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)

    code = serializers.validated_data["code"]
    code_verifier = serializers.validated_data["code_verifier"]

    token = UserAuthService.token_sign_in(
        code=code, code_verifier=code_verifier, authclient=GoogleClient
    )

    return Response({"token": token})
