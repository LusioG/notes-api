# Notes API

Simple REST API for managing notes, built with Python and FastAPI.

This API allows users to create, read, update and delete notes.  
When the application starts, it automatically creates the required database tables for storing notes.

## Features

- Create notes
- Retrieve notes
- Update notes
- Delete notes
- Automatic database table creation
- RESTful endpoints

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Installation

Clone the repository:

```
git clone https://github.com/LusioG/notes-api.git
cd notes-api
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

## Example Endpoints

Get all notes

```
GET /notes
```

Create a note

```
POST /notes
```

Update a note

```
PUT /notes/{id}
```

Delete a note

```
DELETE /notes/{id}
```

## Project Structure

```
notes-api
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt
└── README.md
```

## Author

Luciano Ivan Grandjean