import os

def generate_readme():
    readme_content = """# Todo Auth

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
```ini
sqlalchemy.url = postgresql://sushil:1234@localhost:5432/todo_auth_db
```

### Generate and Apply Migrations
```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## License
This project is licensed under the MIT License.
"""
    
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)
    
    print("README.md file has been generated successfully.")

if __name__ == "__main__":
    generate_readme()
