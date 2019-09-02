from functools import wraps
from sanic.response import json

"""
def role_required(argument):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return app.login_manager.unauthorized()
            allowed = False
            for role in current_user.roles:
                for role_ in argument:
                    if role.name == role_:
                        allowed = True
                        break
                if allowed is True:
                    break
            if allowed is False:
                flash("access denied", "negative")
                return redirect(url_for("site.index"))
            return function(*args, **kwargs)
        return wrapper
    return real_decorator
"""

"""
def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator
"""