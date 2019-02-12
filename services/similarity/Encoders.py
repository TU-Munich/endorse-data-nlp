from unicodedata import category
import numpy as np
# import tensorflow as tf
# import tensorflow_hub as hub
from .LASER.source.embed import SentenceEncoder as LaserSentenceEncoder


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

    def encode_sentences(self, lang, sentence_array):
        pass


# g = tf.Graph()
# with g.as_default():
#     text_input = tf.placeholder(dtype=tf.string, shape=[None])
#     en_de_embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
#     embedded_text = en_de_embed(text_input)
#     init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
#     g.finalize()
# # Initialize session.
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# session = tf.Session(config=config, graph=g)
# session.run(init_op)


# Alternative Encoder / Google Universal Sentence Encoder
# class GoogleUse(Encoder):
#    def __init__(self):
#        super(GoogleUse, self).__init__()
#        self.name = "Google Universal Sentence Encoder"
#        self.short_name = "google-use"
#
#    def encode_sentences(self, worklist):
#        # Define result and  batchsize
#        embeddings = None
#        BATCH_SIZE_ENCODER = 512
#        # Iterate over the stuff
#        for i in range(0, len(worklist), BATCH_SIZE_ENCODER):
#            print(i, len(worklist))
#            batch = worklist[i:i + BATCH_SIZE_ENCODER]  # the result might be shorter than batchsize at the end
#            # do stuff with batch
#            res = session.run(embedded_text, feed_dict={text_input: batch})
#            if embeddings is None:
#                embeddings = res
#            else:
#                embeddings = np.append(embeddings, res, axis=0)
#
#        return embeddings
#
#    def encode_sentence(self, sentence):
#        res = session.run(embedded_text, feed_dict={text_input: [sentence]})
#        return res[0]


class LASEREncoder(Encoder):
    def __init__(self, path, verbose=False, stable=True, cpu=True, max_sentences=100, max_tokens=12000,
                 buffer_size=max(10000, 1)):
        super(LASEREncoder, self).__init__()
        self.name = "LASER"
        self.short_name = "laser"
        # print(self.name)
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

    def encode_sentences(self, sentences_array):
        """
        Encode sentences
        """
        sentence_embeddings = self.model.encode_sentences(sentences_array)
        return sentence_embeddings
