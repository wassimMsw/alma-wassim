from typing import Union

from fastapi import FastAPI

from app.api import lead

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(lead.router)
