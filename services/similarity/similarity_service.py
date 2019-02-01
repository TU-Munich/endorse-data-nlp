import os
import numpy as np
from services.similarity.Encoders import LASEREncoder
from services.similarity.Encoders import operations

encoder_path = os.environ['LASER'] + "/models/bilstm.93langs.2018-12-26.pt"
# bpe_codes = os.environ['LASER']+"/models/bilstm.93langs.2018-12-26.pt"
enc = LASEREncoder(encoder_path)


def create_document_vector(sentences_vectors, chosen_operations="mean"):
    """
    create a documents vector based on sentence vectors
    :param sentences_vectors:
    :param chosen_operations:
    :return:
    """
    sentences_vectors_array = []
    sentences_vectors_array += operations[chosen_operations][0](sentences_vectors)
    result = np.concatenate(
        sentences_vectors_array,
        axis=0
    )
    return result


def create_sentences_vectors(sentences):
    """
    Create a sentence vector
    :param sentences:
    :return:
    """
    results = enc.encode_sentenceses(sentences)
    return results


def create_sentence_vector(sentence):
    """
    :param sentence:
    :return:
    """
    results = enc.encode_sentence(sentence)
    return results
