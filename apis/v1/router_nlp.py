import uuid

from elasticsearch import Elasticsearch
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse

from services.langdetec_service import doc_lang
from services.pipeline_service import handle_document
from services.spacy_service import doc_spacy, doc_ner, doc_pos, doc_tokenize

es = Elasticsearch()

api = Namespace('spacy', description='use all functionality of spacy')

resource_fields = api.model('Spacy Request', {
    'document': fields.String(min=1),
})
parser = reqparse.RequestParser()
parser.add_argument('debug', type=bool, help='Get the response of the nlp content')


@api.route('/')
class Pipeline(Resource):
    @api.doc('Pipeline')
    @api.expect(body=resource_fields, header=parser)
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
        # handle document
        # classify langauge
        lang = doc_lang(document)
        # spacy, pos, tok ...
        doc = doc_spacy(lang, document)
        # get NER
        output = doc_ner(doc)
        # return result
        result["output"] = output
        return jsonify(result)


@api.route('/pos')
class NER(Resource):
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
        # handle document
        # classify language
        lang = doc_lang(document)
        # spacy, pos, tok ...
        doc = doc_spacy(lang, document)
        # get POS
        output = doc_pos(doc)
        # return result
        result["output"] = output
        return jsonify(result)


@api.route('/tokenize')
class NER(Resource):
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
        # handle document
        # classify language
        lang = doc_lang(document)
        # spacy, pos, tok ...
        doc = doc_spacy(lang, document)
        # get tokenzied document
        output = doc_tokenize(doc)
        # return result
        result["output"] = output
        return jsonify(result)
