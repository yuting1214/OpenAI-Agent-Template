import os
from dotenv import load_dotenv
from openai import DefaultAioHttpClient
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

_ = load_dotenv('.env')

model = OpenAIChatCompletionsModel(
    model="accounts/fireworks/models/gpt-oss-120b",
    openai_client=AsyncOpenAI(
        base_url="https://api.fireworks.ai/inference/v1",
        api_key=os.getenv("FIREWORKS_API_KEY"),
        http_client=DefaultAioHttpClient(),
    ),
)