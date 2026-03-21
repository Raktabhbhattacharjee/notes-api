# Notes API

A clean, production-style REST API built with FastAPI and PostgreSQL.
Built as a reusable backend template with proper architecture patterns.

## Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Pydantic** — data validation
- **uv** — package manager

## Project Structure
```
notes-api/
├── main.py              # app init + router inclusion
├── database.py          # engine, sessionmaker, get_db
├── exceptions.py        # custom exceptions
├── models/              # SQLAlchemy models
│   ├── user.py
│   └── note.py
├── schemas/             # Pydantic request/response models
│   ├── user.py
│   └── note.py
├── routers/             # route handlers (thin layer)
│   ├── users.py
│   └── notes.py
└── services/            # business logic (DB queries)
    ├── user_service.py
    └── note_service.py
```

## Architecture

Follows a service layer pattern:
```
Client → Router → Service → Database
```

- **Routers** handle HTTP only — no DB logic
- **Services** handle business logic — no HTTP knowledge
- **Custom exceptions** act as contracts between layers
- **Pydantic schemas** validate all input/output

## API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | List all users (paginated) |
| GET | `/users/{user_id}` | Get a single user |

### Notes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes/` | Create a new note |
| GET | `/notes/` | List all notes (paginated + search) |
| GET | `/notes/{note_id}` | Get a single note |
| GET | `/notes/user/{user_id}` | Get all notes for a user |

## Features

- ✅ Service layer pattern (thin routers, logic in services)
- ✅ Custom exceptions (clean error contracts between layers)
- ✅ Pydantic validation (EmailStr, response models)
- ✅ Pagination (limit/offset)
- ✅ Search/filtering (case insensitive title search)
- ✅ Proper error handling (404, 409, 422)

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL
- uv

### Setup

1. Clone the repo:
```bash
git clone 
cd notes-api
```

2. Install dependencies:
```bash
uv sync
```

3. Create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/notes_db
```

4. Run the server:
```bash
uv run uvicorn main:app --reload
```

5. Visit docs:
```
http://localhost:8000/docs
```

## Error Handling

| Status Code | Meaning |
|-------------|---------|
| 201 | Resource created |
| 400 | Bad request |
| 404 | Resource not found |
| 409 | Conflict (duplicate email) |
| 422 | Validation failed |
| 500 | Internal server error |

## What I Learned Building This

- How to structure a FastAPI project properly
- Service layer pattern and separation of concerns
- Custom exceptions as contracts between layers
- Why routers should only speak HTTP
- ORM queries and their SQL equivalents
- Edge case handling (foreign key violations, duplicates)