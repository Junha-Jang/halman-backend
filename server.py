import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ...existing code...

# Create FastAPI app
app = FastAPI()

# Database connection
def get_db():
    conn = sqlite3.connect('test.db')
    try:
        yield conn
    finally:
        conn.close()

# Initialize the database
def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Example route
@app.get("/")
def read_root():
    return {"Hello": "World"}

# ...existing code...

class Task(BaseModel):
    user_id: int
    task_name: str
    due_date: datetime
    status: bool = False

@app.post("/addtodo")
def add_todo(task: Task, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('INSERT INTO task (name, due_date, assigned_user, status) VALUES (?, ?, ?, ?)', 
                   (task.task_name, task.due_date, task.user_id, task.status))
    db.commit()
    return {"message": "Task added"}

@app.get("/gettodo")
def get_todo(user_id: Optional[int] = None, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    if user_id is not None:
        cursor.execute('SELECT * FROM task WHERE assigned_user = ?', (user_id,))
    else:
        cursor.execute('SELECT * FROM task')
    tasks = cursor.fetchall()
    return {"tasks": tasks}

# New endpoint to update the status of a task by ID
@app.put("/task/{task_id}/status")
def update_task_status(task_id: int, status: bool, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('UPDATE task SET status = ? WHERE id = ?', (status, task_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    db.commit()
    return {"message": "Task status updated"}

@app.delete("/task/{task_id}")
def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('DELETE FROM task WHERE id = ?', (task_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    db.commit()
    return {"message": "Task deleted"}

@app.get("/halmal")
def halmal(type: str):
    if(type == "character"):
        return {"message": "character"}
    return {"message": "tone"}