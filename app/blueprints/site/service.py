from sanic.exceptions import (
     SanicException
)
from sanic.log import logger
from app.blueprints.db.db import bp as db_bp
from app import util


async def get_article_by_type(type):
    # get connection from the pool
    async with db_bp.pool.acquire() as connection:
        # get transaction
        async with connection.transaction():
            # fetch article by type
            try:
                sql = "SELECT * FROM article WHERE type = '{0}'".format(type)
                result = await connection.fetchrow(sql, timeout=util.timeout)
                return result
            except Exception as e:
                logger.error("{0}: sql = {1}".format(e, sql))
                raise SanicException(e)


async def create_article_of_type(type, text):
    # get connection from the pool
    async with db_bp.pool.acquire() as connection:
        # get transaction
        async with connection.transaction():
            try:
                sql = "INSERT INTO article (type, text) VALUES ({0}, {1})".format(type, text)
                status = await connection.execute(sql, timeout=util.timeout)
                return status
            except Exception as e:
                logger.error("{0}: sql = {1}".format(e, sql))
                raise SanicException(e)
