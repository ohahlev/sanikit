import asyncio
from sanic import (
    response,
    Blueprint
)
from sanic.exceptions import abort
from app import util
from app.blueprints.site.forms import (
    FormAboutUs
)
from sanic_babel import refresh
from app.jinja import jinja
from app.blueprints.site import service as article_service

bp = Blueprint("site")


@bp.route("/favicon.ico")
async def favicon(request):
    return await response.file("app/static/img/favicon.ico")


@bp.route("/test_error")
async def test_error(request):
    abort(500, "something goes wrong")


@bp.route("/")
async def home(request):
    return response.redirect(request.app.url_for("product.search_results", is_advanced=0, searched=0,
                                                 keyword=util.EMPTY, sorted_by="product_id",
                                                 sorted_as="desc", per_page=util.PER_PAGE, page=1,
                                                 id_to_filter=util.EMPTY, name_to_filter=util.EMPTY,
                                                 tag_to_filter=util.EMPTY,
                                                 category_to_filter=util.EMPTY))


@bp.route("/lang", methods=["POST"])
@jinja.template("index.html")
async def switch_lang(request):
    lang = request.form.get("selected_lang")
    session = request["session"]
    try:
        session_lang = session["lang"]
        if lang != session_lang:
            session["lang"] = lang
    except KeyError:
        session["lang"] = lang
    refresh()
    current_page = request.form.get("current_page")
    if not current_page:
        return {}
    else:
        current_page = current_page.replace("searched=1", "searched=0")
    return response.redirect(current_page)


@bp.route("/about")
@jinja.template("site/about.html")
async def about(request):
    article = await article_service.get_article_by_type(util.about["type"])
    return {"article": article}


@bp.route("/contact")
@jinja.template("site/contact.html")
async def contact(request):
    article = await article_service.get_article_by_type(util.contact["type"])
    return {"article": article}


@bp.route("/admin/about/edit", methods=["GET", "POST"])
@jinja.template("site/about_edit.html")
async def edit_about(request):
    form = FormAboutUs(request)
    if form.validate_on_submit():
        return response.redirect("/admin/about/edit")
    return {"form": form}



