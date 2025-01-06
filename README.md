# Django Book Management API

This project is a simple **Django REST API** for managing books and user authentication. It uses **MongoDB** for storing books and Django's default SQLite database for user authentication and JSON Web Tokens (JWT).

---

## Features
- **User Authentication**: Register and login functionality using JWT.
- **Book Management**: CRUD operations for books stored in MongoDB.
- **API Endpoints**: Provides RESTful API endpoints for managing books and user authentication.

---

## Tech Stack
- **Python**: Programming language.
- **Django**: Web framework.
- **Django REST Framework (DRF)**: For building REST APIs.
- **MongoDB**: Database for storing book records.
- **SQLite**: Default database for Django, used for user authentication.

---

## Prerequisites

Before starting, ensure you have the following installed:
1. Python 3.8 or higher
2. MongoDB Server
3. pip (Python package manager)

---

## Installation

Follow these steps to set up and run the project:

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
- Django
- djangorestframework
- pymongo
- djangorestframework-simplejwt

### 4. Set Up MongoDB

1. Install MongoDB on your machine or use a cloud provider like MongoDB Atlas.
2. Start the MongoDB server.
3. Update the `settings.py` file with your MongoDB credentials:
   ```python
   MONGO_URI = "mongodb://localhost:27017/"
   MONGO_DB_NAME = "book_management"
   ```

### 5. Apply Migrations
Run the following command to set up the default SQLite database:
```bash
python manage.py migrate
```

### 6. Seed MongoDB with Sample Data
Run the `seed_books.py` script to populate the MongoDB database with sample books:
```bash
python -m books.seed_books
```

---

## Running the Application

### Development Server
Run the Django development server on port 8000:
```bash
python manage.py runserver
```
By default, the app will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

### **Authentication Endpoints**

#### 1. Register a User
**POST** `/auth/register/`  
Registers a new user in the system.

**Request Body**:
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```

**Responses**:
- **201 Created**: User successfully registered.
- **400 Bad Request**: Invalid input.

---

#### 2. Login
**POST** `/auth/login/`  
Authenticates a user and returns JWT tokens.

**Request Body**:
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```

**Responses**:
- **200 OK**: Returns `access` and `refresh` tokens for authentication.
- **401 Unauthorized**: Invalid credentials.

**Example Response**:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

### **Book Management Endpoints**

#### 1. List All Books
**GET** `/api/books/`  
Fetches a list of all books in the database.

**Responses**:
- **200 OK**: List of all books.
- **500 Internal Server Error**: Error while fetching data.

---

#### 2. Paginated Books
**GET** `/api/books/?page={number_page}`  
Fetches a paginated list of books.  

**Query Parameters**:
- **page** (Optional): The page number (default: 1).
- **page_size** (Optional): Number of items per page (default: 10).

**Responses**:
- **200 OK**: Returns the paginated book list.
- **400 Bad Request**: Invalid query parameters.

---

#### 3. Retrieve a Single Book
**GET** `/api/books/{id}/`  
Fetches details of a book by its ID.

**Path Parameter**:
- **id**: The unique identifier of the book.

**Responses**:
- **200 OK**: Book details.
- **404 Not Found**: Book not found.

---

#### 4. Add a New Book
**POST** `/api/books/`  
Adds a new book to the database.

**Request Body**:
```json
{
  "title": "Book Title",
  "author": "Author Name",
  "published_date": "2000-01-01",
  "genre": "Fiction",
  "price": 20.99
}
```

**Responses**:
- **201 Created**: Book successfully created.
- **400 Bad Request**: Invalid input.

---

#### 5. Update a Book
**PUT** `/api/books/{id}/`  
Updates the details of an existing book.

**Path Parameter**:
- **id**: The unique identifier of the book.

**Request Body**:
```json
{
  "title": "Updated Title",
  "author": "Updated Author",
  "price": 25.99,
  "published_date": "2001-02-01"
}
```

**Responses**:
- **200 OK**: Book successfully updated.
- **400 Bad Request**: Invalid input.
- **404 Not Found**: Book not found.

---

#### 6. Delete a Book
**DELETE** `/api/books/{id}/`  
Deletes a book from the database.

**Path Parameter**:
- **id**: The unique identifier of the book.

**Responses**:
- **200 OK**: Book successfully deleted.
- **404 Not Found**: Book not found.

---

#### 7. Average Price by Year
**GET** `/api/books/average-price-by-year?year={year}`  
Calculates the average price of books published in a specific year.

**Query Parameter**:
- **year**: (Required) The publication year to filter by.

**Responses**:
- **200 OK**: Returns the average price.
- **400 Bad Request**: Invalid year.
- **404 Not Found**: No books found for the specified year.

**Example Response**:
```json
{
  "average_price": 15.99
}
```

## Deployment Notes

To deploy on a cloud platform like AWS, follow these steps:
1. Use **Nginx** or **Apache** as a reverse proxy.
2. Serve the app using **Gunicorn**.
3. Bind the app to port 80 for direct DNS access.

### Example `systemd` Service File for Gunicorn:
```ini
[Unit]
Description=Gunicorn instance to serve Book Management API
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 book_management.wsgi:application

[Install]
WantedBy=multi-user.target
```

---

## Project Structure
```
BOOKS/
├── book_management/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── auth_views.py
│   ├── migrations/
│   ├── models.py
│   ├── mongo_client.py
│   ├── seed_books.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── env/
```

---

## Notes
- MongoDB is used exclusively for books data.
- JWT authentication relies on Django's default SQLite database.
- Ensure MongoDB is running before using the book-related endpoints.

For further details or issues, feel free to open an issue in the repository.

