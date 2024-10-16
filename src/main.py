# main.py
from fastapi import FastAPI
import uvicorn 
import models
from database import engine
from routers import posts, users, auth
from config import setting

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {'message' : 'Hello World'}

if __name__ == '__main__':
    uvicorn.run("main:app", host=setting.database_hostname, port=setting.database_port, reload=True)
