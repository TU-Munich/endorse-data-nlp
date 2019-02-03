import uuid
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from services.elastic_search import es

BLACKLIST = {
    "users": True,
}

api = Namespace("Generic API", description="The generic api endpoints")


class Generic(object):
    def __init__(self):
        self.data = dict

    def read_all(self, generic_index, generic_type, scroll, sort):
        doc = {'size': 10000, 'query': {'match_all': {}}}
        print(generic_index, generic_type)
        response = es.search(index=generic_index, doc_type=generic_type, body=doc, scroll=scroll, sort=sort)
        return response

    def read_all_with_query(self, generic_index, generic_type, query):
        print(query)
        response = es.search(index=generic_index, doc_type=generic_type, body=query)
        return response

    def read_single(self, generic_index, generic_type, guid):
        response = es.search(index=generic_index, doc_type=generic_type, id=guid)
        return response

    def read_single_with_query(self, generic_index, generic_type, query):
        response = es.search(index=generic_index, doc_type=generic_type, body=query)
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
        response = es.update(index=generic_index, doc_type=generic_type, id=guid, body={"doc": data})
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
        sort = request.args.get('sort', default="", type=str)
        scroll = request.args.get('scroll', default="1m", type=str)
        return jsonify(GEN.read_all(generic_index, generic_type, scroll, sort))

    @api.doc("Create a new generic object", expect=[fields.Raw])
    # @api.route("/:guid")
    def post(self, generic_index, generic_type):
        """
        reate a new generic object
        :param generic_type:
        :param guid:
        :return:
        """
        response = jsonify(GEN.create_with_guid(generic_index, generic_type, api.payload))
        response.status_code = 201
        return response


@api.route("/<generic_index>/<generic_type>/<guid>")
@api.param("generic_index", "The generic index")
@api.param("generic_type", "The generic type name")
@api.param("guid", "The unique identifier of the object")
class GenericSingle(Resource):
    @api.doc("Create a new generic object", expect=[fields.Raw])
    # @api.route("/:guid")
    def post(self, generic_index, generic_type, guid):
        """
        Create a new generic object
        :param generic_type:
        :param guid:
        :return:
        """
        response = jsonify(GEN.create(generic_index, generic_type, guid, api.payload))
        response.status_code = 201
        return response

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


@api.route("/query/<generic_index>/<generic_type>")
@api.param("generic_index", "The generic index")
@api.param("generic_type", "The generic type name")
class GenericListQuery(Resource):
    @api.doc('Read all generic objects using elasticsearch query as request payload', expect=[fields.Raw])
    def post(self, generic_index, generic_type):
        """
        Read all generic objects using elasticsearch query as request payload
        :param generic_index:
        :param generic_type:
        :payload elasticsearch query:
        :return:
        """
        return jsonify(GEN.read_all_with_query(generic_index, generic_type, api.payload))