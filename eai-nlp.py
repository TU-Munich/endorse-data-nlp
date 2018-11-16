from flask import Flask, Blueprint
import router_spacy

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


app.register_blueprint(router_spacy.api_spacy, url_prefix='/spacey')

if __name__ == '__main__':
    app.run(debug=True)
