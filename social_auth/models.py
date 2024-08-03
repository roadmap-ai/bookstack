import secrets

from django.conf import settings
from django.core.cache import cache
from cryptography.fernet import Fernet


class Token:
    def create(self, user):
        token = secrets.token_urlsafe(32)
        cache.set(
            key=f"token:{token}", value=user.id, timeout=settings.TOKEN_EXPIRY_SEC
        )

        enc_key = settings.ENCRYPTION_KEY
        f = Fernet(enc_key)
        enc_token = f.encrypt(token.encode()).decode()

        return enc_token

    def get_user_id(self, enc_token):

        enc_key = settings.ENCRYPTION_KEY
        f = Fernet(enc_key)
        token = f.decrypt(enc_token.encode()).decode()

        return cache.get(f"token:{token}")
