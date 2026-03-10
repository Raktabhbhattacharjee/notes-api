from pydantic import BaseModel, field_validator
from fastapi import FastAPI


class UserCreate(BaseModel):
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls,value):
        if '@' not in value:
            raise ValueError('Invalid Email')
        return value

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


# post request


@app.post("/users")
def create_user(user: UserCreate):
    return {"email": user.email}
