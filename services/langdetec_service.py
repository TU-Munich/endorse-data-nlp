from langdetect import detect


def doc_lang(document):
    return detect(document)
