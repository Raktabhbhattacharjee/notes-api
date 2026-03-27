    # -------------------------------------------------------------
# Note TO SELF
#
# `User` and `user` are NOT the same thing.
#
# User → SQLAlchemy ORM model (represents the "users" table)
# user → Pydantic request object containing client input
#
# Example:
# user.email → email sent in the request body
# User.id    → id column from the database table
#
# Creating a DB row:
# new_user = User(email=user.email)
# -------------------------------------------------------------
from fastapi import FastAPI
from routers import users, notes, auth
from database import engine
from models import Base

app = FastAPI()
app.include_router(users.router)
app.include_router(notes.router)
app.include_router(auth.router)

Base.metadata.create_all(bind=engine)