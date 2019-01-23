from flask_restplus import Namespace, Resource
from services.pipeline_service import *
from config.config import FOLDER
from flask import request, jsonify

api = Namespace('Analysis', description='All file analysis per project')


@api.route('/project/<string:projectUUID>/ner', methods=['GET'])
@api.doc('Retrieve Analysis Project Files')
class RetrieveAnalysisProjectFiles(Resource):
    @api.response(200, 'Retrieve NER files analysis')
    def get(self, projectUUID):
        """
        Retrieve all pipeline analysis of a given project
        :param projectUUID:
        :return:
        """
        q = {
            "_source": ["ner"],
            "query": {
                "term": {
                    "project_uuid": projectUUID,
                }
            }
        }
        response = es.search(index="document-index", doc_type="document", body=q)
        return jsonify(response)
