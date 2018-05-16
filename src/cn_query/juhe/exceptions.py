from functools import wraps


DEFAULT_CODE = -1


class APIError(ValueError):
    pass


def normalize_network_error(func):
    from requests import exceptions as exc

    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.RequestException as e:
            raise APIError(str(e))

    return decorated
