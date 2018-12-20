from flask import request, jsonify
from flask_restplus import Namespace, Resource
from config.config import FOLDER
from services.tika_service import parse_file
from services.elastic_search import es

api = Namespace('TIKA', description='All functionalities of the project tika service')


@api.route('/project/<string:projectUUID>/data')
class ProjectData(Resource):
    def get(self, projectUUID, path):
        """
        Get all data from the tika framework
        :param path: the path to the file
        :return:
        """
        file_path = FOLDER + projectUUID + "/" + path
        print(file_path)
        result = parse_file(file_path)
        return jsonify(result)
