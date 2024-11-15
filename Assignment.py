from fastapi import Body, FastAPI, Form, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

user_db = {1: {"first_name": "johnson", "last_name":"richard", "Age":28, "email":"johnsonrichard1@gmail.com", "height":125}}

class User(BaseModel):
    firstName:str
    lastName:str
    Age:int
    Email:EmailStr
    Height:int

@app.middleware("http")
async def logger(request:Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    response.headers["X-Process-Time"] = str(duration)
    log_info = {"Duration": duration, "Request": request.method, "Status": response.status_code}
    print(log_info)

    return response

origins = ["http://localhost:8000"]

methods = ["POST"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user:Annotated[User, Form()]):
    for user_profile in user_db.values():
        if user_profile["email"] == user.Email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "user already exist")
    
    new_id = len(user_db.keys()) + 1  
    user_db[new_id] = user.model_dump()
        
    return "Profile created successfully"