from sanic_asyncjinja2 import SanicAsyncJinja2

jinja = SanicAsyncJinja2()


def init_jinja(app):
    jinja.init_app(app)
    app.jinja_env.globals["config"] = app.config

