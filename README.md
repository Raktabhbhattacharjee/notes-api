# Notes API

A REST API built with FastAPI and PostgreSQL. Started this as a learning project to understand backend fundamentals — ended up with something I'd actually use as a template for future projects.

## Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Pydantic** — validation
- **passlib + bcrypt** — password hashing
- **python-jose** — JWT tokens
- **Alembic** — database migrations
- **uv** — package manager

## Project Structure

```
notes-api/
├── main.py              # app init + router registration
├── database.py          # DB connection, get_db dependency
├── exceptions.py        # custom exceptions
├── dependencies.py      # get_current_user() auth dependency
├── models/              # SQLAlchemy table definitions
│   ├── user.py
│   └── note.py
├── schemas/             # Pydantic request/response shapes
│   ├── user.py
│   └── note.py
├── routers/             # HTTP layer only, no business logic
│   ├── users.py
│   ├── notes.py
│   └── auth.py
└── services/            # all business logic lives here
    ├── user_service.py
    ├── note_service.py
    ├── auth_service.py
    └── token_service.py
```

## Architecture

```
Client → Router → Service → Database
```

Routers handle HTTP. Services handle logic. They don't know about each other's world — custom exceptions are the contract between them.

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login and get JWT token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | List users (paginated) |
| GET | `/users/{user_id}` | Get a single user |

### Notes (all protected — requires JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes/` | Create a note |
| GET | `/notes/` | List notes (paginated + search) |
| GET | `/notes/{note_id}` | Get a single note |
| GET | `/notes/user/{user_id}` | Get all notes for a user |

## Auth Flow

```
Signup  → password gets hashed → stored in DB
Login   → password verified → JWT token returned
Request → token sent in header → verified → access granted
```

Token lives in the `Authorization: Bearer <token>` header on every protected request.

## Features

- JWT authentication (login, token generation, protected endpoints)
- Password hashing with bcrypt (salted, one-way)
- Service layer pattern (thin routers, logic in services)
- Custom exceptions as contracts between layers
- Pydantic validation (EmailStr, response models)
- Pagination with metadata (total, has_next, has_prev)
- Search/filtering (case insensitive title search)
- Proper error handling (401, 404, 409, 422)
- Database migrations with Alembic

## Setup

### Prerequisites
- Python 3.13+
- PostgreSQL
- uv

### Steps

1. Clone the repo:
```bash
git clone <your-repo-url>
cd notes-api
```

2. Install dependencies:
```bash
uv sync
```

3. Create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/notes_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn main:app --reload
```

6. Visit docs:
```
http://localhost:8000/docs
```

## Error Codes

| Code | Meaning |
|------|---------|
| 201 | Created |
| 401 | Not authenticated or invalid token |
| 404 | Resource not found |
| 409 | Conflict (duplicate email) |
| 422 | Validation failed |

## What I Actually Learned

- How to structure a FastAPI project that doesn't fall apart as it grows
- Why business logic belongs in services, not routers
- How JWT auth works end to end — not just conceptually
- How bcrypt hashing and verification actually works under the hood
- Writing ORM queries by thinking in SQL first
- Using dependency injection to protect endpoints cleanly