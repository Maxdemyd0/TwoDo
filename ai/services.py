from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from TwoDo import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_ai_response(user_message: str) -> str:
    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content="You are a productivity assistant.",
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=user_message,
        ),
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    return response.choices[0].message.content