from sanic import Blueprint
from sanic.log import logger
from app.jinja import jinja

bp = Blueprint("error")


async def handle_error(request, exception):
    logger.exception(exception)
    return await jinja.render_async("error.html", request, status=500, message=exception)
