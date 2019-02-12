from flask_restplus import Namespace, Resource
from services.pipeline_service import *
from config.config import FOLDER

api = Namespace('Pipeline', description='All functionalities of the project pipeline')


@api.route('/project/<string:project_uuid>/pipeline/', methods=['GET'])
@api.doc('Pipeline')
class Pipeline(Resource):
    def get(self, project_uuid):
        folder_path = FOLDER + project_uuid
        handle_folder(project_uuid, folder_path)
        return "", 204
