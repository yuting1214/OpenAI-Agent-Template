import aiohttp
import gradio as gr
from urllib.parse import urljoin
from src.app.core.init_settings import global_settings

def get_client_ip(request: gr.Request) -> str:
    """Get the client's IP address from the request."""
    if request is None:
        return "Client IP not available"
    elif "cf-connecting-ip" in request.headers:
        return request.headers["cf-connecting-ip"]
    elif "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"]
    else:
        return request.client.host

async def start_chat(user_id: str, mode: str) -> str:
    url = urljoin(global_settings.API_BASE_URL, "api/v1/chats/async")
    chat_data = {"user_id": user_id, "mode": mode} 

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=chat_data) as response:
            assert response.status == 200
            data = await response.json()
            return data["id"]