from elasticsearch import Elasticsearch
from flask import Flask, Blueprint, url_for, jsonify, send_from_directory
from flask_cors import CORS
from flask_restplus import Api
import os

from apis.v1 import blueprint as v1

# Env variables
from config.initial import initial_project

DEBUG = os.environ.get('DEBUG', True)

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

# Init flask
app = Flask(__name__)
cors = CORS(app)
# Register blueprints
app.register_blueprint(v1)

INIT = os.environ.get('INIT', None)
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


# Serve the frontend
@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    print(path)
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        return send_from_directory(static_file_dir, 'index.html')

    return send_from_directory(static_file_dir, path)


@app.route('/<index>/<type>/<id>')
def get(index, type, id):
    result = es.get(index=index, doc_type=type, id=id)

    return jsonify(result)

initial_project(es)

if __name__ == '__main__':
    # init
    if INIT != None:
        initial_project(es)

    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
