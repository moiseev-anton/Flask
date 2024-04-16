from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List
import uvicorn


app = FastAPI()


class Task(BaseModel):
    id: str
    title: str
    description: str
    status: bool = False


tasks = []
task_count = 0


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str = Path(..., title="Task ID")):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    global task_count
    task_count += 1
    task.id = task_count
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: Task):
    index = next((index for index, t in enumerate(tasks) if t.id == task_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[index] = task
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    index = next((index for index, t in enumerate(tasks) if t.id == task_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[index]
    return {"message": "Task deleted"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
