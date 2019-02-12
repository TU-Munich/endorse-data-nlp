import os
import glob
from flask import Flask, request, render_template, send_from_directory, send_file, jsonify
from flask_restplus import Namespace, Resource
from werkzeug.utils import secure_filename
from services.files_service import *
#from config.config import FOLDER_SEARCH
from services.crawler_service import execute_crawler, stop_crawler
from services.pipeline_service import handle_file


api = Namespace('Crawler', description='All functionalities of the crawler service')


@api.route('/project/<string:project_uuid>/crawl', methods=['GET'])
@api.doc('Execute crawling articles')
@api.response(200, 'Crawling new articles')
class ExecuteCrawler(Resource):
    def get(self, project_uuid):
        """
        CStart to crawl form selected new websites
        :param project_uuid:
        :return:
        """
        
        #response = {}
        #Verify whether the stored FOLDER_SEARCH is existed
        # if not os.path.exists(FOLDER_SEARCH + project_uuid):
        #     os.makedirs(FOLDER_SEARCH + project_uuid)
        #Save file in destination
        # for file in request.files.getlist('filepond'):
        #     filename = secure_filename(file.filename)
        #     file_path = os.path.join(FOLDER_SEARCH + project_uuid, filename)
        #     file.save(file_path)
        #     # Start pipeline
        #     result = handle_file(project_uuid, file_path)
        #     response = { "name": filename, "result": result }
        #print(request)
        request_body = {
            'query' : request.args.get('query'),
            'source': request.args.getlist('source[]'),
            'period': request.args.get('period')
        }
        
        
        execute_crawler(request_body, project_uuid)

        return {
            'message':'Inside the crawler function',
            'keyword': request.args.get('query'),
            'source': request.args.getlist('source[]'),
            'period': request.args.get('period')
        }, 200
         
        # return jsonify(response)


@api.route('/project/<string:project_uuid>/crawl', methods=['POST'])
@api.doc('Stop crawling')
@api.response(208, 'Stop crawling')
class StopCrawler(Resource):
    def post(self, project_uuid):
        """
        Stop crawling process
        :param project_uuid:
        :return:
        """
        stop_crawler()

        return {
            'message':'Crawler is stopped',
        }, 208

# @api.route('/project/<string:project_uuid>/files', methods=['GET'])
# @api.doc('Handle Project Files')
# class HandleProjectFiles(Resource):
#     def get(self, project_uuid):
#         """
#         Read all files of a project
#         :param project_uuid:
#         :return:
#         """
#         results = read_all_files(FOLDER_SEARCH + project_uuid)
#         return results


# @api.route('/project/<string:project_uuid>/files/<path:path>', methods=['GET', 'POST'])
# @api.doc('Handle Project Files')
# class HandleProjectFile(Resource):
#     @api.response(200, 'Read files in a directory')
#     def get(self, project_uuid, path):
#         """
#         read a specific path of files in the project
#         :param project_uuid:
#         :param path:
#         :return:
#         """
#         results = read_all_files(FOLDER_SEARCH + project_uuid + "/" + path)
#         return results

#     @api.response(204, 'File deleted')
#     def delete(self, project_uuid, path):
#         """
#         Delete a file within a project
#         :param project_uuid:
#         :param path:
#         :return:
#         """
#         for hgx in glob.glob(FOLDER_SEARCH + project_uuid + "/" + path):
#             os.remove(hgx)
#         return '', 204


# @api.route('/project/<string:project_uuid>/files/download/<path:path>', methods=['GET', 'POST'])
# @api.doc('Download Project Files')
# class DownloadProjectFile(Resource):
#     @api.response(200, 'Download a file')
#     def get(self, project_uuid, path):
#         """
#         Download a specific file
#         :param project_uuid:
#         :param path:
#         :return:
#         """
#         return send_file(FOLDER_SEARCH + project_uuid + "/" + path, as_attachment=True)
