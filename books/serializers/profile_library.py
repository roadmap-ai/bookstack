from rest_framework import serializers
from rest_framework_money_field import MoneyField

from books.models.profile_library import ProfileLibrary


class ProfileLibrarySerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    ownership_type = serializers.ChoiceField(
        choices=[
            ("e_book", "E-Book"),
            ("audio_book", "Audio Book"),
            ("owned_physical_book", "Owned Physical Book"),
            ("borrowed_book", "Borrowed Book"),
        ],
        required=False,
    )
    price = MoneyField(required=False)
    notes = serializers.CharField(required=False)

    def create(self, validated_data):
        profile_library = ProfileLibrary.objects.create(**validated_data)
        return profile_library
