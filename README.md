```markdown
# FastAPI + MySQL CRUD

A simple FastAPI application using SQLAlchemy and Alembic to perform CRUD operations on a `User` resource, backed by a local MySQL database.

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Project Structure](#project-structure)  
3. [Environment Configuration](#environment-configuration)  
4. [Installation](#installation)  
5. [Database Setup & Migrations](#database-setup--migrations)  
6. [Running the Server](#running-the-server)  
7. [API Endpoints](#api-endpoints)  
8. [Testing](#testing)  
9. [Troubleshooting](#troubleshooting)  

---

## Prerequisites

- **Python 3.8+**  
- **MySQL Server** installed and running locally  
- A MySQL user (`fastapi_user`) with password (`admin!`) and a database named `fastapi_users`

---

## Project Structure

```

fastapi\_mysql\_crud/
│
├── alembic.ini
├── init\_db.sql
├── requirements.txt
├── README.md
├── .env
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│        └── <revision>\_create\_users\_table.py
│
└── app/
├── **init**.py
├── settings.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
└── main.py

```

- **init_db.sql**: SQL script to create the `fastapi_users` database and `fastapi_user` user.  
- **.env**: Environment variables (e.g. `DATABASE_URL`).  
- **alembic/**: Alembic configuration and migration scripts.  
- **app/**: Application code (FastAPI routes, SQLAlchemy models, Pydantic schemas, CRUD logic).

---

## Environment Configuration

Create a file named `.env` in the project root with the following content:

```

DATABASE\_URL=mysql+pymysql://fastapi\_user\:admin!@localhost:3306/fastapi\_users

````

> **Security Note**:  
> - Never commit `.env` to version control. Add it to `.gitignore`.

---

## Installation

1. **Clone or copy** this repository to your local machine.  
2. **Change into** the project directory:
   ```bash
   cd /d D:\ananth\prodigy\backend\task2
````

3. **Create & activate** a virtual environment:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   # source .venv/bin/activate
   ```
4. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Database Setup & Migrations

### 1. Create Database & User

Use MySQL Workbench or MySQL Shell to execute:

```sql
CREATE DATABASE IF NOT EXISTS fastapi_users
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'fastapi_user'@'localhost' IDENTIFIED BY 'admin!';
ALTER USER 'fastapi_user'@'localhost' IDENTIFIED BY 'admin!';

GRANT ALL PRIVILEGES ON fastapi_users.* TO 'fastapi_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Configure Alembic

1. If not already initialized, run:

   ```bash
   alembic init alembic
   ```
2. Edit `alembic/env.py` so it includes:

   ```python
   import sys, os
   from logging.config import fileConfig
   from sqlalchemy import engine_from_config, pool
   from alembic import context

   sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
   from app.settings import settings
   from app.database import Base

   config = context.config
   config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
   fileConfig(config.config_file_name)
   target_metadata = Base.metadata

   def run_migrations_offline():
       url = config.get_main_option("sqlalchemy.url")
       context.configure(
           url=url,
           target_metadata=target_metadata,
           literal_binds=True,
           dialect_opts={"paramstyle": "named"},
       )
       with context.begin_transaction():
           context.run_migrations()

   def run_migrations_online():
       connectable = engine_from_config(
           config.get_section(config.config_ini_section),
           prefix="sqlalchemy.",
           poolclass=pool.NullPool,
       )
       with connectable.connect() as connection:
           context.configure(connection=connection, target_metadata=target_metadata)
           with context.begin_transaction():
               context.run_migrations()

   if context.is_offline_mode():
       run_migrations_offline()
   else:
       run_migrations_online()
   ```

### 3. Generate & Apply Migrations

From the project root:

```bash
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

Verify in MySQL Workbench:

```sql
USE fastapi_users;
SHOW TABLES;
```

You should see:

```
+----------------------+
| Tables_in_fastapi_users |
+----------------------+
| users                |
+----------------------+
```

---

## Running the Server

```bash
uvicorn app.main:app --reload
```

* The server runs at `http://127.0.0.1:8000`.
* Interactive docs:

  * Swagger UI → `http://127.0.0.1:8000/docs`
  * ReDoc → `http://127.0.0.1:8000/redoc`

---

## API Endpoints

### 1. Create User

```
POST /users
```

* **Body** (JSON):

  ```json
  {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
  }
  ```
* **Response**: `201 Created`

  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
  }
  ```

### 2. List All Users

```
GET /users?skip=0&limit=100
```

* **Response**: `200 OK`

  ```json
  [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Alice",
      "email": "alice@example.com",
      "age": 30
    }
  ]
  ```

### 3. Get One User

```
GET /users/{user_id}
```

* **Response**: `200 OK`

  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
  }
  ```

### 4. Update User

```
PUT /users/{user_id}
```

* **Body** (JSON; any subset of fields):

  ```json
  {
    "age": 31
  }
  ```
* **Response**: `200 OK`

  ```json
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Alice",
    "email": "alice@example.com",
    "age": 31
  }
  ```

### 5. Delete User

```
DELETE /users/{user_id}
```

* **Response**: `204 No Content`

---

## Testing

### Postman

1. **Create a collection** (e.g., “FastAPI Users”).
2. **Add requests** for each endpoint (POST, GET, PUT, DELETE).
3. **Send** and verify responses.

### curl (Windows)

```bat
# Create a user
curl -X POST "http://127.0.0.1:8000/users" ^
     -H "Content-Type: application/json" ^
     -d "{\"name\":\"Alice\",\"email\":\"alice@example.com\",\"age\":30}"

# List users
curl "http://127.0.0.1:8000/users?skip=0&limit=10"

# Get one user
curl "http://127.0.0.1:8000/users/550e8400-e29b-41d4-a716-446655440000"

# Update a user
curl -X PUT "http://127.0.0.1:8000/users/550e8400-e29b-41d4-a716-446655440000" ^
     -H "Content-Type: application/json" ^
     -d "{\"age\":31}"

# Delete a user
curl -X DELETE "http://127.0.0.1:8000/users/550e8400-e29b-41d4-a716-446655440000"
```

---

## Troubleshooting

1. **“Table ‘fastapi\_users.users’ doesn’t exist”**

   * Run `alembic upgrade head`.
   * Confirm in MySQL Workbench that `users` table exists.

2. **Access denied for `fastapi_user`**

   * In MySQL, run:

     ```sql
     ALTER USER 'fastapi_user'@'localhost' IDENTIFIED BY 'admin!';
     GRANT ALL PRIVILEGES ON fastapi_users.* TO 'fastapi_user'@'localhost';
     FLUSH PRIVILEGES;
     ```

3. **Field required (Pydantic V2)**

   * Ensure `.env` is in project root with correct `DATABASE_URL`.
   * `app/settings.py` must import `BaseSettings` from `pydantic-settings`.

4. **“ImportError: cannot import name ‘settings’”**

   * Check that `app/settings.py` contains:

     ```python
     from pydantic_settings import BaseSettings

     class Settings(BaseSettings):
         DATABASE_URL: str
         class Config:
             env_file = ".env"
             env_file_encoding = "utf-8"

     settings = Settings()
     ```
   * Verify `app/__init__.py` exists (even if empty).

5. **Dependency Warnings**

   * Warning:

     ```
     UserWarning: Valid config keys have changed in V2:
     * 'orm_mode' has been renamed to 'from_attributes'
     ```
   * Safe to ignore; functionality remains.

