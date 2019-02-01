from unicodedata import category
import numpy as np
import tensorflow as tf
import pickle


# https://github.com/UKPLab/arxiv2018-xling-sentence-embeddings/blob/master/model/sentence_embeddings.py

def gen_mean(vals, p):
    p = float(p)
    return np.power(
        np.mean(
            np.power(
                np.array(vals, dtype=complex),
                p),
            axis=0),
        1 / p
    )


# https://github.com/UKPLab/arxiv2018-xling-sentence-embeddings/blob/master/model/sentence_embeddings.py
operations = dict([
    ('mean', (lambda word_embeddings: [np.mean(word_embeddings, axis=0)], lambda embeddings_size: embeddings_size)),
    ('max', (lambda word_embeddings: [np.max(word_embeddings, axis=0)], lambda embeddings_size: embeddings_size)),
    ('min', (lambda word_embeddings: [np.min(word_embeddings, axis=0)], lambda embeddings_size: embeddings_size)),
    ('p_mean_2',
     (lambda word_embeddings: [gen_mean(word_embeddings, p=2.0).real], lambda embeddings_size: embeddings_size)),
    ('p_mean_3',
     (lambda word_embeddings: [gen_mean(word_embeddings, p=3.0).real], lambda embeddings_size: embeddings_size)),
])


# Encoder
class Encoder():
    def __init__(self):
        self.name = "Default Encoder"
        self.short_name = "default"
        self.file_path = "./data/amazon-reviews/"
        self.prefix = "amz-"
        self.postfix = ""
        self.postfix_pickle = ".pickle"
        self.postfix_txt = ".txt"
        pass

    def clean_sentence(self, s, lower=True):
        if lower:
            s = s.lower()
        s = s.replace("_", " ")
        s = s.replace(":", " ")
        s = ''.join(ch for ch in s if category(ch)[0] != 'P').strip()
        s = " ".join(s.split())
        return s

    def clear_memory(self):
        # clear all
        tf.reset_default_graph()
        # cuda.select_device(0)
        # do tf stuff
        # cuda.close()
        # the memory was released here!
        # cuda.select_device(0)
        # to tf stuff -> caused an OOM

    def save_as_pickle(self, lang, x):
        np.savetxt(
            self.file_path + self.prefix + lang.lower() + "-x-" + self.short_name + self.postfix + self.postfix_txt, x,
            delimiter=',')  # X is an array
        # save encoded
        path = self.file_path + self.prefix + lang.lower() + "-x-" + self.short_name + self.postfix + self.postfix_pickle
        pickle.dump(x, open(path, 'wb'))
        print("saved: " + path)

    def encode_sentences(self, lang, sentence_array):
        pass


import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['LASER'] = dir_path
os.environ['LASER'] += "/LASER"
print(os.environ['LASER'])

from LASER.source.embed import SentenceEncoder as LaserSentenceEncoder




class LASEREncoder(Encoder):
    def __init__(self, path, verbose=False, stable=True, cpu=True, max_sentences=100, max_tokens=12000,
                 buffer_size=max(10000, 1)):
        super(LASEREncoder, self).__init__()
        self.name = "LASER"
        self.short_name = "laser"
        print(self.name)
        self.path = path
        # init model
        self.model = LaserSentenceEncoder(self.path,
                                          max_sentences=max_sentences,
                                          max_tokens=max_tokens,
                                          sort_kind='mergesort' if stable else 'quicksort',
                                          cpu=cpu)

    def word_in_model(self, word):
        """
        check if a word is in the model
        """
        # only lower words
        word = word.lower()
        if word in self.model:
            return True
        else:
            return False

    def embeddings_dimensionality(self):
        """
        Get the domensionality of the model
        """
        return 1024

    def encode_sentence(self, sentence_string):
        """
        Encode a single sentence
        partially from: https://github.com/UKPLab/arxiv2018-xling-sentence-embeddings/blob/master/model/sentence_embeddings.py
        """
        result = self.model.encode_sentences([sentence_string])
        return result[0]

    def encode_sentences(self, lang, sentences_array):
        """
        Encode sentences
        """
        sentence_embeddings = self.model.encode_sentences(sentences_array)
        return sentence_embeddings
