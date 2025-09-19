from agents import ModelSettings

chat_model_settings = ModelSettings(
    parallel_tool_calls=True,
)

reasoning_model_settings = ModelSettings(
    parallel_tool_calls=True,
    reasoning_effort="medium",
)