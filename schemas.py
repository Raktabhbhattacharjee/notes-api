from datetime import datetime

from pydantic import BaseModel,EmailStr,ConfigDict


class UserCreate(BaseModel):
    email:EmailStr
    
    
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    model_config=ConfigDict(from_attributes=True)
    
    


class NoteCreate(BaseModel):
    title:str
    content:str
    owner_id:int
    ''' this is what the client sends and we have pydantic 
    to validate 
     it 
     '''



class NoteResponse(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime
    owner_id:int
    
    ''' this is what i want to show to my end user this is the response model so yea  
    '''
    model_config=ConfigDict(from_attributes=True)