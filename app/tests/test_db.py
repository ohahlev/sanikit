import pytest


async def test_db(test_cli):
    response = await test_cli.get("/")
    assert response.status == 200
