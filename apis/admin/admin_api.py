from flask import Blueprint
from flask_restplus import Api

from apis.common import authorizations

blueprint = Blueprint('admin_app', __name__, url_prefix='/admin')
api = Api(
    blueprint,
    authorizations=authorizations,
    title='ADMIN IMDB',
    doc='/doc',
    version='1.0.0',
    description=''
)