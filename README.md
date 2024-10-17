# Student Rental Application

A Django web application for managing book rentals for students. The application allows users to rent books, view their rentals, and enables admins to manage books and rentals.

## Features

- User authentication using JWT.
- Integration with OpenLibrary API for fetching book details.
- Pagination and filtering capabilities for books and rentals.

## Requirements

- Python 3.11+
- Django 5.1.2
- Django REST Framework 
- SQLite (default database)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd student_rental

2. Build the Docker image:
   ```bash
   sudo docker-compose up --build 

3. Access the application at http://0.0.0.0:8000/api/schema/swagger-ui/

