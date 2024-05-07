from django.urls import path

from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("books/", views.BooksView.as_view()),
    path("books/<int:pk>/", views.BookView.as_view()),
]
