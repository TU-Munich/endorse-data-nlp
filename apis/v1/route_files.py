import os

from flask import Flask, request, render_template
from flask_restplus import Namespace, Resource
from werkzeug.utils import secure_filename

api = Namespace('Files', description='All functionalities of the file service')

FOLDER = "./data"


@api.route('/upload', methods=['GET', 'POST'])
@api.doc('Pipeline')
class Upload(Resource):
    def post(self):
        for file in request.files.getlist('files'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(FOLDER, filename))
            # Todo json
        return 'Upload completed.'
