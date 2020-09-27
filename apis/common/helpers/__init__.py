from functools import wraps

from flask import request, current_app

authorizations = {
    'Authorization': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


def authorization_required(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):

        authorization = request.headers.get('Authorization')
        if not authorization:
            return {'status': False,
                    'data': None,
                    'message': 'No authorization token provided!'}, 403

        auth_token = authorization.split(" ")

        if len(auth_token) == 1:
            return {'status': False,
                    'data': None,
                    'message': 'Invalid auth header!'}, 403

        auth_token = authorization.split(" ")[1]

        if current_app.config['API_TOKEN'] != auth_token:
            return {'status': False,
                    'data': None,
                    'message': 'Unauthorized!'}, 401

        return fn(self, *args, **kwargs)

    return wrapper
