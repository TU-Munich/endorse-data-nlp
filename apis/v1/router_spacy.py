import time
import uuid
from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

from apis.v1.controller_spacy import handle_document

es = Elasticsearch()

api = Namespace('spacy', description='use all functionality of spacy')

resource_fields = api.model('Spacy Request', {
    'sentence': fields.String(min=1),
})
parser = reqparse.RequestParser()
parser.add_argument('debug', type=bool, help='Get the response of the nlp content')


@api.route('/')
class Spacy(Resource):
    @api.doc('Spacy')
    @api.expect(resource_fields)
    @api.expect(parser)
    def post(self):
        req = request.get_json(silent=True)
        # parse arguments

        debug = request.args.get('debug', default=False)
        sentence = req['sentence']  # request.args.get('sentence')
        # handle sentence
        result = handle_document(sentence)
        # Save in database if its not debugged
        if debug:
            # return result
            print(result)
        else:
            # return if object was created
            res = es.index(index="test-index", doc_type='sentence', id=uuid.uuid1(), body=result)
        # return json result
        return jsonify(result)


resource_fields = api.model('Resource', {
    'name': fields.String,
})


@api.route('/hello/<id>')
class MyResource(Resource):
    @api.doc(body=resource_fields)
    def get(self):
        pass
