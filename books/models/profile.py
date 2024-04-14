from django.contrib.auth.models import User
from django.db import models

from books.models import Book, UserLibrary


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through=UserLibrary)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
