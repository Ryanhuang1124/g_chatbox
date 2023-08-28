from fastapi import FastAPI 
from database import engine
import models
from routers import auth,user,record,conversation

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(record.router)
app.include_router(conversation.router)