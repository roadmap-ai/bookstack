from django.db import models


# Create your models here.
class Book(models.Model):
    class Meta:
        managed = False
        db_table = "Book"
        unique_together = (("title"), ("author"))

    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publication_year = models.IntegerField(null=True)
    genre = models.CharField(max_length=50)
    isbn = models.CharField(max_length=50, null=True)
    publisher = models.CharField(max_length=50, null=True)
    language = models.CharField(max_length=50)
    num_pages = models.IntegerField(null=True)
    summary = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
