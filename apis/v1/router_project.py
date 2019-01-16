from flask import request, jsonify
from flask_restplus import Namespace, Resource
from config.config import FOLDER
from services.tika_service import parse_file
from services.elastic_search import es

api = Namespace('Project', description='All functionalities of the project')


@api.route('/project/<string:projectUUID>/overview')
class ProjectData(Resource):
    def get(self, projectUUID, path):
        """
        Get a aggregated overview of project data:
        """
        q = {
            "aggs": {
                "by_userid": {
                    "terms": {
                        "field": "_user"
                    },
                    "aggs": {
                        "overall": {
                            "avg": {
                                "field": "overall",
                                "missing": 0
                            }
                        },
                    }
                }
            }
        }
        try:
            scroll = "1m"
            response = es.search(index="symptoms-index", doc_type="project", body=q, scroll=scroll)
            return jsonify(response["aggregations"]["by_userid"]["buckets"][0])
        except:
            return jsonify([])
