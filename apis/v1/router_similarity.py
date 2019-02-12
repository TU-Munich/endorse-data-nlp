from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields
from services.similarity.similarity_service import FaissIndex, add_sentences_to_index, find_sentences_in_index

api = Namespace("Similarity API", description="The similarity api endpoints")

sentences_fields = api.model('Resource', {
    'sentences': fields.List(fields.String),
})
sentence_field = api.model('Resource', {
    'sentence': fields.String,
})


@api.route("/project/<string:project_uuid>/sentences/<id>")
class Sentences(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    @api.expect(sentences_fields)
    def post(self, project_uuid, id):
        """
        Create a new document in the index
        :return:
        """
        payload = request.get_json(force=True)

        if "sentences" not in payload:
            return {"msg": "no sentences"}, 400

        # init faiss index
        DocumentIndex = FaissIndex(project_uuid + "-documents", 1024, create_ind2id=True, create_ind2sent=False)
        SentenceIndex = FaissIndex(project_uuid + "-sentences", 1024, create_ind2id=True, create_ind2sent=True)

        document_results, _, sentence_results = add_sentences_to_index(DocumentIndex, SentenceIndex, id, payload["sentences"])

        response = {
            "document_results": document_results,
            "sentence_results": sentence_results
        }

        return jsonify(response)

    @api.expect(sentence_field)
    def put(self, project_uuid, id):
        """
        find similar documents
        :param id:
        :return:
        """
        payload = request.get_json(force=True)

        if "sentence" not in payload:
            return {"msg": "no sentence"}, 400

        SentenceIndex = FaissIndex(project_uuid + "-sentences", 1024, create_ind2id=True, create_ind2sent=True)

        result = find_sentences_in_index(SentenceIndex,payload["sentence"])
        print(result)
        return jsonify(result)


@api.route("/project/<string:project_uuid>/documents/<id>")
class Sentences(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    @api.expect(sentence_field)
    def put(self, project_uuid, id):
        """
        find similar documents
        :param id:
        :return:
        """
        payload = request.get_json(force=True)

        if "sentence" not in payload:
            return {"msg": "no sentence"}, 400

        # init faiss index
        DocumentIndex = FaissIndex(project_uuid + "-documents", 1024, create_ind2id=True, create_ind2sent=False)

        result = find_document_in_index(DocumentIndex, payload["sentence"])
        print(result)
        return jsonify(result)
