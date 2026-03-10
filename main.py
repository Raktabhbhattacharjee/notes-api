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
# creating a userreposne class 
class UserResponse(BaseModel):
    email:str
    
app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


# post request


@app.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate):
    return {"email": user.email}
