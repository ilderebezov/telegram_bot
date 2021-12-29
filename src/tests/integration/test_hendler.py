import pytest
from aiohttp import web


async def test_post_value(cli):
    """Проверка запроса пользователя."""
    resp = await cli.post('/', data={'message': '/start'})
    assert resp.status == 200
    assert await resp.text() == 'thanks for the data'
    assert cli.server.app['message'] == '/start'


async def test_post_value(cli):
    """Проверка  get затроса."""
    resp = await cli.get('/get')
    assert resp.status == 404
