import os
from services.similarity.Encoders import LASEREncoder

encoder_path = os.environ['LASER'] + "/models/bilstm.93langs.2018-12-26.pt"
# bpe_codes = os.environ['LASER']+"/models/bilstm.93langs.2018-12-26.pt"
encoder_laser = LASEREncoder(encoder_path)


def create_document_vector():
    pass


def create_sentence_vector(sentence):
    pass

