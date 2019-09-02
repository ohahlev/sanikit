from aiocache import cached, SimpleMemoryCache as Cache
from sanic.exceptions import (
     SanicException
)
import logging
from app.blueprints.db.db import bp as db_bp
from app import util

logger = logging.getLogger()

@cached(key="categories")
async def get_db_categories():
    # get connection from the pool
    async with db_bp.pool.acquire() as connection:
        # get transaction
        async with connection.transaction():
            # fetch article by type
            try:
                sql = "SELECT * FROM category WHERE deleted IS FALSE ORDER BY name ASC"
                result = await connection.fetch(sql, timeout=util.timeout)
                logger.info("from db, categories in size = {}".format(len(result)))
                return result
            except Exception as e:
                logger.error("{0}: sql = {1}".format(e, sql))
                raise SanicException(e)


async def get_cached_categories():
    cache = Cache()
    result = await cache.get("categories")
    logger.info("from cached, categories in size = {}".format(0 if result is None else len(result)))
    return result


@cached(key="tags")
async def get_db_tags():
    # get connection from the pool
    async with db_bp.pool.acquire() as connection:
        # get transaction
        async with connection.transaction():
            # fetch article by type
            try:
                sql = "SELECT * FROM tag WHERE deleted IS FALSE ORDER BY name ASC"
                result = await connection.fetch(sql, timeout=util.timeout)
                logger.info("from db, tags in size = {}".format(len(result)))
                return result
            except Exception as e:
                logger.error("{0}: sql = {1}".format(e, sql))
                raise SanicException(e)


async def get_cached_tags():
    cache = Cache()
    result = await cache.get("tags")
    logger.info("from cache, tags in size = {}".format(0 if result is None else len(result)))
    return result

async def get_db_products(since, tz, is_advanced, per_page, page, sorted_by, sorted_as, id_to_filter, name_to_filter,
                      tag_to_filter, category_to_filter):
    # get connection from the pool
    async with db_bp.pool.acquire() as connection:
        # get transaction
        async with connection.transaction():
            # fetch article by type
            where_clause = ""
            if is_advanced == 1:
                where_clause = "AND LOWER(p.name::VARCHAR) LIKE LOWER($5::VARCHAR) " \
                      "AND LOWER(c.name::VARCHAR) LIKE LOWER($6::VARCHAR) " \
                      "AND LOWER(t.name::VARCHAR) LIKE LOWER($7::VARCHAR) "
            elif is_advanced == 0:
                where_clause = "OR LOWER(p.name::VARCHAR) LIKE LOWER($5::VARCHAR) " \
                      "OR LOWER(c.name::VARCHAR) LIKE LOWER($6::VARCHAR) " \
                      "OR LOWER(t.name::VARCHAR) LIKE LOWER($7::VARCHAR) "
            sql = ""
            try:
                sql = "WITH cte AS (SELECT p.id AS product_id,p.name," \
                      "p.date_created AT TIME ZONE 'UTC' AT TIME ZONE $1 AS product_date_created," \
                      "p.last_updated AT TIME ZONE 'UTC' AT TIME ZONE $2 AS product_last_updated," \
                      "c.id AS category_id, c.name AS category_name, " \
                      "array_to_string(array(SELECT t1.name FROM tag t1 JOIN tag_product tj1 ON tj1.tag_id = t1.id " \
                      "WHERE tj1.product_id = p.id),',') as tags " \
                      "FROM product p " \
                      "LEFT JOIN category c ON c.id = p.category_id " \
                      "LEFT JOIN tag_product tp ON tp.product_id = p.id " \
                      "LEFT JOIN tag t ON tp.tag_id = t.id " \
                      "WHERE p.deleted IS FALSE " \
                      "AND p.date_created > CURRENT_TIMESTAMP - ($3 || ' DAY')::INTERVAL " \
                      "AND(p.id::VARCHAR LIKE $4::VARCHAR " \
                      "{0}" \
                      ") " \
                      "GROUP BY p.id, c.id) " \
                      "SELECT * FROM (TABLE cte " \
                      "ORDER BY {1} " \
                      "LIMIT $8 OFFSET $9) sub " \
                      "RIGHT JOIN(SELECT COUNT(*) FROM cte) c(full_count) ON TRUE"\
                    .format(where_clause, "{0} {1}".format(sorted_by, sorted_as))
                result = await connection.fetch(sql, tz, tz,
                                                "'{}'".format(since),
                                                "%{}%".format(id_to_filter),
                                                "%{}%".format(name_to_filter),
                                                "%{}%".format(category_to_filter),
                                                "%{}%".format(tag_to_filter),
                                                per_page, (page-1)*per_page,
                                                timeout=util.timeout)
                logger.info("from db, products in page = {0} in size = {1}".format(page, len(result)))
                return result
            except Exception as e:
                logger.exception(e)
                raise SanicException(e)


async def get_cached_products(page):
    cache = Cache()
    result = await cache.get("products{}".format(page))
    logger.info("from cache, products in page = {0} in size = {1}".format(page, 0 if result is None else len(result)))
    return result
