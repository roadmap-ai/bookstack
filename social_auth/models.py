import uuid

from django.conf import settings
from django.core.cache import cache


# Create your models here.
class Token:
    def __init__(self, user):
        self.user_id = user.id

    def generate(self):
        token = str(uuid.uuid4())
        cache.set(key=f"token:{token}", value=self.user_id, timeout=settings.TOKEN_EXPIRY_SEC)
        return token
