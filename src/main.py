from json import loads, JSONDecodeError
import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

@app.get("/")
@app.post("/")
async def echo_reply(request: Request) -> HTMLResponse:
    if request.method == "POST":
        return await request.body()
    html_response = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_response, status_code=200)

class ServiceRequestParser(BaseModel):
    headers: Dict[str, Any] = {}
    cookies: Dict[str, Any] = {}
    method: str
    body: Dict[str, Any] = {}

@app.get("/request")
@app.post("/request")
async def request_parser(request: Request) -> ServiceRequestParser:
    body = {}
    try:
        body = loads(await request.body())
    except JSONDecodeError:
        logging.info("Body is empty")
    return ServiceRequestParser(
        headers=request.headers,
        cookies=request.cookies,
        method=request.method,
        body=body
    )

