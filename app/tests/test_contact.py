import pytest


@pytest.mark.run(after="test_db")
async def test_contact_page_is_up(test_cli):
    response = await test_cli.get("/contact")
    assert response.status == 200
