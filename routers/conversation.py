from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import and_,DateTime
from starlette import status
from database import DB_ANNOTATED
from models import Conversations,Users,Records
from .auth import VERIFY_TOKEN

router = APIRouter(
    tags=['conversation'],
    prefix='/conversation'
)


def self_check(session,user_id,record_id):
    
    self_check = session.query(Records).filter(and_(Records.user_id == user_id, Records.id == record_id)).all()
    return self_check


class RequestDeleteConversation(BaseModel):
    conversation_id : int
    class Config:
        json_schema_extra={
			'example':{
            'record_id':'record_id to be deleted'
			}
		}

class RequestCreateConversation(BaseModel):
    message : str = Field(max_length=50)
    record_id : int 
    assistant : bool
    class Config:
        json_schema_extra={
			'example':{
            'record_id':0,
            'message':'Message content',
            'assistant':False
			}
		}

class ResponseConversation(BaseModel):
    msg : str
    message : str
    conversation_id : int
    date : str 


class ResponseConversationList(BaseModel):
    msg : str
    conversation_list : list
    count : int


@router.get("/",status_code=status.HTTP_200_OK,response_model=ResponseConversationList)
def get_conversations_by_record_id(record_id:int,session : DB_ANNOTATED , applyer : VERIFY_TOKEN):

    user_id = applyer.get("id")


    if self_check(session,user_id,record_id):
        data = [{"message_id":message.id , "content":message.message,"assistant":message.assistant,"date":message.date} for message in session.query(Conversations).filter( Conversations.record_id == record_id).all()]
        return ResponseConversationList(msg="success",conversation_list=data,count=len(data))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")


@router.post("/create" ,status_code=status.HTTP_201_CREATED,response_model=ResponseConversation)
async def create_conversation_by_record_id(session:DB_ANNOTATED,applyer:VERIFY_TOKEN, request_data : RequestCreateConversation):
    user_id = applyer.get("id")
    
    if self_check(session,user_id,request_data.record_id):
        data = Conversations(
            message = request_data.message,
            record_id = request_data.record_id,
            assistant = request_data.assistant
        )
        session.add(data)
        session.commit()
        
        return ResponseConversation(msg='Message Added',message=data.message, conversation_id = data.id, date=data.date.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    

# @router.get("/delete" ,status_code=status.HTTP_200_OK,response_model=ResponseRecord)
# async def delete_record_by_id(record_id:str,session:DB_ANNOTATED,applyer:VERIFY_TOKEN):

#     user_id = applyer.get("id")
    
#     record = session.query(Records).filter(Records.id == record_id).first()
#     if record.user_id == user_id:
#         session.delete(record)
#         session.commit()
#         return ResponseRecord(msg='Record Deleted',title=record.title,record_id = record.id)
#     else:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
