from flask import Flask, Blueprint, request, jsonify
import spacy

nlp = spacy.load('en_core_web_sm')

api_spacy = Blueprint('api_spacy', __name__, template_folder='templates')


@api_spacy.route("/parse/")
def parse_text():
    sentence = request.args.get('sentence')
    doc = nlp(sentence)
    result = {}
    result["input"] = sentence

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

    ner = []
    for ent in doc.ents:
        ner.append(
            {
                "text": ent.text, "start": ent.start_char, "end": ent.end_char, "label": ent.label_
            })

    result['pos'] = pos
    result['ner'] = ner

    return jsonify(result)

    @api_spacy.route("/")
    def index_page():
        return "This is a website about burritos"
