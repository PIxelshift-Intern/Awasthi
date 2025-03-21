# Todo Auth

A FastAPI-based authentication and task management system using PostgreSQL and Alembic for database migrations.

## Project Setup

### Initialize the Project
```sh
uv init todo_auth
```

### Install Dependencies
```sh
uv add fastapi --extra standard
uv add uvicorn sqlalchemy pydantic-settings psycopg2-binary passlib --extra bcrypt
uv add python-jose --extra cryptography
uv add alembic
```

### Alembic Init
```
alembic init alembic
```

## Folder Structure
```
todo_auth/
│── app/
│   ├── core/          # Configuration, security, utilities
|   |   ├── config.py
|   |   ├── auth.py
│   ├── database/      # DB models, connection, CRUD
|   |   ├── base.py 
|   |   ├── models.py
│   ├── routers/       # API routes (auth, todos, users)
|   |   ├── auth.py 
|   |   ├── todo.py 
|   |   ├── user.py 
│   ├── schemas/       # Pydantic schemas
|   |   ├── schemas.py
│   ├── __init__.py
│   ├── main.py        # Entry point for FastAPI
│── .venv/
│── pyproject.toml
│── uv.lock
│── README.md
│── .python-version
```

## Running the Project
```sh
uv run uvicorn app.main:app --port 8000
```

### Deploying Using Docker on local server

## Docker Image contains everything needed to run an application, including the application code, runtime, libraries, environment variables, and dependencies of the project.

Its features are 
>Immutable
>Portable
>Reusability

## Basic Workflows
Create a Dockerfile: This file contains the instructions to build your Docker image.
```Dockerfile
# Use Python 3.12-slim as the base image
FROM python:3.12-slim-bookworm

# Copy `uv` package manager from Astral's repository
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Copy the entire project into the container
ADD . /app

# Install dependencies using `uv`
RUN uv sync --frozen

# Expose the port FastAPI will run on
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```
Build the Docker Image: Using the docker build command, you create an image from the Dockerfile.

```sh
docker build -t my-fastapi-app .
```
Run a Docker Container: You use the image to create and run a container with the docker run command.
```sh
docker run -d -p 8000:8000 my-fastapi-app
```
Check if its running
```sh
docker ps
```
To check Terminal Logs 
```sh
docker logs -f 00c1d80afcf1  # Use container ID
```

## Automatically generated API documentation pages provided by FastAPI.
Swagger UI(http://localhost:8000/docs) 
ReDoc UI(http://localhost:8000/redoc)



## Database Migrations with Alembic

### Initialize Alembic
```sh
alembic init alembic
```

### Update Alembic Configuration
Edit `env.py` to include:
```python
from app.database.database import Base
target_metadata = Base.metadata
```

Update `alembic.ini`:
```python
sqlalchemy.url = postgresql://sushil:1234@localhost:5432/todo_auth_db
```

### Generate and Apply Migrations
```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Testing APIs

```ini
Create User

Endpoint: POST /users

Content-Type: application/json

Request Body (Raw JSON):
```

```sh
{
  "username": "testuser",
  "email" :"test@gmail.com",
  "password": "testpassword"
}
```

```ini
Authenticate User (Get Token)

Endpoint: POST /token

Content-Type: application/x-www-form-urlencoded

Request Body (Form Data):
```

```sh
username=testuser&password=testpassword
```


## All todo endpoints require authentication via Bearer token
```ini
They all require to have header like this 

Headers: 
```
```sh
Content-Type: application/json
Authorization: Bearer your_generated_token
```





```ini
Create a Todo (POST /todos)

Endpoint: POST /todos

Request Body (JSON - Raw):
```
```sh
{
  "title": "Complete API Testing",
  "description": "Test the create_todo API in Postman",
  "completed": false
}
```

Expected Response:
```sh
{
  "id": 1,
  "title": "Complete API Testing",
  "description": "Test the create_todo API in Postman",
  "completed": false,
  "owner_id": 123
}

```
```ini
Get All Todos (GET /todos)

Endpoint: GET /todos

Authorization: Bearer your_generated_token

Expected Response :
```
```sh
[
  {
    "id": 1,
    "title": "Complete API Testing",
    "description": "Test the create_todo API in Postman",
    "completed": false,
    "owner_id": 123,
    "is_active": true
  },
  {
    "id": 2,
    "title": "Write Documentation",
    "description": "Document all API endpoints",
    "completed": true,
    "owner_id": 123,
    "is_active": true
  }
]
```


```ini
Completely updates all fields.

Update Entire Todo (PUT /todos/{todo_id})

Endpoint: PUT /todos/1

Request Body (must include all fields from TodoCreate):
```
```sh
{
    "title": "Updated Title via PUT",
    "description": "Updated Description via PUT"
}
```


Response ( updated with default values if not provided):

```sh
{
    "id": 1,
    "title": "Updated Title via PUT",
    "description": "Updated Description via PUT",
    "owner_id": 1,
    "is_active": true  
}

```

### if there are no default values assigned in the TodoCreate model, and the client sends a PUT request without all the required fields (like owner_id or is_active), then the server should respond with a validation error, indicating that those fields are missing. The response would probably be a 422 error with details about the missing fields.



```ini
Partially updates only given fields.
Partially Update Todo (PATCH /todos/{todo_id})

Endpoint: PATCH /todos/1

Request Body (update only the description):
```
```sh
{
    "description": "Updated via PATCH"
}
```
Response (only description changes; title remain unchanged):
```sh
{
    "id": 1,
    "title": "Original Title",  // Unchanged
    "description": "Updated via PATCH",
    "owner_id": 1,
    "is_active": false          
}
```

```ini
Delete Todo (Soft Delete)

Endpoint: DELETE /todos/1

Expected Response:
```
```sh
{
  "message": "Todo marked as inactive"
}
```


## License
This project is licensed under the MIT License.
