from sanic_session import Session, InMemorySessionInterface

session = Session()


def init_session(app):
    session.init_app(app, interface=InMemorySessionInterface(expiry=2592000))

