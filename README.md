# library_manager
Library Management System CLI with SQLAlchemy, Alembic, and Click
# Library Management System CLI

This is a Python CLI application for managing a library's authors, publishers, and books using SQLAlchemy ORM, Alembic for migrations, and Click for command-line interactions, with a SQLite database.

## Setup
1. Install dependencies: `pipenv install`
2. Initialize Alembic migrations: `pipenv run alembic init alembic`
3. Update `alembic.ini` with `sqlalchemy.url = sqlite:///lib/db/library.db`
4. Edit `alembic/env.py` to include model imports (see below).
5. Generate and apply initial migration: `pipenv run alembic revision --autogenerate -m "Initial schema"` then `pipenv run alembic upgrade head`
6. Run the app: `pipenv run python lib/main.py`

## Features
- Create, delete, list, and find authors, publishers, and books via CLI commands.
- View related objects (e.g., books by author or publisher).
- Input validation and error handling.
- Database migrations with Alembic for schema changes.
- Persistent SQLite database in `lib/db/library.db`.

## Entities and Relationships
- **Author**: first_name, last_name, birth_year, nationality (one-to-many with Books).
- **Publisher**: name, founded_year, location, website (one-to-many with Books).
- **Book**: title, publication_year, genre, author_id, publisher_id.

## Project Structure
- `main.py`: Click-based CLI interface with commands for managing entities.
- `models.py`: SQLAlchemy model definitions and schema.
- `crud.py`: CRUD operations for database interactions.
- `alembic/`: Alembic migration environment (env.py, script.py.mako, versions/).
- `db/library.db`: SQLite database (generated at runtime).

## Alembic Setup
Edit `alembic/env.py` to include:
```python
from lib.models import Base, Author, Publisher, Book
target_metadata = Base.metadata