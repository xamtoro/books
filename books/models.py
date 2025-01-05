from .mongo_client import db
from datetime import datetime
from .utils import validate_object_id, convert_published_date, error_message

class Book:
    """
    Class to manage operations on the 'books' collection in MongoDB.
    Includes methods for creating, retrieving, updating, deleting, and
    calculating the average price of books.
    """
    collection = db['books']

    @staticmethod
    def create(data):
        """
        Inserts a new book document into the database.

        Args:
            data (dict): Book data to be inserted. Can include 'published_date'
                         as a date object.

        Returns:
            dict: Message confirming creation and the inserted book data.
        """
        data = convert_published_date(data)
        inserted_id = Book.collection.insert_one(data).inserted_id
        data["_id"] = str(inserted_id)

        return {
            "message": "The book was successfully created.",
            "book": data,
        }

    @staticmethod
    def get_all():
        """
        Retrieves all books from the database.

        Returns:
            list: List of all books with '_id' converted to string.
        """
        books = list(Book.collection.find({}))
        for book in books:
            book["_id"] = str(book["_id"])
        return books

    @staticmethod
    def get_one(book_id):
        """
        Retrieves a single book by its ID.

        Args:
            book_id (str): The ID of the book to retrieve.

        Returns:
            dict: The retrieved book data or an error message.
        """
        obj_id = validate_object_id(book_id)
        if not obj_id:
            return error_message("Invalid ID.")

        book = Book.collection.find_one({"_id": obj_id})
        if book:
            book["_id"] = str(book["_id"])
            return book
        return error_message(f"No book found with ID '{book_id}'.", 404)

    @staticmethod
    def update(book_id, data):
        """
        Updates a book by its ID.

        Args:
            book_id (str): The ID of the book to update.
            data (dict): The data to update.

        Returns:
            dict: Message confirming the update or an error message.
        """
        obj_id = validate_object_id(book_id)
        if not obj_id:
            return error_message("Invalid ID.")

        data = convert_published_date(data)
        result = Book.collection.update_one({"_id": obj_id}, {"$set": data})
        if result.matched_count:
            return {
                "message": "The book was successfully updated.",
                "updated_data": data,
            }
        return error_message(f"No book found with ID '{book_id}'.", 404)

    @staticmethod
    def delete(book_id):
        """
        Deletes a book by its ID.

        Args:
            book_id (str): The ID of the book to delete.

        Returns:
            dict: Message confirming deletion or an error message.
        """
        obj_id = validate_object_id(book_id)
        if not obj_id:
            return error_message(f"Invalid ID '{book_id}'.")

        result = Book.collection.delete_one({"_id": obj_id})
        if result.deleted_count > 0:
            return {"message": f"The book with ID '{book_id}' was deleted successfully."}
        return error_message(f"No book found with ID '{book_id}'.", 404)

    @staticmethod
    def get_average_price_by_year(year):
        """
        Calculates the average price of books published in a specific year.

        Args:
            year (int): The year for which to calculate the average price.

        Returns:
            dict: The average price or a message if no books are found.
        """
        try:
            pipeline = [
                {
                    "$match": {
                        "published_date": {
                            "$gte": datetime(year, 1, 1),
                            "$lt": datetime(year + 1, 1, 1),
                        }
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "average_price": {"$avg": "$price"},
                    }
                },
            ]

            result = list(Book.collection.aggregate(pipeline))
            if result:
                return {"average_price": result[0]["average_price"]}
            return {"message": "No books found for the given year."}
        except Exception as e:
            return {"error": str(e), "status": 500}
