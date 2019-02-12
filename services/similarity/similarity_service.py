import hashlib
import os
import numpy as np
import faiss
from threading import Thread, Lock
import json
from config.config import FOLDER
from sklearn.manifold import TSNE

# Set the laser env
os.environ['LASER'] = os.path.dirname(os.path.realpath(__file__)) + "/LASER"

from services.similarity.Encoders import LASEREncoder

encoder_path = os.environ['LASER'] + "/models/bilstm.93langs.2018-12-26.pt"
bpe_codes = os.environ['LASER'] + "/models/bilstm.93langs.2018-12-26.pt"
enc = LASEREncoder(encoder_path)


# enc = GoogleUse()

class FaissIndex():
    def __init__(self, name, dimensions, create_ind2id=True, create_ind2sent=False):
        self.name = name
        self.dimensions = dimensions
        self.index = None
        self.mutex = Lock()
        self.create_ind2id = create_ind2id
        self.create_ind2sent = create_ind2sent
        try:
            print("try to load " + self.name + " faiss index")
            self.index = faiss.read_index(FOLDER + self.name + '.index')
            print("successfuly loaded ", self.index.ntotal, " entries in " + self.name + " index")
        except:
            print("failed to load  " + self.name + " faiss index")
            self.index = faiss.IndexFlat(self.dimensions)  # build the index

        if self.create_ind2id:
            # index to id
            self.ind2id = {}
            try:
                print("try load  " + self.name + " ind2id index")
                json_file = json.load(open(FOLDER + self.name + ".json", "r"))
                self.ind2id = {}
                for k, v in json_file.items():
                    self.ind2id[int(k)] = v
                print("successfuly  " + self.name + " loaded ", len(self.ind2id), " entries in ind2id")
            except:
                print("failed to load  " + self.name + " ind2id")
                self.ind2id = {}

        # index to sentence
        if self.create_ind2sent:
            self.ind2sent = {}
            try:
                print("try load  " + self.name + " ind2sent index")
                json_file = json.load(open(FOLDER + self.name + "-sentence.json", "r"))
                self.ind2sent = {}
                for k, v in json_file.items():
                    self.ind2sent[int(k)] = v
                print("successfuly  " + self.name + " loaded ", len(self.ind2sent), " entries in ind2sent")
            except:
                print("failed to load  " + self.name + " ind2sent index")
                self.ind2sent = {}

    def add_vector_to_index(self, sentence, id, vector):
        """
        Add a new vector to the index with the id
        :param id:
        :param vector:
        :return:
        """
        self.mutex.acquire()
        try:
            # add to the faiss index
            self.index.add(np.array([vector]))
            faiss.write_index(self.index, FOLDER + self.name + ".index")
            print("Amount of elements in the index:", self.index.ntotal)
            # add to the shadow index
            if self.create_ind2id:
                self.ind2id[self.index.ntotal - 1] = id
                json.dump(self.ind2id, open(FOLDER + self.name + ".json", "w"))
                print("Amount of elements in the ind index:", len(self.ind2id))
            # add to the sentence index
            if self.create_ind2sent:
                self.ind2sent[self.index.ntotal - 1] = sentence
                json.dump(self.ind2sent, open(FOLDER + self.name + "-sentence.json", "w"))
                print("Amount of elements in the shadow index:", len(self.ind2id))
        finally:
            self.mutex.release()

        return {"index": self.index.ntotal - 1,
                "id": id}

    def find_similar(self, sentence_vector, k=10, calc_TSNE=True):
        results = []
        # we want to see 4 nearest neighbors
        D, I = self.index.search(np.array([sentence_vector]), k)

        print(D)
        print(I)
        # print(self.shadow_index)

        for count, ind in enumerate(I[0]):
            # don't go for things that are not in the index
            if ind > 0:
                print("Index", ind)
                print("Count", D[0][count])
                res = {}
                # Add the similarity to the result
                res["similarity"] = round(D[0][count].item(), 2)
                res["r"] = min(0.1, 5 - round(D[0][count].item(), 2))
                # add the sentence to the result if the sentence is stored in the index
                if self.create_ind2sent:
                    res["sentence"] = self.ind2sent[ind]

                # add the id if the id is stored in the index
                if self.create_ind2id:
                    res["id"] = self.ind2id[ind]

                results.append(res)

        # Calculate the T-SNE
        if calc_TSNE:
            vecs = []
            for count, ind in enumerate(I[0]):
                if ind > 0:
                    vecs.append(self.index.reconstruct(int(I[0, count])))

            X_embedded = TSNE(n_components=2).fit_transform(vecs)
            print("RESULTS", results)
            print("TSNE", X_embedded)
            for i, xy in enumerate(X_embedded):
                results[i]['x'] = round(xy[0].item(), 2)
                results[i]['y'] = round(xy[1].item(), 2)

        return results


def add_sentence_to_index(SentenceIndex, document_UUID, sentence, return_vector=False):
    # encode the sentence
    sentence_vector = enc.encode_sentence(sentence)
    # create a hash for a sentence
    sentence_hash = hashlib.md5(str(sentence).encode("utf8")).hexdigest()
    # combine the document uuid and the sentence uuid
    document_and_sentence_uuid = document_UUID + ":" + sentence_hash
    # add the vector to the index
    result = SentenceIndex.add_vector_to_index(sentence, document_and_sentence_uuid, sentence_vector)
    result["sentence"] = sentence
    result["sentence_hash"] = sentence_hash
    result["document_and_sentence_uuid"] = document_and_sentence_uuid
    return result


def add_sentences_to_index(DocumentIndex, SentenceIndex, document_UUID, sentences):
    sentence_results = []
    sentences_vectors = enc.encode_sentences(sentences)
    # iterate over the sentence
    for i, sentence_vector in enumerate(sentences_vectors):
        # create a hash for a sentence
        sentence_hash = hashlib.md5(str(sentences[i]).encode("utf8")).hexdigest()
        # combine the document uuid and the sentence uuid
        document_and_sentence_uuid = document_UUID + ":" + sentence_hash
        result = SentenceIndex.add_vector_to_index(sentences[i], document_and_sentence_uuid, sentence_vector)
        result["sentence"] = sentences[i]
        result["sentence_hash"] = sentence_hash
        result["document_and_sentence_uuid"] = document_and_sentence_uuid
        sentence_results.append(result)
    # Calc document vector
    document_vector = calculate_document_vector(sentences_vectors)
    document_result = add_document_vector_to_index(DocumentIndex, document_UUID, document_UUID, document_vector)
    # Generate the results
    return document_result, document_vector, sentence_results


def calculate_document_vector(sentence_vectors):
    document_vector = np.mean(sentence_vectors, axis=0)
    return document_vector


def add_document_vector_to_index(DocumentIndex, document_name, document_UUID, document_vector):
    return DocumentIndex.add_vector_to_index(document_name, document_UUID, document_vector)


def find_sentences_in_index(SentenceIndex, sentence, k=10):
    sentence_vector = enc.encode_sentence(sentence)
    results = SentenceIndex.find_similar(sentence_vector, k=k)
    return results


def find_document_in_index(DocumentIndex, document_uuid, k=10):
    # TODO Get document and document vector
    document_vector = None
    results = DocumentIndex.find_similar(document_vector, k=k)
    return results
