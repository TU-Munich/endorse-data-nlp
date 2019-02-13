from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields
import numpy as np

from services.elastic_search import es
from services.similarity.similarity_service import FaissIndex, add_sentences_to_index, find_sentences_in_index, \
    find_document_in_index

api = Namespace("Similarity API", description="The similarity api endpoints")

sentences_fields = api.model('Resource', {
    'sentences': fields.List(fields.String),
})
sentence_field = api.model('Resource', {
    'sentence': fields.String,
})

"""
{
  labels:['a','b','c',],
  datasets: [{
      label: 'First Dataset',
      data: [
              {x: 100, y: 30, r: 20 , label:'cats'},
              {x: 40, y: 10, r: 10 , label:'cats'},
              {x: 25, y: 15, r: 8 , label:'cats'}
            ],
      backgroundColor: '#FF6384',
      hoverBackgroundColor: '#FF6384',
    }]
}
"""


def create_bubble_chart(data):
    """
    Transform the data so that the result is usable for chartjs bubble chart
    :param data:
    :return:
    """
    result = {}
    result["labels"] = ["similarity"]
    result["datasets"] = []
    for d in data:
        response = es.get(_source_include=["file_name", "file_path", "origin"],
                          index="document-index",
                          doc_type="document", id=d["id"])

        label = response["_source"]["file_name"]

        res = {}
        res["label"] = label
        # add the data to the array
        # adapt the radius for the charjs
        d["r"] = (1-d["similarity"]) * 30
        res["data"] = [d]
        res["backgroundColor"] = "#FF6384"
        res["hoverBackgroundColor"] = "#FF6384"
        result["datasets"].append(res)
    return result


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

        document_results, _, sentence_results = add_sentences_to_index(DocumentIndex, SentenceIndex, id,
                                                                       payload["sentences"])

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

        result = find_sentences_in_index(SentenceIndex, payload["sentence"])

        show_bubble_chart = request.args.get('chartjs')

        if bool(show_bubble_chart):
            result = create_bubble_chart(result)
        print(result)
        return jsonify(result)


@api.route("/project/<string:project_uuid>/documents/<id>")
class Documents(Resource):
    def get(self, project_uuid, id):
        """
        find similar documents
        :param id:
        :return:
        """
        # init faiss index
        DocumentIndex = FaissIndex(project_uuid + "-documents", 1024, create_ind2id=True, create_ind2sent=False)

        response = es.get(_source_include=["document_vector"], index="document-index", doc_type="document", id=id)

        document_vector = np.asarray((response["_source"]["document_vector"]), dtype=np.float32)

        result = find_document_in_index(DocumentIndex, document_vector)

        show_bubble_chart = request.args.get('chartjs')
        if bool(show_bubble_chart):
            result = create_bubble_chart(result)

        return jsonify(result)
