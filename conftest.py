import pytest
from aiohttp import web


async def previous(request):
    """Получение запроса."""
    if request.method == 'POST':
        request.app['message'] = (await request.post())['message']
        return web.Response(body=b'thanks for the data')
    return web.Response(
        body='message: {}'.format(request.app['message']).encode('utf-8'))


@pytest.fixture
def cli(loop, aiohttp_client):
    """Клиент."""
    app = web.Application()
    app.router.add_post('/', previous)
    return loop.run_until_complete(aiohttp_client(app))