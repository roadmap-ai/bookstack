import uuid

from django.conf import settings
from django.core.cache import cache


# Create your models here.
class Token:
    def create(self, user):
        token = str(uuid.uuid4())
        cache.set(
            key=f"token:{token}", value=user.id, timeout=settings.TOKEN_EXPIRY_SEC
        )
        return token

    def get_user_id(self, key):
        return cache.get(f"token:{key}")
