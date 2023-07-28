from starlette.requests import Request


class LowerCaseMiddleware:
    def __init__(self) -> None:
        self.DECODE_FORMAT = "latin-1"

    async def __call__(self, request: Request, call_next):
        raw = request.scope["query_string"].decode(self.DECODE_FORMAT).lower()
        request.scope["query_string"] = raw.encode(self.DECODE_FORMAT)

        path = request.scope["path"].lower()
        request.scope["path"] = path

        response = await call_next(request)
        return response
