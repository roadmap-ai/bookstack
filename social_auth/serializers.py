from rest_framework import serializers


class GoogleLoginCallbackSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
