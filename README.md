# bookstore-backend
# Bookstore Management API

A RESTful API built with FastAPI for managing a bookstore with different user roles, book borrowing functionality, and role-based permissions.

## Project Overview

This application provides a backend API for a bookstore management system with three types of users:
- **Admin**: Can manage users and books
- **Librarian**: Can manage books for customers
- **Customer**: Can view borrowed books

## Features

- User authentication (register/login)
- Role-based access control
- Book management (add, edit, delete, list)
- Book borrowing system
- User management

## Tech Stack

- **Backend**: Python 3.13+ with FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Testing**: pytest

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/Novarroh/bookstore-backend
cd bookstore-backend
```

2. Create a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up database
```bash
# Create a .env file with your PostgreSQL credentials
echo "DATABASE_USER=postgres" > .env
echo "DATABASE_PASSWORD=yourpassword" >> .env
echo "DATABASE_HOST=localhost" >> .env
echo "DATABASE_PORT=5432" >> .env
echo "DATABASE_NAME=bookstore" >> .env
```

5. Initialize the database
```bash
python -m app.init_data
```

6. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000)  
API documentation is automatically available at [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

### Authentication
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login and get user details

### Users
- `GET /api/users/` - Get all users
- `PUT /api/users/{user_id}/role` - Update user role (admin only)

### Books
- `GET /api/books/` - Get all books

### Book Borrowings
- `POST /api/borrowings/` - Create a new borrowing record
- `GET /api/borrowings/user/{user_id}` - Get user's borrowing history
- `PUT /api/borrowings/{borrowing_id}/return` - Mark a book as returned

## Project Structure

```
bookstore-backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── users.py
│   │   │   ├── books.py
│   │   │   └── borrowings.py
│   ├── crud/
│   │   ├── user.py
│   │   ├── book.py
│   │   └── book_borrowing.py
│   ├── models/
│   │   ├── user.py
│   │   ├── book.py
│   │   └── book_borrowing.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── book.py
│   │   └── book_borrowing.py
│   ├── config.py
│   ├── database.py
│   └── init_data.py
├── tests/
│   ├── test_user_register.py
│   └── ...
├── main.py
├── .env
├── requirements.txt
└── README.md
```

## Testing

Run the tests with:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_user_register.py -v
```

## Default Users

The application is initialized with three default users:

- **Admin**: 
  - Email: admin@example.com
  - Password: admin123
