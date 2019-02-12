import hashlib
import time
import json

import os

from services.langdetec_service import *
from services.spacy_service import *
from services.files_service import *
from services.tika_service import *
from services.vader_service import *
from services.elastic_search import es
from services.similarity.similarity_service import add_sentences_to_index, FaissIndex


def handle_crawler_folder(project_uuid, folder_path):
    # get all files in the folder
    file_paths = read_all_files(folder_path)
    # print("FILES:")
    # print(file_paths)
    for file_path in file_paths:
        handle_crawler_file(project_uuid, file_path)

    return


def handle_crawler_file(project_uuid, file_path):
    # create a hashname from the file path
    id = hashlib.md5(str(file_path).encode("utf8")).hexdigest()
    # open file with tika
    # parsed_doc = parse_file(file_path)
    with open(file_path, 'r') as f:
        loaded_json = json.load(f)
        # run the nlp pipeline on text
        result = handle_document(project_uuid, id, loaded_json['content'])
        # print(result)

    # remove content
    # its now called input
    # result["_meta"] = parsed_doc["meta"]
    result["file_path"] = file_path
    result["project_uuid"] = project_uuid

    response = es.index(index="document-index", doc_type="document", id=id, body=result)
    return response


def handle_folder(project_uuid, folder_path):
    # get all files in the folder
    file_paths = read_all_files(folder_path)
    # print("FILES:")
    # print(file_paths)
    for file_path in file_paths:
        handle_file(project_uuid, file_path)

    return


def handle_file(project_uuid, file_path):
    # create a hashname from the filepath
    id = hashlib.md5(str(file_path).encode("utf8")).hexdigest()
    # open file with tika
    print("FILE PATH", file_path)
    parsed_doc = parse_file(file_path)
    # run the nlp pipeline on text
    result = handle_document(project_uuid, id, parsed_doc["content"])
    # remove content
    # its now called input
    # result["_meta"] = parsed_doc["meta"]
    result["file_path"] = file_path
    # get the filename
    result["file_name"] = os.path.basename(file_path)
    result["project_uuid"] = project_uuid
    response = es.index(index="document-index", doc_type="document", id=id, body=result)
    return response


def handle_notebook_document(project_uuid, file_name, parsed_doc, save=True):
    # create a hashname from the filepath
    id = hashlib.md5(str(file_name).encode("utf8")).hexdigest()
    # run the nlp pipeline on text
    result = handle_document(project_uuid, id, parsed_doc)
    # remove content
    # its now called input
    # result["_meta"] = parsed_doc["meta"]
    result["file_path"] = file_name
    result["project_uuid"] = project_uuid
    if save:
        es.index(index="document-index", doc_type="document", id=id, body=result)
    else:
        return result
    return


def handle_document(project_uuid, id, parsed_document, similarity=False):
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
    # similarity
    if similarity:
        # init faiss index
        DocumentIndex = FaissIndex(project_uuid + "-documents", 1024, create_ind2id=True, create_ind2sent=False)
        SentenceIndex = FaissIndex(project_uuid + "-sentences", 1024, create_ind2id=True, create_ind2sent=True)
        document_results, document_vector, sentence_results = add_sentences_to_index(DocumentIndex, SentenceIndex, id, result["sentences"])
        result["similarity_document"] = document_results
        result["similarity_sentences"] = sentence_results
        result["document_vector"] = document_vector.tolist()
    # Part of Speech tagging
    result['pos'] = doc_pos(doc)
    # Named entity recognition
    result['ner'] = doc_ner(doc)
    return result
