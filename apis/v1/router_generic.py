import os
import uuid
from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

BLACKLIST = {
    "users": True,
}

ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USERNAME, ES_PASSWORD),
    scheme="http",
    port=80,
)

api = Namespace("Generic API", description="The generic api endpoints")


class Generic(object):
    def __init__(self):
        self.data = dict

    def read_all(self, generic_index, generic_type, scroll):
        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
        print(generic_index, generic_type)
        response = es.search(index=generic_index, doc_type=generic_type, body=doc, scroll=scroll)
        return response

    def read_single(self, generic_index, generic_type, guid):
        response = {}
        response["generic_type"] = generic_type
        response["guid"] = guid
        return response

    def create_with_guid(self, generic_index, generic_type, data):
        # create new guid
        guid = str(uuid.uuid4())
        response = es.index(index=generic_index, doc_type=generic_type, id=guid, body=data)
        return response

    def create(self, generic_index, generic_type, guid, data):
        response = es.index(index=generic_index, doc_type=generic_type, id=guid, body=data)
        return response

    def update(self, generic_index, generic_type, guid, data):
        response = es.update(index=generic_index, doc_type=generic_type, id=guid, body=data)
        return response

    def delete(self, generic_index, generic_type, guid):
        response = es.delete(index=generic_index, doc_type=generic_type, id=guid)
        return response


GEN = Generic()


# payload = api.model('Todo')


@api.route("/<generic_index>/<generic_type>")
@api.param("generic_index", "The generic index")
@api.param("generic_type", "The generic type name")
class GenericList(Resource):
    @api.doc("Read all generic objects")
    def get(self, generic_index, generic_type):
        """
        Read all generic objects
        :return:
        """
        scroll = "1m"
        return jsonify(GEN.read_all(generic_index, generic_type, scroll))

    @api.doc("Create a new generic object", expect=[fields.Raw])
    # @api.route("/:guid")
    def post(self, generic_index, generic_type):
        """
        reate a new generic object
        :param generic_type:
        :param guid:
        :return:
        """
        return jsonify(GEN.create_with_guid(generic_index, generic_type, api.payload)), 201


@api.route("/<generic_index>/<generic_type>/<guid>")
@api.param("generic_index", "The generic index")
@api.param("generic_type", "The generic type name")
@api.param("guid", "The unique identifier of the object")
class GenericSingle(Resource):
    @api.doc("Create a new generic object", expect=[fields.Raw])
    # @api.route("/:guid")
    def post(self, generic_index, generic_type, guid):
        """
        reate a new generic object
        :param generic_type:
        :param guid:
        :return:
        """
        return jsonify(GEN.create(generic_index, generic_type, guid, api.payload)), 201

    @api.doc("Read a single generic object")
    def get(self, generic_index, generic_type, guid):
        """
        Read a single generic object
        :param generic_type:
        :param guid:
        :return:
        """
        return jsonify(GEN.read_single(generic_index, generic_type, guid))

    @api.doc("Update a single generic object")
    # @api.expect(payload)
    def put(self, generic_index, generic_type, guid):
        """
        Update a single generic object
        :param generic_type:
        :param guid:
        :return:
        """
        return jsonify(GEN.update(generic_index, generic_type, guid, api.payload))

    @api.doc("Delete a single generic object")
    @api.response(204, "Symptom deleted")
    def delete(self, generic_index, generic_type, guid):
        """
        Delete a single generic object
        :param generic_type:
        :param guid:
        :return:
        """
        GEN.delete(generic_index, generic_type, guid)
        return "", 204
