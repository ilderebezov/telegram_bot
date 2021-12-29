import aiohttp_cors
from aiohttp.web_app import Application

from src.api.status.handler import post_handler
from src.api.status.handler import get_handler


def setup_routes(app: Application):
    """Настраивает эндпоинты сервиса с поддержкой CORS."""
    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        ),
    })
    cors.add(app.router.add_post('/', post_handler))
    cors.add(app.router.add_get('/get', get_handler))
