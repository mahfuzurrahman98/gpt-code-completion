from os import getenv

import openai


def review_code(source_code):
    # openai.api_key = getenv('OPENAI_API_KEY')
    openai.api_key = getenv('OPENAI_API_KEY')
    # Create a list to store all the messages for context
    messages = []

    # Add the source_code to the list
    messages.append({'role': 'user', 'content': source_code})

    # Add the prompt to modify the code
    instructions = 'Do a in depth proper code review, make the code documented, and put better comments where needed.'
    messages.append({'role': 'user', 'content': instructions})

    # Request gpt-3.5-turbo for chat completion
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=messages,
        stream=True
    )

    output = ''
    for chunk in response:
        if 'content' in chunk.choices[0].delta:
            output += chunk.choices[0].delta['content']
            print(chunk.choices[0].delta)

    return output


if __name__ == '__main__':
    output = review_code('''
    def add(a, b):
        return a + b
    ''')

    print(output)
