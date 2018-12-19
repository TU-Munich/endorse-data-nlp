import os
import glob
from flask import Flask, request, render_template, send_from_directory, send_file
from flask_restplus import Namespace, Resource
from werkzeug.utils import secure_filename
from services.files_service import *
from config.config import FOLDER
from services.pipeline_service import handle_file

api = Namespace('Files', description='All functionalities of the project file service')


@api.route('/project/<string:projectUUID>/file', methods=['POST'])
@api.doc('Upload Project Files')
class UploadProjectFile(Resource):
    def post(self, projectUUID):
        """
        Upload file to a project
        :param projectUUID:
        :return:
        """
        for file in request.files.getlist('filepond'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(FOLDER + projectUUID, filename)
            file.save(file_path)
            # Start pipeline
            handle_file(projectUUID, file_path)

        return '', 204


@api.route('/project/<string:projectUUID>/files', methods=['POST'])
@api.doc('Upload Project Files')
class UploadProjectFiles(Resource):
    def post(self, projectUUID):
        """
        Upload files to a project
        :param projectUUID:
        :return:
        """
        for file in request.files.getlist('filepond'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(FOLDER + projectUUID, filename)
            file.save(file_path)
            # Start pipeline
            handle_file(projectUUID, file_path)

        return '', 204


@api.route('/project/<string:projectUUID>/files', methods=['GET'])
@api.doc('Handle Project Files')
class HandleProjectFiles(Resource):
    def get(self, projectUUID):
        """
        Read all files of a project
        :param projectUUID:
        :return:
        """
        results = read_all_files(FOLDER + projectUUID)
        return results


@api.route('/project/<string:projectUUID>/files/<path:path>', methods=['GET', 'POST'])
@api.doc('Handle Project Files')
class HandleProjectFile(Resource):
    @api.response(200, 'Read files in a directory')
    def get(self, projectUUID, path):
        """
        read a specific path of files in the project
        :param projectUUID:
        :param path:
        :return:
        """
        results = read_all_files(FOLDER + projectUUID + "/" + path)
        return results

    @api.response(204, 'File deleted')
    def delete(self, projectUUID, path):
        """
        Delete a file within a project
        :param projectUUID:
        :param path:
        :return:
        """
        for hgx in glob.glob(FOLDER + projectUUID + "/" + path):
            os.remove(hgx)
        return '', 204


@api.route('/project/<string:projectUUID>/files/download/<path:path>', methods=['GET', 'POST'])
@api.doc('Download Project Files')
class DownloadProjectFile(Resource):
    @api.response(200, 'Download a file')
    def get(self, projectUUID, path):
        """
        Download a specific file
        :param projectUUID:
        :param path:
        :return:
        """
        return send_file(FOLDER + projectUUID + "/" + path, as_attachment=True)
