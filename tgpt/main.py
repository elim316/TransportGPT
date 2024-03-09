from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Query(BaseModel):
    query: Optional[str]
    target_dest : str
    user_lat : float
    user_long : float

@app.post("/")
async def generate(query : Query):
    #TODO Add logic + integrate w model / frontend  
    pass