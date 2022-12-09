from fastapi import FastAPI, Request
from json import loads

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
    body = loads(await request.body())
    return {
        "headers": request.headers,
        "cookies": request.cookies,
        "method": request.method,
        "body": body
    }

