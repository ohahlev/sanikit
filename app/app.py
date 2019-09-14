import os
import asyncio
import uvloop
import aiotask_context as context
from sanic import Sanic
from app import util
from app.blueprints.error import error
from app.blueprints.site import site
from app.blueprints.product import product
import app.config as config
from app.listeners.db import init_pool
from app.middlewares.jinja import init_jinja
from app.middlewares.babel import init_babel
from app.middlewares.session import init_session


def create_app(app_config):

    app = Sanic(__name__)

    # configuration
    app.config.from_object(app_config)
    app.static("/static", "./app/static")
    app.error_handler.add(Exception, error.handle_error)

    # blueprints
    app.blueprint(site.bp)
    app.blueprint(product.bp)

    # listeners
    app.register_listener(init_pool, "before_server_start")

    # middlewares
    init_session(app)
    init_jinja(app)
    init_babel(app)

    return app


if __name__ == "__main__":

    current_env = os.environ["ENVIRONMENT"]

    ssl_certificate = None if current_env == util.dev else  {
        "cert": "./certificates/domain.cert.pem",
        "key": "./certificates/private.key.pem"
    }

    app = create_app(config)
    app1 = app
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