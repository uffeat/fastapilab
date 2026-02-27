import json
import os
from fastapi import FastAPI, Request, Response

app = FastAPI()
PROD = os.getenv("RENDER") == "true"
# TODO Remove  localhost from allowed_origins, once stuff works.
allowed_origins = set(["https://rolloh.vercel.app", "http://localhost"]) if PROD else set()


class get_key:
    def __init__(self):
        self._ = {}

    def __call__(self) -> str:
        """Returns uplink key."""
        if not self._.get("key"):
            if PROD:
                self._["key"] = os.getenv("UPLINK_KEY_CLIENT")
            else:
                from pathlib import Path

                self._["key"] = (
                    json.loads(
                        (Path.cwd() / "secrets.json").read_text(encoding="utf-8")
                    )
                )["development"]["client"]
        return self._["key"]


get_key = get_key()

##print("key:", get_key())  ##


def set_access(request: Request, response: Response) -> None:
    """Sets response header to control access."""
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


class Api:
    """Base class for targets."""

    def __init__(self, **_):
        self._ = _

    def __getitem__(self, key: str):
        if not hasattr(self, "_"):
            self._ = {}
        return self._.get(key)

    def __getattr__(self, key: str):
        return self._[key]


class api:
    """Decorator for targets."""

    registry = {}

    def __init__(self, **options):
        self.options = options

    def __call__(self, target):
        name = self.options.get("name")
        if not name:
            name = target.__name__
            self.options["name"] = name

        api.registry[name] = dict(target=target, options=self.options)

        return target


@api()
class echo(Api):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        print("meta:", self.meta)  ##
        print("options:", self.options)  ##

        print("args:", args)  ##
        print("kwargs:", kwargs)  ##

        return dict(args=args, kwargs=kwargs)


@api()
class foo(Api):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        return "FOO"


@app.post("/_/api/main")
async def main(
    request: Request, response: Response, name: str = None, submission: int = None
):
    """Delegates request to target."""
    set_access(request, response)
    # Retrieve target and related options
    registered = api.registry.get(name)
    target = registered["target"]
    options = registered["options"]
    # Create meta
    # TODO Remove key from meta, once stuff works
    meta = dict(name=name, submission=submission, key=get_key())
    # Extract args and kwargs from request body
    data = await request.json()
    args = data.get("args", tuple())
    kwargs = data.get("kwargs", dict())
    # Get target result
    # NOTE To guard against mutation copies of meta and options could be passed
    # into the target constructor. However, not doing so enables powerful patterns,
    # but do handle with care!
    result = target(meta=meta, options=options)(*args, **kwargs)
    # Return target result and meta
    return dict(meta=meta, result=result)
