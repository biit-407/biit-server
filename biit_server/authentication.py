from biit_server.http_responses import http400, http401
from biit_server.azure import azure_refresh_token
from enum import Enum
from biit_server.utils import send_discord_message


class AuthenticatedType(Enum):
    BODY = 0
    """
    the token to authenticate with is located in the body 
    of the request
    """
    QUERY = 1
    """
    the token to authenticate with is located in the query
    parameters of the request
    """
    FORM = 2
    """
    the token to authenticate with is located in the body, 
    under the form section within the request
    """
    NONE = 3
    """
    there is no authentication for this request
    """


def authenticated(type: AuthenticatedType = AuthenticatedType.NONE):
    """
    Decorator for making sure a request is authenticated properly

    Args:
        type (AuthenticatedType): the type of authentication to use

    """

    def decorator(func):
        def wrapper(request):
            auth = None
            if type == AuthenticatedType.BODY:
                body = None
                try:
                    body = request.get_json()
                except:
                    send_discord_message(
                        f"unable to parse body for request handler {func.__name__}"
                    )
                    return http400("Missing body")
                auth = azure_refresh_token(body["token"])
                if not auth[0]:
                    send_discord_message(
                        f"body authentication failed for request handler {func.__name__}"
                    )
                    return http401("Not Authenticated")
            if type == AuthenticatedType.QUERY:
                args = request.args
                auth = azure_refresh_token(args["token"])
                if not auth[0]:
                    send_discord_message(
                        f"query authentication failed for request handler {func.__name__}"
                    )
                    return http401("Not Authenticated")
            if type == AuthenticatedType.FORM:
                body = None
                try:
                    body = request.form
                except:
                    send_discord_message(
                        f"unable to parse form for request handler {func.__name__}"
                    )
                    return http400("Missing body")
                auth = azure_refresh_token(body["token"])
                if not auth[0]:
                    send_discord_message(
                        f"form authentication failed for request handler {func.__name__}"
                    )
                    return http401("Not Authenticated")

            result = func(request, auth)
            return result

        return wrapper

    return decorator
