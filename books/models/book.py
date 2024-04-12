from django.db import models
from djmoney.models.fields import MoneyField


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=50)
    isbn = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    num_pages = models.IntegerField()
    price = MoneyField(max_digits=14, decimal_places=2)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
