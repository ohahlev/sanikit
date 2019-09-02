import asyncio
from sanic import (
    response,
    Blueprint
)
import logging
from app import util
from app.jinja import jinja
from app.blueprints.product import service as product_service

bp = Blueprint("product", url_prefix="products")

logger = logging.getLogger()


@bp.route("/play&is_advanced=<is_advanced>", methods=["GET", "POST"])
@jinja.template("index.html")
async def play_play(request, is_advanced):
    return {}


@bp.route("/search", methods=["POST"])
def search(request):
    searched = request.form.get("searched")
    sorted_by = request.form.get("sorted_by")
    sorted_as = request.form.get("sorted_as")

    keyword = request.form.get("keyword")

    if keyword is None:
        id_to_filter = util.EMPTY
        name_to_filter = util.EMPTY
        tag_to_filter = util.EMPTY
        category_to_filter = util.EMPTY
        keyword = util.EMPTY
    else:
        id_to_filter = keyword
        name_to_filter = keyword
        tag_to_filter = keyword
        category_to_filter = keyword

    return response.redirect(request.app.url_for("product.search_results", is_advanced=0, searched=searched,
                                                 keyword=keyword, sorted_by=sorted_by, sorted_as=sorted_as,
                                                 per_page=util.PER_PAGE, page=1, id_to_filter=id_to_filter,
                                                 name_to_filter=name_to_filter, tag_to_filter=tag_to_filter,
                                                 category_to_filter=category_to_filter))


@bp.route("/search/advance", methods=["POST"])
def advance_search(request):
    sorted_by = request.form.get("sorted_by")
    sorted_as = request.form.get("sorted_as")

    id_to_filter = request.form.get("id_to_filter") \
        if request.form.get("id_to_filter") is not None else util.EMPTY
    name_to_filter = request.form.get("name_to_filter") \
        if request.form.get("name_to_filter") is not None else util.EMPTY
    tag_to_filter = request.form.get("tag_to_filter") \
        if request.form.get("tag_to_filter") is not None else util.EMPTY
    category_to_filter = request.form.get("category_to_filter") \
        if request.form.get("category_to_filter") is not None else util.EMPTY

    return response.redirect(request.app.url_for("product.search_results", is_advanced=1, searched=1,
                                                 keyword=util.EMPTY, sorted_by=sorted_by, sorted_as=sorted_as,
                                                 per_page=util.PER_PAGE, page=1, id_to_filter=id_to_filter,
                                                 name_to_filter=name_to_filter, tag_to_filter=tag_to_filter,
                                                 category_to_filter=category_to_filter))


@bp.route("/search&is_advanced=<is_advanced:int>&searched=<searched>&keyword=<keyword>&sorted_by=<sorted_by>"
          "&sorted_as=<sorted_as>&per_page=<per_page:int>&page=<page:int>&filtered_by_id=<id_to_filter>"
          "&filtered_by_name=<name_to_filter>"
          "&filtered_by_tag=<tag_to_filter>&filtered_by_category=<category_to_filter>",
          methods=["GET", "POST"])
@jinja.template("product/index.html")
async def search_results(request, is_advanced, searched, keyword, sorted_by, sorted_as, per_page, page, id_to_filter,
                         name_to_filter, tag_to_filter, category_to_filter):

    async def get_categories():
        cached = await product_service.get_cached_categories()
        if cached is None:
            cached = await product_service.get_db_categories()
        return cached

    async def get_tags():
        cached = await product_service.get_cached_tags()
        if cached is None:
            cached = await product_service.get_db_tags()
        return cached

    async def get_products():
        id_to_filter1 = "" if id_to_filter == util.EMPTY else id_to_filter.replace("+", " ")
        name_to_filter1 = "" if name_to_filter == util.EMPTY else name_to_filter.replace("+", " ")
        tag_to_filter1 = "" if tag_to_filter == util.EMPTY else tag_to_filter.replace("+", " ")
        category_to_filter1 = "" if category_to_filter == util.EMPTY else category_to_filter.replace("+", " ")

        return await product_service.get_db_products(util.recent_days, "Asia/Bangkok", is_advanced, per_page, page, sorted_by,
                                             sorted_as, id_to_filter1, name_to_filter1, tag_to_filter1, category_to_filter1)

    f1 = get_categories()
    f2 = get_tags()
    f3 = get_products()

    cas, tas, pros = await asyncio.gather(f1, f2, f3)

    logger.info("found categories in size = {}".format(len(cas)))
    logger.info("found tags in size = {}".format(len(tas)))
    logger.info("found products in size = {}".format(len(pros)))

    total = int(pros[0]["full_count"])
    if total == 0:
        jos = []

    last_page = 0
    if total % per_page == 0:
        last_page = int(total / per_page)
    elif total % per_page > 0:
        last_page = int(total / per_page) + 1

    if keyword == util.EMPTY:
        keyword = ""

    return {"categories": cas, "tags": tas, "products": pros,
            "empty_hash": util.EMPTY, "per_page": per_page, "page": page, "searched": searched,
            "keyword": keyword, "total": total, "last_page": last_page, "sorted_by": sorted_by,
            "sorted_as": sorted_as, "id_to_filter": id_to_filter, "name_to_filter": name_to_filter,
            "tag_to_filter": tag_to_filter, "category_to_filter": category_to_filter.replace("+", " "),
            "is_advanced": is_advanced }