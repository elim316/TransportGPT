from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from model import Generator
from data import Retrieval
from fastapi.responses import JSONResponse

app = FastAPI()
model = Generator()
retrieval = Retrieval()

class Query(BaseModel):
    user_lat : float
    user_long : float
    dest_lat : float
    dest_long : float

class GPTResponse(BaseModel):
    resp : str

@app.post("/", response_model=GPTResponse)
async def generate(query : Query) -> GPTResponse:
    context = retrieval.retrieve(
        user_lat=query.user_lat,
        user_long=query.user_long,
        dest_lat=query.dest_lat,
        dest_long=query.dest_long
    )
    return GPTResponse(resp=model.generate(context))