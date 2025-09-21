import os
from dotenv import load_dotenv
from openai import DefaultAioHttpClient
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

_ = load_dotenv('.env')

model = OpenAIChatCompletionsModel(
    model="gpt-4.1-mini-2025-04-14",
    openai_client=AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "placeholder-key-set-OPENAI_API_KEY-env-var"),
        http_client=DefaultAioHttpClient(),
    ),
)