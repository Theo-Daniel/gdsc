from fastapi import HTTPException, FastAPI, status
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def root():
    return "hello"


Todos = {
    1: {
        "title": "complete micro DA",
        "completed": False,
    },
    2: {
        "title": "play cricket",
        "completed": False,
    }
}


class TodoItem(BaseModel):
    title: str
    completed: bool


@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todo_items(title: str = ""):
    results = {}
    if title != "" or title is not None:
        for id in Todos:
            if title in  Todos[id]['title']:
                results[id] = Todos[id]
    else:
        results = Todos
    return results


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo_item(todo_item: TodoItem):
    id = max(Todos)+1
    Todos[id] = todo_item.dict()
    return Todos[id]


@app.put("/todos/{id}", status_code=status.HTTP_200_OK)
def update_todo_item(id: int, todo_item: TodoItem):
    if id in Todos:
        Todos[id] = todo_item.dict()
        return Todos[id]
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found!")


@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_item(id: int):
    if id in Todos:
        Todos.pop(id)
        return
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found!")


@app.get("/todos/{id}", status_code=status.HTTP_200_OK)
def get_todo_item(id: int):
    if id in Todos:
        return Todos[id]
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found!")
