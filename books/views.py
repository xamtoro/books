from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .utils import validate_object_id
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ViewSet):
    """
    A ViewSet to handle CRUD operations and additional actions
    for the Book model, integrated with MongoDB.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retrieves a paginated list of books.
        """
        books = Book.get_all()  # Retrieve all books as a list
        print("Authenticated user:", request.user)  # Debugging
        print("User ID:", request.user.id)
        # Configure the paginator
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of books per page
        result_page = paginator.paginate_queryset(books, request)

        # Return the paginated page
        return paginator.get_paginated_response(result_page)

    def create(self, request):
        """
        Creates a new book.

        Args:
            request: The HTTP request containing book data.

        Returns:
            Response: The created book data with HTTP 201 status,
                      or errors with HTTP 400 status.
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = Book.create(serializer.validated_data)
            return Response(book, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieves a single book by its ID.

        Args:
            request: The HTTP request.
            pk (str): The primary key of the book to retrieve.

        Returns:
            Response: The book data with HTTP 200 status,
                      or an error message with HTTP 404/400 status.
        """
        obj_id = validate_object_id(pk)
        if not obj_id:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        book = Book.get_one(obj_id)
        if not ("status" in book and book["status"] == 404):
            return Response(book, status=status.HTTP_200_OK)
        return Response(
            {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def update(self, request, pk=None):
        """
        Updates an existing book by its ID.

        Args:
            request: The HTTP request containing updated data.
            pk (str): The primary key of the book to update.

        Returns:
            Response: A success message with HTTP 200 status,
                      or errors with HTTP 404/400 status.
        """
        obj_id = validate_object_id(pk)
        if not obj_id:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        book = Book.get_one(obj_id)
        if "status" in book and book["status"] == 404:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            result = Book.update(obj_id, serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Deletes a book by its ID.

        Args:
            request: The HTTP request.
            pk (str): The primary key of the book to delete.

        Returns:
            Response: A success message with HTTP 200 status,
                      or an error with HTTP 404/400 status.
        """
        obj_id = validate_object_id(pk)
        if not obj_id:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        book = Book.get_one(obj_id)
        if "status" in book and book["status"] == 404:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        result = Book.delete(obj_id)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="average-price-by-year")
    def average_price_by_year(self, request):
        """
        Calculates the average price of books published in a specific year.

        Args:
            request: The HTTP request containing the 'year' query parameter.

        Returns:
            Response: The average price with HTTP 200 status,
                      or an error message with HTTP 400/404/500 status.
        """
        year = request.query_params.get("year")
        if not year or not year.isdigit():
            return Response(
                {"error": "A valid year is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        year = int(year)
        result = Book.get_average_price_by_year(year)
        if "error" in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif "message" in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)
