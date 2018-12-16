import hashlib
import time

import os
import uuid

from elasticsearch import Elasticsearch

from services.langdetec_service import *
from services.spacy_service import *
from services.files_service import *
from services.tika_service import *
from services.vader_service import *

ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USERNAME, ES_PASSWORD),
    scheme="http",
    port=80,
)


def handle_folder(project_uuid, folder_path):
    # get all files in the folder
    file_paths = read_all_files(folder_path)
    #print("FILES:")
    #print(file_paths)
    for file_path in file_paths:
        handle_file(project_uuid, file_path)

    return


def handle_file(project_uuid, file_path):
    # create a hashname from the filepath
    id = hashlib.md5(str(file_path).encode("utf8")).hexdigest()
    # open file with tika
    parsed_doc = parse_file(file_path)
    # run the nlp pipeline on text
    result = handle_document(parsed_doc["content"])
    # remove content
    # its now called input
    # result["_meta"] = parsed_doc["meta"]
    result["_file_path"] = file_path
    result["_project_uuid"] = project_uuid

    es.index(index="document-index", doc_type="document", id=id, body=result)
    return


def handle_document(parsed_document):
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
    # add unix timestamp
    result["timestamp"] = time.time()
    # add input sentence
    result["input"] = parsed_document
    # clean the document
    clean = doc_clean(parsed_document)
    # detect langs
    result["lang"] = doc_lang(clean)
    # spacy classify document
    doc = doc_spacy(result["lang"], clean)
    # Sentence Segmentation
    result["sentences"] = doc_tokenize(doc)
    # sentiment
    result["sentiment"] = sentences_sentiment(result["sentences"])
    # Part of Speech tagging
    result['pos'] = doc_pos(doc)
    # Named entity recognition
    result['ner'] = doc_ner(doc)

    return result
