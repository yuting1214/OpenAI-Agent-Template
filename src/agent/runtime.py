import os
from agents import (
    Agent,
    set_tracing_export_api_key
)
from src.agent.models.fireworks import model as fireworks_model
from src.agent.models.openai import model as openai_model
from src.agent.models.settings import reasoning_model_settings, chat_model_settings
from src.agent.prompt.example import INSTRUCTIONS
from src.agent.tools.example import fetch_weather

set_tracing_export_api_key(os.getenv('OPENAI_API_KEY'))

# ai_agent = Agent(
#     name="Agent (Fireworks AI)",
#     model=fireworks_model,
#     model_settings=reasoning_model_settings,
#     instructions=INSTRUCTIONS,
#     tools=[fetch_weather],
# )

ai_agent = Agent(
    name="Agent (OpenAI)",
    model=openai_model,
    model_settings=chat_model_settings,
    instructions=INSTRUCTIONS,
    tools=[fetch_weather],
)