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


@api.route('/project/<string:projectUUID>/crawl', methods=['GET'])
@api.doc('Execute crawling articles')
@api.response(200, 'Crawling new articles')
class ExecuteCrawler(Resource):
    def get(self, projectUUID):
        """
        CStart to crawl form selected new websites
        :param projectUUID:
        :return:
        """
        
        #response = {}
        #Verify whether the stored FOLDER_SEARCH is existed
        # if not os.path.exists(FOLDER_SEARCH + projectUUID):
        #     os.makedirs(FOLDER_SEARCH + projectUUID)
        #Save file in destination
        # for file in request.files.getlist('filepond'):
        #     filename = secure_filename(file.filename)
        #     file_path = os.path.join(FOLDER_SEARCH + projectUUID, filename)
        #     file.save(file_path)
        #     # Start pipeline
        #     result = handle_file(projectUUID, file_path)
        #     response = { "name": filename, "result": result }
        #print(request)
        request_body = {
            'query' : request.args.get('query'),
            'source': request.args.getlist('source[]'),
            'period': request.args.get('period')
        }
        
        
        execute_crawler(request_body, projectUUID)

        return {
            'message':'Inside the crawler function',
            'keyword': request.args.get('query'),
            'source': request.args.getlist('source[]'),
            'period': request.args.get('period')
        }, 200
         
        # return jsonify(response)


@api.route('/project/<string:projectUUID>/crawl', methods=['POST'])
@api.doc('Stop crawling')
class StopCrawler(Resource):
    def post(self, projectUUID):
        """
        Stop crawling process
        :param projectUUID:
        :return:
        """
        stop_crawler()

        return {
            'message':'Crawler is stopped',
        }, 204

# @api.route('/project/<string:projectUUID>/files', methods=['GET'])
# @api.doc('Handle Project Files')
# class HandleProjectFiles(Resource):
#     def get(self, projectUUID):
#         """
#         Read all files of a project
#         :param projectUUID:
#         :return:
#         """
#         results = read_all_files(FOLDER_SEARCH + projectUUID)
#         return results


# @api.route('/project/<string:projectUUID>/files/<path:path>', methods=['GET', 'POST'])
# @api.doc('Handle Project Files')
# class HandleProjectFile(Resource):
#     @api.response(200, 'Read files in a directory')
#     def get(self, projectUUID, path):
#         """
#         read a specific path of files in the project
#         :param projectUUID:
#         :param path:
#         :return:
#         """
#         results = read_all_files(FOLDER_SEARCH + projectUUID + "/" + path)
#         return results

#     @api.response(204, 'File deleted')
#     def delete(self, projectUUID, path):
#         """
#         Delete a file within a project
#         :param projectUUID:
#         :param path:
#         :return:
#         """
#         for hgx in glob.glob(FOLDER_SEARCH + projectUUID + "/" + path):
#             os.remove(hgx)
#         return '', 204


# @api.route('/project/<string:projectUUID>/files/download/<path:path>', methods=['GET', 'POST'])
# @api.doc('Download Project Files')
# class DownloadProjectFile(Resource):
#     @api.response(200, 'Download a file')
#     def get(self, projectUUID, path):
#         """
#         Download a specific file
#         :param projectUUID:
#         :param path:
#         :return:
#         """
#         return send_file(FOLDER_SEARCH + projectUUID + "/" + path, as_attachment=True)
