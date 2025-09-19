from agents import function_tool


@function_tool  
async def fetch_weather(location: str) -> str:
    
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return f"The weather in {location} is sunny"