import secrets

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.cache import cache


class Token:
    @staticmethod
    def encrypt_token(token: str, encryption_key: bytes) -> bytes:
        cipher = Fernet(encryption_key)
        return cipher.encrypt(token.encode())

    @staticmethod
    def decrypt_token(encrypted_token: bytes, encryption_key: bytes) -> str:
        try:
            cipher = Fernet(encryption_key)
            return cipher.decrypt(encrypted_token).decode()
        except InvalidToken:
            return ""

    @staticmethod
    def generate_cache_key(token: str) -> str:
        return f"token:{token}"

    def create(self, user) -> str:
        token = secrets.token_urlsafe(32)
        cache.set(
            self.generate_cache_key(token),
            user.id,
            timeout=settings.TOKEN_EXPIRY_SEC,
        )

        return self.encrypt_token(token, settings.ENCRYPTION_KEY).decode()

    def get_user_id(self, encrypted_token: str) -> int:
        token = self.decrypt_token(
            encrypted_token.encode(),
            settings.ENCRYPTION_KEY,
        )

        cache_key = self.generate_cache_key(token)
        return cache.get(cache_key)
