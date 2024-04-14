from django.contrib import admin

from books.models import Book, UserLibrary


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "isbn"]


class UserLibraryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "book"]
    list_display_links = ["user", "book"]


admin.site.register(Book, BookAdmin)
admin.site.register(UserLibrary, UserLibraryAdmin)
