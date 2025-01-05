from rest_framework import serializers
import re


class BookSerializer(serializers.Serializer):
    """
    Serializer for the Book model.

    Provides validation and serialization for Book objects with the
    following fields:
        - title: The title of the book (string, max length 255).
        - author: The author of the book (string, max length 255).
        - published_date: The publication date of the book (date).
        - genre: The genre of the book (string, max length 100).
        - price: The price of the book (float).
        - _id: The unique identifier of the book (read-only, string).
    """
    title = serializers.CharField(
        max_length=255,
        help_text="The title of the book."
    )
    author = serializers.CharField(
        max_length=255,
        help_text="The author of the book."
    )
    published_date = serializers.DateField(
        help_text="The publication date of the book."
    )
    genre = serializers.CharField(
        max_length=100,
        help_text="The genre of the book."
    )
    price = serializers.FloatField(
        help_text="The price of the book."
    )
    # _id = serializers.CharField(
    #     read_only=True,
    #     help_text="The unique identifier of the book."
    # )
