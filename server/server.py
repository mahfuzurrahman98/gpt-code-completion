from os import getenv

import openai
from fastapi import FastAPI, WebSocket
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
    # return a hello world response
    return {"message": "Hello World"}


@app.get("/review-codes")
async def review_codes():
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
            {'role': 'user', 'content': source_code},
            {'role': 'user', 'content': instructions}
        ]

        # Request gpt-3.5-turbo for chat completion
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=messages,
            stream=True
        )

        output = 'asdfsafasdf'
        # Send the response as a stream
        for chunk in response:
            if 'content' in chunk.choices[0].delta:
                cur_op_chunk = chunk.choices[0].delta['content']
                print(cur_op_chunk)
                # output += cur_op_chunk
                # await websocket.send_text(cur_op_chunk)

                # return StreamingResponse(
                #     content=cur_op_chunk,
                #     status_code=200,
                #     media_type="text/plain",
                # )
        return JSONResponse(content=output, status_code=200)
    except Exception as e:
        # print(e)
        return JSONResponse(content='sadfsadf', status_code=400)

    # await websocket.close()
    # return JSONResponse(content=output)


names = ["Name1", "Name2", "Name3", "Name4", ...]  # 5 million names


def generate_names():
    for i in range(50):
        yield 'name' + str(i)


@app.get("/get_names_chunked")
async def get_names_chunked():
    return StreamingResponse(generate_names())
