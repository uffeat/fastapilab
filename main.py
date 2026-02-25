import os
from typing import Optional
from fastapi import FastAPI, Header, Request, Response

app = FastAPI()
PROD = os.getenv("RENDER") == "true"
allowed_origins = set(["https://rolloh.vercel.app"]) if PROD else set()


def set_access(request: Request, response: Response) -> None:
    origin = request.headers.get("origin")
    if not origin:
        return
    if PROD:
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
    else:
        if origin.startswith("http://127.0.0.1") or origin.startswith(
            "http://localhost"
        ):
            response.headers["Access-Control-Allow-Origin"] = origin


@app.post("/echo")
async def echo(request: Request, response: Response):
    set_access(request, response)
    body = await request.json()
    return body


@app.get("/ping")
async def ping(request: Request, response: Response):
    set_access(request, response)
    return {"ping": 42}
