from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse

from services.pipeline_service import *
from services.spacy_service import *
from services.vader_service import *

es = Elasticsearch()

api = Namespace('NLP', description='All functionalities of the natural language processing service')

resource_fields = api.model('NLP Document Request', {
    'document': fields.String(min=1),
})
parser = reqparse.RequestParser()
parser.add_argument('debug', type=bool, help='Get the response of the nlp content')


@api.route('/')
class Pipeline(Resource):
    def get(self):
        result = {
            "api": "pipeline"
        }
        return jsonify(result)

    @api.doc('Pipeline')
    @api.expect(resource_fields)
    def post(self):
        req = request.get_json(silent=True)
        # parse arguments
        debug = request.args.get('debug', default=False)
        document = req['document']  # request.args.get('sentence')
        # handle sentence
        result = handle_document(document)
        # Save in database if its not debugged
        if not debug:
            es.index(index="test-index", doc_type='sentence', id=uuid.uuid1(), body=result)
        # return json result
        return jsonify(result)


def pre_process_doc(document):
    # handle document
    # classify language
    lang = doc_lang(document)
    cleaned = doc_clean(document)
    # spacy, pos, tok ...
    doc = doc_spacy(lang, cleaned)
    return doc


@api.route('/ner')
class NER(Resource):
    @api.doc('Named Entity Recognition')
    @api.expect(resource_fields)
    def post(self):
        # parse arguments
        req = request.get_json(silent=True)
        # get document
        document = req['document']
        # init result dict
        result = dict()
        result["input"] = document
        # pre process doc
        doc = pre_process_doc(document)
        # get NER
        output = doc_ner(doc)
        # return result
        result["output"] = output
        return jsonify(result)


@api.route('/pos')
class POS(Resource):
    @api.doc('Part of speech tagging')
    @api.expect(resource_fields)
    def post(self):
        # parse arguments
        req = request.get_json(silent=True)
        # get document
        document = req['document']
        # init result dict
        result = dict()
        result["input"] = document
        # pre process doc
        doc = pre_process_doc(document)
        # get POS
        output = doc_pos(doc)
        # return result
        result["output"] = output
        return jsonify(result)


@api.route('/tokenize')
class Tokenize(Resource):
    @api.doc('Tokenize document')
    @api.expect(resource_fields)
    def post(self):
        # parse arguments
        req = request.get_json(silent=True)
        # get document
        document = req['document']
        # init result dict
        result = dict()
        result["input"] = document
        # pre process doc
        doc = pre_process_doc(document)
        # get tokenzied document
        output = doc_tokenize(doc)
        # return result
        result["output"] = output
        return jsonify(result)


@api.route('/lang')
class Language(Resource):
    @api.doc('Detect language')
    @api.expect(resource_fields)
    def post(self):
        # parse arguments
        req = request.get_json(silent=True)
        # get document
        document = req['document']
        # init result dict
        result = dict()
        result["input"] = document
        # return result
        result["output"] = doc_lang(document)
        return jsonify(result)


@api.route('/sentiment')
class Language(Resource):
    @api.doc('Calc sentiment')
    @api.expect(resource_fields)
    def post(self):
        # parse arguments
        req = request.get_json(silent=True)
        # get document
        document = req['document']
        # init result dict
        result = dict()
        result["input"] = document
        # check if input is list
        if isinstance(document, list):
            result["output"] = sentences_sentiment(document)
        else:
            result["output"] = sentences_sentiment([document])
        # return result

        return jsonify(result)
