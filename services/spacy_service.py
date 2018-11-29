from textacy.io import spacy

nlp_en = spacy.load('en')
nlp_de = spacy.load('de')


def doc_clean(raw):
    clean = raw.strip(' \t\n\r')
    return clean


def doc_pos(doc):
    """
    Take a spacy doc object
    extract all necessary information
    from the part of speech subsection
    """
    pos = []
    for token in doc:
        pos.append({
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop,
        })
    return pos


def doc_ner(doc):
    """
    Take a spacy doc object
    extract all necessary information
    from the named entity subsection
    """
    ner = []
    for ent in doc.ents:
        ner.append(
            {
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_
            })
    return ner


def doc_tokenize(doc):
    """
    Take a spacy doc object
    split the document into sentences
    """
    sentences = []
    for sent in doc.sents:
        sentences.append(sent.text)
    return sentences


def doc_spacy(lang, clean):
    if lang == "de":
        return nlp_de(clean)
    else:
        return nlp_en(clean)
