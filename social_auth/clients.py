import requests
from django.conf import settings


class GoogleClient:
    class TokenResponse:
        access_token: str

    def get_token_or_raise(code, code_verifier):
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "code_verifier": code_verifier,
            "client_id": settings.GOOGLE_AUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_AUTH_CLIENT_SECRET,
            "redirect_url": settings.GOOGLE_AUTH_REDIRECT_URL,
            "grant_type": "authorization_code",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url=token_url, data=data, headers=headers)
        response.raise_for_status()

        return GoogleClient.TokenResponse(access_token=response.json()["access_token"])

    class UserInfoResponse:
        email: str
        first_name: str
        last_name: str

    def get_user_details_or_raise(access_token):
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url=user_info_url, headers=headers)
        response.raise_for_status()

        return GoogleClient.UserInfoResponse(
            email=response.json()["email"],
            first_name=response.json()["given_name"],
            last_name=response.json()["family_name"],
        )
