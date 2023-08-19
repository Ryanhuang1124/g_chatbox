from database import Base
from sqlalchemy import ForeignKey,Column,Integer,String,Boolean,DateTime
from datetime import datetime

class Users(Base):
    __tablename__ = "users"
    id = Column("id",Integer,primary_key=True,index=True)
    name = Column("name",String)
    account = Column("account",String)
    password = Column("password",String)


class Records(Base):
    __tablename__ = "records"
    id = Column("id",Integer,primary_key=True,index=True)
    user_id = Column("user_id",Integer,ForeignKey("users.id"))
    title = Column("title",String)
    account = Column("account",String)
    password = Column("password",String)
    date = Column("date",DateTime,default=datetime.utcnow)

class Conversations(Base):
    __tablename__ = "conversations"
    id = Column("id",Integer,primary_key=True,index=True)
    record_id = Column("record_id",Integer,ForeignKey("records.id"))
    assistant = Column("assistant",Boolean)
    message = Column("message",String)
    date = Column("date",DateTime,default=datetime.utcnow)
