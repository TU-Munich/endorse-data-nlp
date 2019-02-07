from elasticsearch import Elasticsearch
from flask import Flask, Blueprint, url_for, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from flask_socketio import SocketIO, emit
from threading import Lock
import random, logging, json
import os
from apis.v1.router_user import UserDbHandler
from services.elastic_search import es

from apis.v1 import blueprint as v1

# Env variables
from config.initial import init_initial_project

DEBUG = os.environ.get('DEBUG', True)

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

thread = None
thread_lock = Lock()

# Init flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-super-secret-string'
jwt = JWTManager(app)
cors = CORS(app)
# Register blueprints
app.register_blueprint(v1)
socketio = SocketIO(app)

INIT = os.environ.get('INIT', False)


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


init_initial_project(es)

@socketio.on('connect')
def test_connect():
    
    logging.debug('Client connected')
    print('Client connected')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

def background_thread():
    with open('quotes.json') as json_data:
        q = json.load(json_data)
        while True:
            socketio.sleep(7)
            i = random.randint(0, len(q['quotes']))
            socketio.emit('server_response',
                        {'data': q['quotes'][i]})
            

#def update_progress():



@socketio.on('disconnect', namespace='/crawl')
def test_disconnect():
    logging.debug('Client disconnected')

if __name__ == '__main__':
    

    # Create a new admin if not present
    create_admin = os.environ.get("CREATE_ADMIN", None)
    admin_password = os.environ.get("ADMIN_PASSWORD", None)
    print(create_admin)
    print(admin_password)
    if create_admin and admin_password:
        # ADMIN

        data = {
            "user_name": "admin",
            "name": "admin",
            "password": admin_password
        }
        UserDbHandler.create_default_admin(data)

    # init
    if INIT:
        init_initial_project(es)

    socketio.run(app, debug=DEBUG, host='0.0.0.0', port=3002)
