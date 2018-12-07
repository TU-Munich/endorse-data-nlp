from flask import Blueprint
from flask_restplus import Api
from .router_nlp import api as spacy_api
from .route_files import api as files_api
from .router_tika import api as tika_api
from .router_generic import api as generic_api

blueprint = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(blueprint,
          title='NLP Backend API',
          version='1.0',
          description='This is the documentation of the NLP Backend',
          # All API metadatas
          )

api.add_namespace(spacy_api, path="/nlp")
api.add_namespace(files_api, path="/files")
api.add_namespace(tika_api, path="/tika")
api.add_namespace(generic_api, path="/generic")
