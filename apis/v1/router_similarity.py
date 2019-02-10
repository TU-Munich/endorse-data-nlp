from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields
from services.similarity.similarity_service import add_documents_to_index, find_document_in_index

api = Namespace("Similarity API", description="The similarity api endpoints")

resource_fields = api.model('Resource', {
    'sentences': fields.List(fields.String),
})


@api.route("/sentences/<id>")
class Sentences(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    @api.expect(resource_fields)
    def post(self, id):
        """
        Create a new document in the index
        :return:
        """
        payload = request.get_json(force=True)

        if "sentences" not in payload:
            return {"msg": "no sentences"}, 400

        results = add_documents_to_index(id, payload["sentences"])
        return jsonify(results)

    def put(self, id):
        """
        find similar documents
        :param id:
        :return:
        """
        payload = request.get_json(force=True)

        if "sentence" not in payload:
            return {"msg": "no sentence"}, 400

        result = find_document_in_index(payload["sentence"])
        print(result)
        return jsonify(result)
