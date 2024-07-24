import collections
import logging

import requests
from django.conf import settings
from rest_framework import status

logger = logging.getLogger(__name__)


class GoogleClient:

    TokenResponse = collections.namedtuple("TokenResponse", ["access_token"])

    def get_token_or_raise(code, code_verifier):
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "code_verifier": code_verifier,
            "client_id": settings.GOOGLE_AUTH_CLIENT_ID,
            "client_secret": "",
            "redirect_uri": settings.GOOGLE_AUTH_REDIRECT_URL,
            "grant_type": "authorization_code",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url=token_url, data=data, headers=headers)
        if not status.is_success(response.status_code):
            logger.error(
                f"failed to fetch token from google. status: {response.status_code}, body: {response.json()}"
            )
            response.raise_for_status()

        return GoogleClient.TokenResponse(access_token=response.json()["access_token"])

    UserInfoResponse = collections.namedtuple(
        "UserInfoResponse", ["email", "first_name", "last_name"]
    )

    def get_user_details_or_raise(access_token):
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url=user_info_url, headers=headers)

        if not status.is_success(response.status_code):
            logger.error(
                f"failed to fetch user details from google. status: {response.status_code}, body: {response.json()}"
            )
            response.raise_for_status()

        return GoogleClient.UserInfoResponse(
            email=response.json()["email"],
            first_name=response.json()["given_name"],
            last_name=response.json()["family_name"],
        )
