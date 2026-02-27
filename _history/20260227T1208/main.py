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


registry = dict()


class Api:
    def __init__(self, **_):
        self._ = _

    def __getitem__(self, key: str):
        if not hasattr(self, "_"):
            self._ = {}
        return self._.get(key)

    def __getattr__(self, key: str):
        return self._[key]

    @property
    def meta(self) -> dict:
        return self["meta"]


class api:
    def __init__(self, **meta):
        self.meta = meta

    def __call__(self, target):

        ##print("target:", target)  ##

        name = self.meta.get("name")
        if not name:
            name = target.__name__
            self.meta["name"] = name

        registry[name] = dict(target=target, meta=self.meta)

        ##print("Registered target with name:", name)  ##

        return target


@api()
class foo:
    def __init__(self, **meta):
        self.meta = meta

    def __call__(self, *args, **kwargs):
        return "FOO"


@app.post("/main/_/api")
async def main(
    request: Request, response: Response, name: str = None, submission: int = None
):
    """."""

    set_access(request, response)

    ##print("name:", name)  ##

    registered = registry.get(name)

    ##print("registered:", registered)  ##

    target = registered["target"]
    meta = registered["meta"]

    _meta = dict(submission=submission, **meta)

    data = await request.json()
    args = data.get("args", tuple())
    kwargs = data.get("kwargs", dict())

    result = target(**_meta)(*args, **kwargs)

    return dict(meta=_meta, result=result)


@app.post("/echo")
async def echo(request: Request, response: Response, submission: int = None):

    set_access(request, response)

    meta = dict(name=echo.__name__, submission=submission)
    result = await request.json()

    return dict(meta=meta, result=result)


@app.get("/ping")
async def ping(request: Request, response: Response, submission: int = None):

    set_access(request, response)

    meta = dict(name=ping.__name__, submission=submission)
    result = "PING"

    return dict(meta=meta, result=result)
