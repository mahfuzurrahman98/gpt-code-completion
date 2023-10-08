from os import getenv


import openai
from fastapi import FastAPI, WebSocket, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()
# allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


def get_openai_response():
    try:
        openai.api_key = getenv('OPENAI_API_KEY')
        # Define the source code and instructions
        source_code = '''
        def add(a, b):
            return a + b
        '''
        instructions = 'Do an in-depth code review, add documentation, and improve comments.'

        # Create a list to store all the messages for context
        messages = [
            {'role': 'system', 'content': 'You are a experienced software engineer reviewing a random code snippet.'},
            {'role': 'user', 'content': source_code},
            {'role': 'user', 'content': instructions}
        ]

        # Request gpt-3.5-turbo for chat completion
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=messages,
            stream=True
        )
    except Exception as e:
        return JSONResponse(content='sadfsadf', status_code=400)

    try:
        # Send the response as a stream
        for chunk in response:
            if 'content' in chunk.choices[0].delta:
                cur_op_chunk = chunk.choices[0].delta['content']
                print(cur_op_chunk)
                yield cur_op_chunk
         
        # return JSONResponse(content=output, status_code=200)
    except Exception as e:
        return JSONResponse(content='sadfsadf', status_code=400)


@app.get("/review-code")
def review_codes():
    # return get_openai_response()
    return StreamingResponse(get_openai_response(), media_type='text/plain')