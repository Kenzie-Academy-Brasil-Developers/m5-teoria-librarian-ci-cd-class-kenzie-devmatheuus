import ipdb
from librarians.serializers import RegisterSerializer
from rest_framework import serializers

from .models import Book, BookStatus


class BookSerializerOld(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    published_date = serializers.DateField()
    status = serializers.ChoiceField(
        choices=BookStatus.choices, default=BookStatus.DEFAULT
    )
    isbn = serializers.CharField(max_length=13)

    librarian = RegisterSerializer(read_only=True)

    def validate_isbn(self, isbn: str) -> str:
        if Book.objects.filter(isbn=isbn).exists():
            raise serializers.ValidationError("isbn already registered")

        return isbn

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
