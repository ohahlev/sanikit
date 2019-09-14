import os
from asyncpg import create_pool
from sanic.log import logger
from app import util

async def init_pool(app, loop):
    max_connection = os.environ["MAX_CONNECTION"]
    if not max_connection:
        max_connection = 50
    else:
        max_connection = int(max_connection)
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    connection_str = "postgresql://{0}:{1}@{2}:{3}/{4}".format(db_user, db_pass, db_host, db_port, db_name)
    timeout = util.timeout
    if not timeout:
        timeout = 30
    try:
        pool = await create_pool(connection_str, max_size=max_connection)
        app.pool = pool
    except Exception as e:
        logger.error("{0}: connection string = {1}, max connection={2}, timeout={3}"
                     .format(e, connection_str, max_connection, timeout))
        return

    """
    try:
        file = os.path.join("app", "data", "schema.sql")
        await init_schema(pool, file)
    except Exception as e:
        logger.error(e)
        return
    """
