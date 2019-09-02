import pytest


@pytest.mark.run(after="test_db")
async def test_home_page_is_up(test_cli):
    response = await test_cli.get("/")
    assert response.status == 200


@pytest.mark.run(after="test_db")
async def test_download_favicon(test_cli):
    response = await test_cli.get("/favicon.ico")
    assert response.status == 200


@pytest.mark.run(after="test_db")
async def test_download_logo(test_cli):
    response = await test_cli.get("/static/img/logo.png")
    assert response.status == 200
