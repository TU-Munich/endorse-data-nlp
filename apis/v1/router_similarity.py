from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields
from services.similarity.similarity_service import add_sentences_to_index, find_sentences_in_index

api = Namespace("Similarity API", description="The similarity api endpoints")

sentences_fields = api.model('Resource', {
    'sentences': fields.List(fields.String),
})
sentence_field = api.model('Resource', {
    'sentence': fields.String,
})


@api.route("/sentences/<id>")
class Sentences(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    @api.expect(sentences_fields)
    def post(self, id):
        """
        Create a new document in the index
        :return:
        """
        payload = request.get_json(force=True)

        if "sentences" not in payload:
            return {"msg": "no sentences"}, 400

        document_results, _, sentence_results = add_sentences_to_index(id, payload["sentences"])

        response = {
            "document_results": document_results,
            "sentence_results": sentence_results
        }

        return jsonify(response)

    @api.expect(sentence_field)
    def put(self, id):
        """
        find similar documents
        :param id:
        :return:
        """
        payload = request.get_json(force=True)

        if "sentence" not in payload:
            return {"msg": "no sentence"}, 400

        result = find_sentences_in_index(payload["sentence"])
        print(result)
        return jsonify(result)


@api.route("/documents/<id>")
class Sentences(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    @api.expect(sentence_field)
    def put(self, id):
        """
        find similar documents
        :param id:
        :return:
        """
        payload = request.get_json(force=True)

        if "sentence" not in payload:
            return {"msg": "no sentence"}, 400

        result = find_sentences_in_index(payload["sentence"])
        print(result)
        return jsonify(result)
