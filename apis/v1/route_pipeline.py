from flask_restplus import Namespace, Resource
from services.pipeline_service import *
from config.config import FOLDER

api = Namespace('Pipeline', description='All functionalities of the project pipeline')


@api.route('/project/<string:projectUUID>/pipeline/', methods=['GET'])
@api.doc('Pipeline')
class Pipeline(Resource):
    def get(self, projectUUID):
        folder_path = FOLDER + projectUUID
        handle_folder(projectUUID, folder_path)
        return (200, 'YES')
