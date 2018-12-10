from elasticsearch import Elasticsearch
from flask import Flask, Blueprint, url_for, jsonify
from flask_restplus import Api
from gevent import os

from apis.v1 import blueprint as v1

# Init flask
app = Flask(__name__)

# Register blueprints
app.register_blueprint(v1)

ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

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
    app.run(debug=True, port=5002)
