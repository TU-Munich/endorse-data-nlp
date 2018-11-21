import time
import uuid
import spacy
from langdetect import detect, detect_langs
from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

es = Elasticsearch()

nlp = spacy.load('en_core_web_sm')

api = Namespace('spacy', description='use all functionality of spacy')


def doc_pos(doc):
    """
    Take a spacy doc object
    extract all necessary information
    from the part of speech subsection
    """
    pos = []
    for token in doc:
        pos.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop,
        })
    return pos


def doc_ner(doc):
    """
    Take a spacy doc object
    extract all necessary information
    from the named entity subsection
    """
    ner = []
    for ent in doc.ents:
        ner.append(
            {
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_
            })
    return ner


def doc_sentences(doc):
    """
    Take a spacy doc object
    split the document into sentences
    """
    sentences = []
    for sent in doc.sents:
        sentences.append(sent.text)
    return sentences


def handle_document(document, debug=False):
    """
    Take a sentence and use the spacy classifier
    to execute the following tasks
    * POS
    * NER
    """
    # spacy classify document
    doc = nlp(document)
    # init result dict
    result = dict()
    # detect langs
    result["lang"] = detect(doc.text)
    #result["langs"] = detect_langs(doc.text)
    # add input sentence
    result["input"] = document
    # add unix timestamp
    result["timestamp"] = time.time()
    # Sentence Segmentation
    result["sentences"] = doc_sentences(doc)
    # Part of Speech tagging
    result['pos'] = doc_pos(doc)
    # Named entity recognition
    result['ner'] = doc_ner(doc)
    # Save in database if its not debugged
    if debug:
        # return result
        print(result)
        res = result
    else:
        # return if object was created
        res = es.index(index="test-index", doc_type='sentence', id=uuid.uuid1(), body=result)

    return res


resource_fields = api.model('Spacy Request', {
    'sentence': fields.String(min=1),
})
parser = reqparse.RequestParser()
parser.add_argument('debug', type=bool, help='Get the response of the nlp content')


@api.route('/')
class Spacy(Resource):
    @api.doc('Spacy')
    @api.expect(resource_fields)
    @api.expect(parser)
    def post(self):
        req = request.get_json(silent=True)
        # parse arguments

        debug = request.args.get('debug', default=False)
        sentence = req['sentence']  # request.args.get('sentence')
        # handle sentence
        result = handle_document(sentence, debug)
        # return json result
        return jsonify(result)


resource_fields = api.model('Resource', {
    'name': fields.String,
})


@api.route('/hello/<id>')
class MyResource(Resource):
    @api.doc(body=resource_fields)
    def get(self):
        pass
