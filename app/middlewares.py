from app import util


def init_middlewares(app):

    @app.middleware("response")
    async def insert_last_status(request, response):
        session = request["session"]
        if "last_status" not in session:
            session["last_status"] = util.undefined
        response.headers["Last-Status"] = session["last_status"]
