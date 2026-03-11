# Task Boards API

REST API for managing task boards and tasks with user authentication.  
Built with Python and FastAPI.

The API allows users to register, authenticate, create boards and manage tasks inside those boards.

When the application starts, it automatically creates the required database tables defined in the models.

## Features

- User registration and login
- JWT authentication
- Create and manage boards
- Create, update and delete tasks
- View tasks inside boards
- Automatic database table creation
- RESTful API

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- JWT Authentication

## Installation

Clone the repository

```
git clone https://github.com/LusioG/notes-api.git
cd notes-api
```

Install dependencies

```
pip install -r requirements.txt
```

Run the server

```
uvicorn main:app --reload
```

The API will start at:

```
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides automatic interactive documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

Health check:

```
http://127.0.0.1:8000/health
```

---

# Authentication

Authentication uses JWT tokens.

Login endpoint returns a token that must be sent in protected requests.

Header example:

```
Authorization: Bearer <your_token>
```

---

# Endpoints

## General

```
GET /
```
Check if the API is running.

```
GET /health
```
Health status of the API.

---

# Users

Register a new user

```
POST /users/register
```

Login

```
POST /users/login
```

Get current authenticated user

```
GET /me
```

---

# Boards

Create a board

```
POST /boards
```

List user boards

```
GET /boards
```

Update board

```
PUT /boards/{board_id}
```

Delete board

```
DELETE /boards/{board_id}
```

Get board with its tasks

```
GET /boards/{id_board}
```

---

# Tasks

Create a task

```
POST /tasks
```

List tasks from a board

```
GET /tasks?board_id={board_id}
```

Get task by id

```
GET /tasks/{task_id}
```

Update task

```
PUT /tasks/{task_id}
```

Delete task

```
DELETE /tasks/{task_id}
```

---

# Project Structure

```
notes-api
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── security.py
├── deps.py
├── requirements.txt
└── README.md
```

---

# Author

Luciano Ivan Grandjean