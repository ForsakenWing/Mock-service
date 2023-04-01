from fastapi import FastAPI, Request
from json import loads, JSONDecodeError
import logging

app = FastAPI()


@app.get('/')
@app.post('/')
async def echo_reply(request: Request):
    if request.method == 'POST':
        return await request.body()
    return {"message": "Hello, stranger"}


@app.get('/request')
@app.post('/request')
async def request_parser(request: Request):
    body = {}
    try:
        body = loads(await request.body())
    except JSONDecodeError:
        logging.info("Body is empty")
    return {
        "headers": request.headers,
        "cookies": request.cookies,
        "method": request.method,
        "body": body
    }

