from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField

from books.models import Book


class UserLibrary(models.Model):
    class OwnershipType(models.TextChoices):
        e_book = "E-Book"
        audio_book = "Audio Book"
        owned_physical_book = "Owned Physical Book"
        borrowed_book = "Borrowed Book"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    ownership_type = models.CharField(
        choices=OwnershipType, default=OwnershipType.owned_physical_book, max_length=50
    )
    notes = models.TextField(null=True)
    price = MoneyField(max_digits=14, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
