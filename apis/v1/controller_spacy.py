import time
from langdetect import detect
import spacy
from langdetect import detect, detect_langs

nlp_en = spacy.load('en')
nlp_de = spacy.load('de')


def doc_pre_process(raw):
    clean = raw.strip(' \t\n\r')
    return clean


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


def handle_document(document):
    """
    Take a document and classify the language of the document
    with the google lang classifier
    Take a document and use the spacy classifier
    to execute the following tasks
    * POS
    * NER
    """
    # init result dict
    result = dict()
    clean = doc_pre_process(document)
    # classify language
    result["lang"] = detect(clean)
    # spacy classify document
    if result["lang"] == "de":
        doc = nlp_de(clean)
    else:
        doc = nlp_en(clean)
    # detect langs
    result["lang"] = detect(doc.text)
    # the raw document
    result["raw"] = document

    # result["langs"] = detect_langs(doc.text)
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

    return result
