import hashlib
import os
import numpy as np
import faiss
from threading import Thread, Lock
import json
from config.config import FOLDER
# Set the laser env
os.environ['LASER'] = os.path.dirname(os.path.realpath(__file__)) + "/LASER"

from services.similarity.Encoders import LASEREncoder
from services.similarity.Encoders import GoogleUse
from services.similarity.Encoders import operations


encoder_path = os.environ['LASER'] + "/models/bilstm.93langs.2018-12-26.pt"
bpe_codes = os.environ['LASER'] + "/models/bilstm.93langs.2018-12-26.pt"
enc = LASEREncoder(encoder_path)
# enc = GoogleUse()

# make faiss available
# dimensions
d = 1024  # LASER
# d = 512  # Google USE
# init index
mutex = Lock()
index = None
try:
    print("try to load faiss index")
    index = faiss.read_index(FOLDER +'laser.index')
    print("successfuly loaded ", index.ntotal, " entries")
except:
    print("failed to load faiss index")
    index = faiss.IndexFlatL2(d)  # build the index

shadow_index = {}
try:
    print("try load shadow index")
    shadow_index_string = json.load(open(FOLDER+"laser.json", "r"))
    shadow_index = {}
    for k, v in shadow_index_string.items():
        shadow_index[int(k)] = v
except:
    print("failed to load shadow index")
    shadow_index = {}


def add_vector_to_index(id, vector):
    mutex.acquire()
    try:
        # print(vector)
        # print(np.array([vector]).shape)
        index.add(np.array([vector]))
        faiss.write_index(index, FOLDER+"laser.index")
        json.dump(shadow_index, open(FOLDER+"laser.json", "w"))
        print("Amount of elements in the index:", index.ntotal)
        shadow_index[index.ntotal - 1] = id
    finally:
        mutex.release()

    return {"index": index.ntotal - 1,
            "id": id}


def find_similar(sentence_vector, k=10):
    results = []
    # we want to see 4 nearest neighbors
    D, I = index.search(np.array([sentence_vector]), k)

    print(D)
    print(I)
    print(shadow_index)

    for count, ind in enumerate(I[0]):
        # don't go for things that are not in the index
        if ind > 0:
            print(ind)
            print(D[0][count])
            results.append({
                "id": shadow_index[ind],
                "similarity": D[0][count].item()
            })

    return results


def add_document_to_index(document_UUID, sentence):
    # encode the sentence
    sentence_vector = enc.encode_sentence(sentence)
    # create a hash for a sentence
    sentence_hash = hashlib.md5(str(sentence).encode("utf8")).hexdigest()
    # combine the document uuid and the sentence uuid
    document_and_sentence_uuid = document_UUID + ":" + sentence_hash
    # add the vector to the index
    result = add_vector_to_index(document_and_sentence_uuid, sentence_vector)
    result["sentence"] = sentence
    result["sentence_hash"] = sentence_hash
    result["document_and_sentence_uuid"] = document_and_sentence_uuid
    return result


def add_documents_to_index(document_UUID, sentences):
    results = []
    sentences_vectors = enc.encode_sentences(sentences)
    # iterate over the sentence
    for i, sentence_vector in enumerate(sentences_vectors):
        # create a hash for a sentence
        sentence_hash = hashlib.md5(str(sentences[i]).encode("utf8")).hexdigest()
        # combine the document uuid and the sentence uuid
        document_and_sentence_uuid = document_UUID + ":" + sentence_hash
        result = add_vector_to_index(document_and_sentence_uuid, sentence_vector)
        result["sentence"] = sentences[i]
        result["sentence_hash"] = sentence_hash
        result["document_and_sentence_uuid"] = document_and_sentence_uuid
        results.append(result)

    return results


def find_document_in_index(sentence):
    sentence_vector = enc.encode_sentence(sentence)
    results = find_similar(sentence_vector)

    return results
