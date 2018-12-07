import uuid

from elasticsearch import Elasticsearch
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse

from services.langdetec_service import doc_lang
from services.pipeline_service import handle_document
from services.spacy_service import doc_spacy, doc_ner, doc_pos, doc_tokenize, doc_clean
from services.tika_service import parse_file

api = Namespace('TIKA', description='All functionalities of the tika')


@api.route('/<path:path>')
class Pipeline(Resource):
    def get(self, path):
        """
        Get all data from the tika framework
        :param path: the path to the file
        :return:
        """
        print(path)
        result = parse_file(path)
        return jsonify(result)
