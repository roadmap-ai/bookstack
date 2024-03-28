from django.db import models


# Create your models here.
class Books(models.Model):
    class OwnershipType(models.TextChoices):
        e_book = "E-Book"
        audio_book = "Audio Book"
        owned_physical_book = "Owned Physical Book"
        borrowed_book = "Borrowed Book"

    book_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=50)
    isbn = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    num_pages = models.IntegerField()
    price = models.IntegerField()
    summary = models.TextField()
    created_at = models.DateField()
    ownership_type = models.CharField(
        choices=OwnershipType, default=OwnershipType.owned_physical_book, max_length=50
    )
    notes = models.TextField()
