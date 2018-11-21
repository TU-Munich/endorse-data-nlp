from flask import Flask, Blueprint, url_for
from flask_restplus import Api

from apis.v1 import blueprint as v1

# Init flask
app = Flask(__name__)

# Register blueprints
app.register_blueprint(v1)

if __name__ == '__main__':
    app.run(debug=True)
