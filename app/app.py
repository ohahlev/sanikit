import os
import asyncio
import uvloop
import aiotask_context as context
from sanic import Sanic
from app import util
from app.blueprints.error import error
from app.blueprints.db import db
from app.blueprints.site import site
from app.blueprints.product import product
import app.config as config
from app.jinja import init_jinja
from app.babel import init_babel
from app.session import init_session
from app.middlewares import init_middlewares

import pprint


def create_app(app_config):

    app = Sanic(__name__)

    app.config.from_object(app_config)
    app.static("/static", "./app/static")
    app.error_handler.add(Exception, error.handle_error)
    app.blueprint(db.bp)
    app.blueprint(site.bp)
    app.blueprint(product.bp)

    init_session(app)
    init_jinja(app)
    init_babel(app)
    init_middlewares(app)

    return app


if __name__ == "__main__":

    current_env = os.environ["ENVIRONMENT"]

    ssl_certificate = None if current_env == util.dev else  {
        "cert": "./certificates/domain.cert.pem",
        "key": "./certificates/private.key.pem"
    }

    app = create_app(config)

    asyncio.set_event_loop(uvloop.new_event_loop())

    port = int(os.environ["MY_PORT"])

    server = app.create_server(host="0.0.0.0", port=port, return_asyncio_server=True,
                               access_log=False, ssl=ssl_certificate,
                               debug=(current_env == util.dev))
    loop = asyncio.get_event_loop()
    loop.set_task_factory(context.task_factory)
    task = asyncio.ensure_future(server)
    try:
        loop.run_forever()
    except:
        loop.stop()