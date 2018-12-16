from flask_restplus import Namespace, Resource
from services.pipeline_service import *
from config.config import FOLDER

api = Namespace('Pipeline', description='All functionalities of the project pipeline')


@api.route('/project/<string:projectUUID>/pipeline/', methods=['POST'])
@api.doc('Pipeline')
class Pipeline(Resource):
    def post(self, projectUUID):
        handle_folder(FOLDER + projectUUID)
        return 204, ''
