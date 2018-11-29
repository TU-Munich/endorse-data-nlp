from flask import Blueprint
from flask_restplus import Api
from .router_nlp import api as spacy_api

blueprint = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(blueprint,
          title='NLP Backend API',
          version='1.0',
          description='This is the documentation of the NLP Backend',
          # All API metadatas
          )

api.add_namespace(spacy_api, path="/nlp")
