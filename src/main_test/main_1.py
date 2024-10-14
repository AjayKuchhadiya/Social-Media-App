
# Here using SQL database drivers to connect with database and using SQL queries. 


from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Posts(BaseModel):
    title : str
    content : str
    published : bool = True   # optional field in our schema ( if nott passed, it will default to True )
    # rating: Optional[int] = Field(default=None, ge=1, le=5) # here is an optional value, It is default to none

while True : 
    try : 
        conn = psycopg2.connect(database = 'fastapi_db', user = 'postgres', password = 'Ajay@123', 
                                port = 5432, host = 'localhost', cursor_factory= RealDictCursor )
        cursor = conn.cursor()
        print("database connection was sucessfull")
        break
    except Exception as e : 
        time.sleep(2)
        print('Connection to database failed with error : ', e)


my_posts = [{'title': 'title of post 1', 'content': 'Content of post 1', 'id': 1}, 
            {'title': 'title of post 2', 'content': 'Content of post 2', 'id': 2}
            ]


def find_index_post(id) : 
    for i, post in enumerate(my_posts): 
        if post['id'] == id: 
            return i


@app.get('/')
def root():
    return {'message' : 'Hii  world'}

@app.get('/posts')
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {'message' : posts}

@app.get('/posts/{id}')
def get_post(id : int):
    # result = next((post for post in my_posts if post['id'] == id), None)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post : 
        raise HTTPException(status_code=404, detail= f"Item {id} not found")   # to raise HTTP Exception if the item not found in the database, otherwise would have got 200 status code. 
    return {'message' : post}

@app.post('/posts', status_code= status.HTTP_201_CREATED)   # here specifying the status code , otherwise gives 200 
def create_posts(post : Posts):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    
    conn.commit()
    return {'data' : new_post}

@app.delete("/posts/{id}")
def delete_post(id: int): 
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()

    if deleted_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with {id} does not exist")

    conn.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post : Posts): 
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with {id} does not exist")
    
    conn.commit()

    return {"updated_posts" : updated_post}

if __name__ == '__main__': 
    uvicorn.run("main:app", host = '127.0.0.1', port = 8000, reload = True)