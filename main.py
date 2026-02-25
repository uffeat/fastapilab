from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return '<h1>Hi</h1>'

@app.get("/ping")
def ping():
    return {"ping": 42}