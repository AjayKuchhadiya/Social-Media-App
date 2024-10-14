

# Here using python dictionary to store the data instead of db


from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn 
from random import randrange

app = FastAPI()


class Posts(BaseModel):
    title : str
    content : str
    published : bool = True   # optional field in our schema ( if nott passed, it will default to True )
    rating: Optional[int] = Field(default=None, ge=1, le=5) # here is an optional value, It is default to none


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
    return {'message' : my_posts}

@app.get('/posts/{id}')
def get_post(id : int):
    result = next((post for post in my_posts if post['id'] == id), None)
    if not result : 
        raise HTTPException(status_code=404, detail= f"Item {id} not found")   # to raise HTTP Exception if the item not found in the database, otherwise would have got 200 status code. 
    return {'message' : result}

@app.post('/posts', status_code= status.HTTP_201_CREATED)   # here specifying the status code , otherwise gives 200 
def create_posts(post : Posts):
    post_dict = post.dict()
    post_dict['id'] = randrange(3, 1000000)
    my_posts.append(post_dict)

    return {'data' : post_dict}

@app.delete("/posts/{id}")
def delete_post(id: int): 
    index_to_delete = find_index_post(id)
    if index_to_delete == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with {id} does not exist")
    my_posts.pop(index_to_delete)
    return {"updated_posts" : my_posts}


@app.put("/posts/{id}")
def update_post(id: int, post : Posts): 
    index_to_update = find_index_post(id)
    if index_to_update == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with {id} does not exist")
    my_posts.pop(index_to_update)
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts.append(post_dict)
    return {"updated_posts" : my_posts}

if __name__ == '__main__': 
    uvicorn.run("main:app", host = '127.0.0.1', port = 8000, reload = True)




