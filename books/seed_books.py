import os
import django

# Configura el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_management.settings")
django.setup()

from books.mongo_client import db

def seed_books():
    # Libros de prueba
    books = [
        {
            "title": "Moisés",
            "author": "Soy el mapa",
            "published_date": "1998-01-01",
            "genre": "Fiction",
            "price": 51.606,
        },
        {
            "title": "Book Two",
            "author": "Author Two",
            "published_date": "2000-05-20",
            "genre": "Adventure",
            "price": 34.99,
        },
        {
            "title": "Book Three",
            "author": "Author Three",
            "published_date": "2010-11-11",
            "genre": "Science Fiction",
            "price": 45.00,
        },
        {
            "title": "Book Four",
            "author": "Author Four",
            "published_date": "2015-06-23",
            "genre": "Mystery",
            "price": 25.50,
        },
        {
            "title": "Book Five",
            "author": "Author Five",
            "published_date": "2022-09-12",
            "genre": "Drama",
            "price": 30.00,
        },
    ]

    # Insertar los libros en la colección de MongoDB
    db.books.insert_many(books)
    print("Se insertaron datos de prueba en la colección de libros.")

if __name__ == "__main__":
    seed_books()
