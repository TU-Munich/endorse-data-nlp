from elasticsearch import Elasticsearch
from flask import Flask, Blueprint, url_for, jsonify
from flask_cors import CORS
from flask_restplus import Api
import os

from apis.v1 import blueprint as v1

# Init flask
app = Flask(__name__)
cors = CORS(app)
# Register blueprints
app.register_blueprint(v1)

ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

if len(ES_HOST) == 0 or len(ES_USERNAME) == 0:
    print("No environment parameters set. Please specify")
    os._exit(os.EX_NOHOST)

es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USERNAME, ES_PASSWORD),
    scheme="http",
    port=80,
)

test = {
    "hello": "world"
}

es.index(index="test-index", doc_type='sentence', id=1, body=test)


@app.route('/')
def index():
    result = {
        "api": "v1"
    }
    return jsonify(result)


@app.route('/<index>/<type>/<id>')
def get(index, type, id):
    result = es.get(index=index, doc_type=type, id=id)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
