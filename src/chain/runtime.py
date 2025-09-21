import os
from typing import List, Dict, Any
from openai import AsyncOpenAI, DefaultAioHttpClient
from src.chain.prompt.example import SYSTEM_PROMPT

# Initialize OpenAI client with environment variable for API key
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=DefaultAioHttpClient(),
)

async def call_llm_api(
    messages: List[Dict[str, Any]],
    model: str = "gpt-4.1-mini",
    stream: bool = True,
) -> Any:
    """
    Call the OpenAI API with the provided conversation history.

    Args:
        messages (List[Dict[str, Any]]): List of message dicts in OpenAI format.
        model (str): Model name to use for completion.
        stream (bool): Whether to stream the response.

    Returns:
        Any: The API response object.
    """
    # Prepend the system prompt as a system message
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    response = await client.chat.completions.create(
        model=model,
        messages=full_messages,
        stream=stream,
    )
    return response