import asyncio
import pytest
from app.blueprints.product import service as job_service


@pytest.mark.run(after="test_db")
async def test_find_categories_in_page(test_cli):

    async def get_categories():
        cached = await job_service.get_cached_categories()
        if cached is None:
            cached = await job_service.get_db_categories()
        return cached

    async def get_home():
        return await test_cli.get("/")

    f1 = get_categories()
    f2 = get_home()

    categories, response = await asyncio.gather(f1, f2)

    assert response.status == 200

    async def assert_category(category):
        #print("category = {}".format(category["name"]))
        assert category["name"] in await response.text()

    all = await asyncio.gather(*[assert_category(category) for category in categories])
    assert all is not None


@pytest.mark.run(after="test_db")
async def test_find_tags_in_page(test_cli):

    async def get_tags():
        cached = await job_service.get_cached_tags()
        if cached is None:
            cached = await job_service.get_db_tags()
        return cached

    async def get_home():
        return await test_cli.get("/")

    f1 = get_tags()
    f2 = get_home()

    tags, response = await asyncio.gather(f1, f2)

    assert response.status == 200

    async def assert_tag(tag):
        #print("tag = {}".format(tag["name"]))
        assert tag["name"] in await response.text()

    all = await asyncio.gather(*[assert_tag(tag) for tag in tags])
    assert all is not None


@pytest.mark.run(after="test_db")
async def test_find_companies_in_page(test_cli):
    async def get_companies():
        cached = await job_service.get_cached_companies()
        if cached is None:
            cached = await job_service.get_db_companies()
        return cached

    async def get_home():
        return await test_cli.get("/")

    f1 = get_companies()
    f2 = get_home()

    companies, response = await asyncio.gather(f1, f2)

    assert response.status == 200

    async def assert_company(company):
        #print("company = {}".format(company["name"]))
        assert company["name"] in await response.text()

    all = await asyncio.gather(*[assert_company(company) for company in companies])
    assert all is not None


@pytest.mark.run(after="test_db")
async def test_find_locations_in_page(test_cli):
    async def get_locations():
        cached = await job_service.get_cached_locations()
        if cached is None:
            cached = await job_service.get_db_locations()
        return cached

    async def get_home():
        return await test_cli.get("/")

    f1 = get_locations()
    f2 = get_home()

    locations, response = await asyncio.gather(f1, f2)

    assert response.status == 200

    async def assert_location(location):
        #print("company = {}".format(company["name"]))
        assert location["name"] in await response.text()

    all = await asyncio.gather(*[assert_location(location) for location in locations])
    assert all is not None
