import pytest
from src.api.db.db import blue_chips_db
from src.api.db.db import read_db
from src.api.db.db import update_db

async def test_read_bleu_chips_db():
    """Тест данных голубых фишек."""
    test_value = await blue_chips_db('SBER')
    assert test_value['CLOSE'].max() != 0


async def test_read_db():
    """Тест данных из БД."""
    test_value = await read_db()
    assert test_value != 0


async def test_update_db():
    """Тест данных из БД."""
    test_value = await update_db()
    assert test_value != 0