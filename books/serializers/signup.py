from django.contrib.auth.models import User
from rest_framework import serializers

from books.models.profile import Profile


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        profile = Profile.objects.create(user=user)
        return user
