from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

READONLY_API_KEY = os.getenv("API_KEY_READONLY")
FULL_ACCESS_API_KEY = os.getenv("API_KEY_FULL_ACCESS")

async def api_key_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
            return Response(status_code=200)

    open_paths = ["/docs", "/redoc", "/openapi.json"]

    # Allow access to docs and API schema
    if request.url.path in open_paths:
        return await call_next(request)

    api_key = request.headers.get("api_key")

    # If no API key is provided
    if not api_key:
        return JSONResponse(status_code=401, content={"detail": "Missing API key. Please provide an 'api_key' header!"})

    # If the request is GET, both keys are allowed
    if request.method == "GET" and api_key in [READONLY_API_KEY, FULL_ACCESS_API_KEY]:
        return await call_next(request)

    # If the request is modifying data (POST, PUT, DELETE), only the full-access key is valid
    if request.method in ["POST", "PUT", "DELETE"]:
        if api_key == FULL_ACCESS_API_KEY:
            return await call_next(request)
        else:
            return JSONResponse(status_code=403, content={"detail": "Insufficient permissions. This API key only allows read access!"})

    # If the API key is invalid
    return JSONResponse(status_code=403, content={"detail": "Invalid API key. Check your key or request access!"})
