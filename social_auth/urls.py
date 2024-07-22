from django.urls import path

from . import views

urlpatterns = [path("google/callback", views.google_callback)]
