from pydantic import BaseModel, field_validator
from fastapi import FastAPI,Query




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

@app.get("/users{user_id}")
def get_user(user_id : int ):
    return{
        "user_id":user_id
    }
@app.get("/notes")
def get_notes(page:int=Query(default=1,ge=1),limit:int=Query(default=1,ge=1, le=100)):
    return{
        "page":page, "limit":limit
    }