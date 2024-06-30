from rest_framework.permissions import BasePermission

from books.models import Profile


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        profile_id = view.kwargs.get("profile_id", None)
        return Profile.objects.filter(user_id=request.user.id, id=profile_id).exists()
