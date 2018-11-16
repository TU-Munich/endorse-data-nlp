import time
import uuid
import spacy
from flask import Flask, Blueprint, request, jsonify
from elasticsearch import Elasticsearch

es = Elasticsearch()

nlp = spacy.load('en_core_web_sm')

api_spacy = Blueprint('api_spacy', __name__, template_folder='templates')


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
            "is_stop": token.is_stop
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


@api_spacy.route("/parse/")
def parse_text():
    # parse arguments
    debug = request.args.get('debug', default=False)
    sentence = request.args.get('sentence')
    # handle sentence
    result = handle_document(sentence, debug)
    # return json result
    return jsonify(result)
