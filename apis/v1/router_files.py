import os
import glob
from flask import Flask, request, render_template, send_from_directory, send_file, jsonify
from flask_restplus import Namespace, Resource
from werkzeug.utils import secure_filename
from services.files_service import *
from config.config import FOLDER
from services.pipeline_service import handle_file

api = Namespace('Files', description='All functionalities of the project file service')


@api.route('/project/<string:project_uuid>/file', methods=['POST'])
@api.doc('Upload Project Files')
@api.response(200, 'Upload new files')
class UploadProjectFile(Resource):
    def post(self, project_uuid):
        """
        Upload file to a project
        :param project_uuid:
        :return:
        """
        response = {}
        if not os.path.exists(FOLDER + project_uuid):
            os.makedirs(FOLDER + project_uuid)
        for file in request.files.getlist('filepond'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(FOLDER + project_uuid, filename)
            file.save(file_path)
            # Start pipeline
            result = handle_file(project_uuid, file_path)
            response = { "name": filename, "result": result }
        return jsonify(response)


@api.route('/project/<string:project_uuid>/files', methods=['POST'])
@api.doc('Upload Project Files')
class UploadProjectFiles(Resource):
    def post(self, project_uuid):
        """
        Upload files to a project
        :param project_uuid:
        :return:
        """
        if not os.path.exists(FOLDER + project_uuid):
            os.makedirs(FOLDER + project_uuid)

        for file in request.files.getlist('filepond'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(FOLDER + project_uuid, filename)
            file.save(file_path)
            # Start pipeline
            handle_file(project_uuid, file_path)

        return '', 204


@api.route('/project/<string:project_uuid>/files', methods=['GET'])
@api.doc('Handle Project Files')
class HandleProjectFiles(Resource):
    def get(self, project_uuid):
        """
        Read all files of a project
        :param project_uuid:
        :return:
        """
        results = read_all_files(FOLDER + project_uuid)
        return results


@api.route('/project/<string:project_uuid>/files/<path:path>', methods=['GET', 'POST'])
@api.doc('Handle Project Files')
class HandleProjectFile(Resource):
    @api.response(200, 'Read files in a directory')
    def get(self, project_uuid, path):
        """
        read a specific path of files in the project
        :param project_uuid:
        :param path:
        :return:
        """
        results = read_all_files(FOLDER + project_uuid + "/" + path)
        return results

    @api.response(204, 'File deleted')
    def delete(self, project_uuid, path):
        """
        Delete a file within a project
        :param project_uuid:
        :param path:
        :return:
        """
        for hgx in glob.glob(FOLDER + project_uuid + "/" + path):
            os.remove(hgx)
        return '', 204


@api.route('/project/<string:project_uuid>/files/download/<path:path>', methods=['GET', 'POST'])
@api.doc('Download Project Files')
class DownloadProjectFile(Resource):
    @api.response(200, 'Download a file')
    def get(self, project_uuid, path):
        """
        Download a specific file
        :param project_uuid:
        :param path:
        :return:
        """
        return send_file(FOLDER + project_uuid + "/" + path, as_attachment=True)
