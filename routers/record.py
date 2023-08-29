from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from database import DB_ANNOTATED
from models import Records
from .auth import VERIFY_TOKEN


router = APIRouter(
    tags=['record'],
    prefix='/record'
)

class RequestDeleteRecord(BaseModel):
    record_id : int
    class Config:
        json_schema_extra={
			'example':{
            'record_id':'record_id to be deleted'
			}
		}

class RequestCreateRecord(BaseModel):
    title : str = Field(max_length=20) 
    class Config:
        json_schema_extra={
			'example':{
            'title':'Title Of Record'
			}
		}

class ResponseRecord(BaseModel):
    msg : str
    title : str
    record_id : int


class ResponseRecordsList(BaseModel):
    msg : str
    record_list : list
    count : int


@router.get("/",status_code=status.HTTP_200_OK,response_model=ResponseRecordsList)
def get_self_records(session : DB_ANNOTATED , applyer : VERIFY_TOKEN):
    user_id = applyer.get("id")
    
    data = [{"record_id":record.id , "title":record.title} for record in session.query(Records).filter( Records.user_id == user_id ).all()]
    
    return ResponseRecordsList(msg="success",record_list=data,count=len(data))


@router.post("/create" ,status_code=status.HTTP_201_CREATED,response_model=ResponseRecord)
async def create_self_record(session:DB_ANNOTATED,applyer:VERIFY_TOKEN, request_data : RequestCreateRecord):
    user_id = applyer.get("id")
    data = Records( 
        title = request_data.title,
        user_id = user_id
     )
    session.add(data)
    session.commit()
    
    return ResponseRecord(msg='Record Created',title=data.title,record_id = data.id)

@router.delete("/delete" ,status_code=status.HTTP_202_ACCEPTED,response_model=ResponseRecord)
async def delete_record_by_id(record_id:str,session:DB_ANNOTATED,applyer:VERIFY_TOKEN):

    user_id = applyer.get("id")
    
    record = session.query(Records).filter(Records.id == record_id).first()
    if record is not None:
        if record.user_id == user_id:
            session.delete(record)
            session.commit()
            return ResponseRecord(msg='Record Deleted',title=record.title,record_id = record.id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record Not Found")
        
