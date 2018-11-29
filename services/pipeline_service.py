import time

from services.langdetec_service import doc_lang
from services.spacy_service import doc_pre_process, doc_spacy, doc_tokenize, doc_pos, doc_ner


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
    # add input sentence
    result["input"] = document
    # add unix timestamp
    result["timestamp"] = time.time()
    # clean the document
    clean = doc_pre_process(document)
    # detect langs
    result["lang"] = doc_lang(clean)
    # spacy classify document
    doc = doc_spacy(result["lang"], clean)
    # Sentence Segmentation
    result["sentences"] = doc_tokenize(doc)
    # Part of Speech tagging
    result['pos'] = doc_pos(doc)
    # Named entity recognition
    result['ner'] = doc_ner(doc)

    return result
