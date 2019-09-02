import pytest
from bs4 import BeautifulSoup
from app.util import (
    email_invalid, email_required, password_required, wrong_email_or_password,
    success
)


@pytest.mark.run(after="test_db")
async def test_login_page_is_up(test_cli):
    response = await test_cli.get("/user/login")
    assert response.status == 200


@pytest.mark.run(after="test_db")
async def test_email_required(test_cli):
    response = await test_cli.post("/user/login", data={"email": "", "password": "c"})
    print(await response.text())
    assert email_required in await response.text()


@pytest.mark.run(after="test_db")
async def test_validate_email(test_cli):
    response = await test_cli.post("/user/login", data={"email": "a", "password": "c"})
    print(await response.text())
    assert email_invalid in await response.text()


@pytest.mark.run(after="test_db")
async def test_password_required(test_cli):
    response = await test_cli.post("/user/login", data={"email": "a@b.com", "password": ""})
    print(await response.text())
    assert password_required in await response.text()


@pytest.mark.run(after="test_db")
async def test_login_failed(test_cli):
    # get csrf token from the login form
    request = await test_cli.get("/user/login")
    print(await request.text())
    soup = BeautifulSoup(await request.text(), "html.parser")
    csrf = soup.find(id="csrf_token")["value"]
    assert csrf is not None

    # send post with csrf token
    response = await test_cli.post("/user/login",
                                   data={"csrf_token": csrf, "email": "a@abcdfe.com",
                                         "password": "a"})
    assert response.headers["Last-Status"] == wrong_email_or_password


@pytest.mark.run(after="test_db")
async def test_login_sucess(test_cli):
    # get csrf token from the login form
    request = await test_cli.get("/user/login")
    print(await request.text())
    soup = BeautifulSoup(await request.text(), "html.parser")
    csrf = soup.find(id="csrf_token")["value"]
    assert csrf is not None

    # send post with csrf token
    response = await test_cli.post("/user/login",
                                   data={"csrf_token": csrf, "email": "a@b.com",
                                         "password": "a"})
    assert response.headers["Last-Status"] == success

