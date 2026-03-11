from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = ""

# Create engine (connection manager)
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(bind=engine)
# create database session
# ↓
# give it to the endpoint
# ↓
# endpoint finishes
# ↓
# close database session



# Dependency function will be added next

def get_db():
    # creating a session for theis requerst 
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()