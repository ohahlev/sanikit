from sanic_babel import Babel
import pprint

babel = Babel(configure_jinja=True)


@babel.localeselector
def get_locale(request):
    session = request["session"]
    try:
        lang = session["lang"]
    except KeyError:
        lang = request.app.config["LANG"]
        session.setdefault("lang", lang)
    return lang


def init_babel(app):
    babel.init_app(app)

