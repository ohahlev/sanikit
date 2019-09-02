import pytest

error_png = "error.png"


@pytest.mark.run(after="test_db")
async def test_error_page_is_up(test_cli):
    response = await test_cli.get("/test_error")
    assert response.status == 500


@pytest.mark.run(after="test_db")
async def test_check_for_error_png(test_cli):
    response = await test_cli.get("/test_error")
    assert error_png in await response.text()
