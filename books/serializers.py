import ipdb
from django.core.validators import MaxValueValidator, MinValueValidator
from librarians.serializers import RegisterSerializer
from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    # children = serializers.IntegerField(
    #     validators=[MinValueValidator(0), MaxValueValidator(50)]
    # )

    class Meta:
        model = Author
        # fields = "__all__"
        fields = ["id", "name", "children"]
        # children tem que ser positivo entre 0 e 50
        extra_kwargs = {"children": {"min_value": 0, "max_value": 50}}


class BookSerializer(serializers.ModelSerializer):
    librarian = RegisterSerializer(read_only=True)
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "published_date",
            "isbn",
            "status",
            "librarian",
            "authors",
        ]

    def create(self, validated_data: dict) -> Book:
        authors_data: list[dict] = validated_data.pop("authors")

        book = Book.objects.create(**validated_data)

        for author_data in authors_data:
            author, is_created = Author.objects.get_or_create(**author_data)
            book.authors.add(author)

        return book
