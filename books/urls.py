from django.urls import path

from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("books/", views.BooksView.as_view()),
    path("books/<int:pk>/", views.BookView.as_view()),
    path("signup/", views.create_user, name="create_user"),
    path(
        "profile/<int:profile_id>/library/",
        views.get_profile_library,
        name="get_profile_library",
    ),
    path(
        "profile/<int:profile_id>/book/<int:book_id>/",
        views.add_book_to_profile_library,
        name="add_book_to_profile_library",
    ),
]
