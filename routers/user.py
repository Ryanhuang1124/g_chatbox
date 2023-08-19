from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
from starlette import status

from models import Users
from database import DB_ANNOTATED
from .auth import bcrypt,VERIFY_TOKEN

router = APIRouter(
    prefix='/user',
    tags=['user']
)



class RequestUsers(BaseModel):
    name : str = Field(max_length=12)
    account : str = Field(max_length=12) 
    password : str = Field(max_length=12)
    class Config:
        json_schema_extra={
			'example':{
			'name':"Ryan",
			'account':'account',
            'password':'password'
			}
		}

class ResponseUsers(BaseModel):
    msg : str
    user_id : Optional[int]


@router.get("/",status_code=status.HTTP_200_OK)
async def get_self(session:DB_ANNOTATED, applyer : VERIFY_TOKEN):
    print("app:",applyer)

    if applyer is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User Unauthorized")

    data = session.query(Users).filter(Users.id == applyer.get('id')).first()
    return data


@router.post("/register" ,status_code=status.HTTP_201_CREATED,response_model=ResponseUsers)
async def create_user(session:DB_ANNOTATED, request_data : RequestUsers):
    data = Users( 
        name = request_data.name,
        account = request_data.account,
        password = bcrypt.hash(request_data.password)
     )
    session.add(data)
    session.commit()
    return ResponseUsers(msg='User Created',user_id=data.id)