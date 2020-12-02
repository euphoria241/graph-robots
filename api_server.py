from typing import Optional, List
from fastapi import FastAPI, Query


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

"""
http://localhost:8000/items/3?q=3,4,5,dgdg&q=3
{"item_id":3,"q":["3,4,5,dgdg","3"]}

matrix_id
position1
position2
speed1
speed2
"""
@app.get("/items/{item_id}")
def calculate(item_id: int, q: Optional[List[str]] = Query(None)):
    return {"item_id": item_id, "q": q}
