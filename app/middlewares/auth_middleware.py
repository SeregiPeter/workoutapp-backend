from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

READONLY_API_KEY = os.getenv("API_KEY_READONLY")
FULL_ACCESS_API_KEY = os.getenv("API_KEY_FULL_ACCESS")

async def api_key_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    open_paths = ["/docs", "/redoc", "/openapi.json"]
    if request.url.path in open_paths:
        return await call_next(request)

    api_key = request.headers.get("api_key")
    if not api_key:
        response = JSONResponse(
            status_code=401,
            content={"detail": "Missing API key. Please provide an 'api_key' header!"},
        )
    elif request.method == "GET" and api_key in [READONLY_API_KEY, FULL_ACCESS_API_KEY]:
        return await call_next(request)
    elif request.method in ["POST", "PUT", "DELETE"] and api_key != FULL_ACCESS_API_KEY:
        response = JSONResponse(
            status_code=403,
            content={"detail": "Insufficient permissions. This API key only allows read access!"},
        )
    else:
        response = JSONResponse(
            status_code=403,
            content={"detail": "Invalid API key. Check your key or request access!"},
        )

    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

