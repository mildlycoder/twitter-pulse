from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Todo
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test():
    return {"Ping" : "pong"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    else:
        HTTPException(404)

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    else:
        HTTPException(400)

@app.put("/api/todo/{title}/", response_model=Todo)
async def update_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    else:
        HTTPException(404)

@app.delete("/api/todo/{title}", response_model=Todo)
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Success"
    else:
        HTTPException(404)