import os
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

    def read_single(self, generic_index, generic_type, uuid):
        response = {}
        response["generic_type"] = generic_type
        response["uuid"] = uuid
        return response

    def create(self, generic_index, generic_type, uuid, data):
        response = es.index(index=generic_index, doc_type=generic_type, id=uuid, body=data, _source=True)
        return response

    def update(self, generic_index, generic_type, uuid, data):
        response = es.update(index=generic_index, doc_type=generic_type, id=uuid, body=data, _source=True)
        return response

    def delete(self, generic_index, generic_type, uuid):
        response = es.delete(index=generic_index, doc_type=generic_type, id=uuid)
        return response


GEN = Generic()

payload = api.model('Todo', fields.Raw)


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


@api.route("/<generic_index>/<generic_type>/<uuid>")
@api.param("generic_index", "The generic index")
@api.param("generic_type", "The generic type name")
@api.param("uuid", "The unique identifier of the object")
class GenericSingle(Resource):
    @api.doc("Create a new generic object", expect=[fields.Raw])
    # @api.route("/:uuid")
    def post(self, generic_index, generic_type, uuid):
        """
        reate a new generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.create(generic_index, generic_type, uuid, api.payload)), 201

    @api.doc("Read a single generic object")
    def get(self, generic_index, generic_type, uuid):
        """
        Read a single generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.read_single(generic_index, generic_type, uuid))

    @api.doc("Update a single generic object")
    @api.expect(payload)
    def put(self, generic_index, generic_type, uuid):
        """
        Update a single generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.update(generic_index, generic_type, uuid, api.payload))

    @api.doc("Delete a single generic object")
    @api.response(204, "Symptom deleted")
    def delete(self, generic_index, generic_type, uuid):
        """
        Delete a single generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        GEN.delete(generic_index, generic_type, uuid)
        return "", 204
