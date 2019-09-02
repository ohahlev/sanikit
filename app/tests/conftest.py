import pytest
import app.config_test as config
from app.app import create_app


@pytest.yield_fixture
def test_app():
    app = create_app(config)
    yield app


@pytest.fixture
def test_cli(loop, test_app, sanic_client):
    return loop.run_until_complete(sanic_client(test_app))

