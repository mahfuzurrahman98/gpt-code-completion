from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import sys

# Getting OpenAI API Key

openai.api_key = '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'

# Defining the FastAPI app and metadata
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Defining error in case of 503 from OpenAI
error503 = "OpenAI server is busy, try again later"


def get_response_openai():
    try:
        source_code = '''
        def add(a, b):
            return a + b
        '''
        instructions = 'Do an in-depth code review, add documentation, and improve comments.'

        messages = [
            {'role': 'system', 'content': 'You are an experienced software engineer reviewing a random code snippet.'},
            {'role': 'user', 'content': source_code},
            {'role': 'user', 'content': instructions}
        ]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=messages,
            stream=True
        )
    except Exception as e:
        print("Error in creating campaigns from OpenAI:", str(e))
        raise HTTPException(503, detail=str(e))

    for chunk in response:
        current_content = chunk["choices"][0]["delta"].get("content", "")
        yield current_content
        # print(current_content)


@app.get("/review-code")
async def campaign():
    # get_response_openai()
    return StreamingResponse(get_response_openai(), media_type="text/event-stream")
