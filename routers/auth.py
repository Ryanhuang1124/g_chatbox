from datetime import timedelta,datetime
from typing import Annotated
from jose import JWTError, jwt
from fastapi import APIRouter,Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette import status

from database import DB_ANNOTATED
from models import Users


router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)
        

def create_token(account:str, id:str, time_delta:timedelta):
    expire_time = datetime.utcnow() + time_delta
    payload = {
        "account":account,
        "id":id,
        "exp":expire_time
    }
    return jwt.encode(payload,key=SECRET_KEY,algorithm=ALGORITHM)

def verify_token( token: Annotated[str,Depends(OAuth2PasswordBearer(tokenUrl='auth/login'))] ):
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=ALGORITHM)
        account : str = payload.get('account')
        id : int = payload.get('id')
        if account is  None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't Validate User.")
        return {'account':account,'id':id}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't Validate User.")

VERIFY_TOKEN = Annotated[dict,Depends(verify_token)]
bcrypt = CryptContext(schemes = ['bcrypt'],deprecated = 'auto')
SECRET_KEY = "b8dc57542428ae80680f8dc03216a82f866e4ac846408e2c4b4335dbedb900d9"
ALGORITHM = "HS256"

class ResponseToken(BaseModel):
    access_token : str
    token_type : str


@router.post("/login", status_code=status.HTTP_200_OK,response_model=ResponseToken)
async def login_for_access_token(session : DB_ANNOTATED,body: Annotated[OAuth2PasswordRequestForm,Depends()]):
    
    user = session.query(Users).filter(Users.account==body.username).first()
    
    if bcrypt.verify(body.password, hash = user.password ):
        token = create_token(account=user.account, id=user.id,time_delta=timedelta(minutes=60))
        return ResponseToken(access_token=token,token_type="bearer")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't Validate User.")
