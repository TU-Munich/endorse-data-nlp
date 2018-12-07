from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

BLACKLIST = {
    "users": True,
}

es = Elasticsearch()

api = Namespace("Generic API", description="The generic api endpoints")


class Generic(object):
    def __init__(self):
        self.data = dict

    def read_all(self, generic_type):
        response = {}
        print(generic_type)
        response["generic_type"] = generic_type
        return response

    def read_single(self, generic_type, uuid):
        response = {}
        response["generic_type"] = generic_type
        response["uuid"] = uuid
        return response

    def create(self, generic_type, uuid, data):
        response = {}
        response["generic_type"] = generic_type
        response["uuid"] = uuid
        return response

    def update(self, generic_type, uuid, data):
        response = {}
        response["generic_type"] = generic_type
        response["uuid"] = uuid
        return response

    def delete(self, generic_type, uuid):
        response = {}
        response["generic_type"] = generic_type
        response["uuid"] = uuid
        return response


GEN = Generic()


@api.route("/<generic_type>")
@api.param("generic_type", "The generic type name")
class GenericList(Resource):
    @api.doc("Read all generic objects")
    def get(self, generic_type):
        """
        Read all generic objects
        :return:
        """
        return jsonify(GEN.read_all(generic_type))


@api.route("/<generic_type>/<uuid>")
@api.param("generic_type", "The generic type name")
@api.param("uuid", "The unique identifier of the object")
class GenericSingle(Resource):
    @api.doc("Create a new generic object")
    # @api.route("/:uuid")
    def post(self, generic_type, uuid):
        """
        reate a new generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.create(generic_type, uuid, api.payload)), 201

    @api.doc("Read a single generic object")
    def get(self, generic_type, uuid):
        """
        Read a single generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.read_single(generic_type, uuid))

    @api.doc("Update a single generic object")
    def put(self, generic_type, uuid):
        """
        Update a single generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.update(generic_type, uuid, api.payload))

    @api.doc("Delete a single generic object")
    @api.response(204, "Symptom deleted")
    def delete(self, generic_type, uuid):
        """
        Delete a single generic object
        :param generic_type:
        :param uuid:
        :return:
        """
        GEN.delete(generic_type, uuid)
        return "", 204
