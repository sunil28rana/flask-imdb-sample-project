from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint('v1_app', __name__, url_prefix='/v1')
api = Api(
    blueprint,
    title='IMDB',
    doc='/doc',
    version='1.0.0',
    description=''
)