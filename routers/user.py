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
    name : str = Field(max_length=16)
    account : str = Field(max_length=32) 
    password : str = Field(max_length=16)
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
    user_name : str
    user_id : int

class ResponseUsersList(BaseModel):
    msg : str
    user_list : list
    count : int


@router.get("/",status_code=status.HTTP_200_OK,response_model=ResponseUsersList)
async def get_all_user(session:DB_ANNOTATED, applyer : VERIFY_TOKEN):

    if applyer is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User Unauthorized")
    
    data = [{'user_name': user.name, 'user_id': user.id} for user in session.query(Users).all()]

    return ResponseUsersList(msg="success",count= len(data),user_list=data)


@router.post("/register" ,status_code=status.HTTP_201_CREATED,response_model=ResponseUsers)
async def create_user(session:DB_ANNOTATED, request_data : RequestUsers):
    data = Users( 
        name = request_data.name,
        account = request_data.account,
        password = bcrypt.hash(request_data.password)
     )
    session.add(data)
    session.commit()
    
    return ResponseUsers(msg='User Created',user_name=data.name,user_id=data.id)