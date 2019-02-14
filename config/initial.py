import datetime
from services.elastic_search import es


def init_initial_project():
    """
    Create the initial project which is hillary's emails
    :param es:
    :return:
    """
    print("[INITIAL] Create initial project")
    test = {
        "name": "Hillary Clinton Emails",
        "date": datetime.datetime.now(),
    }
    es.index(index="projects-index", doc_type='project', id="hillary", body=test)

    test = {
        "name": "Reuters Mexico Sentiment",
        "date": datetime.datetime.now(),
    }
    es.index(index="projects-index", doc_type='project', id="reuters-mexico", body=test)

    test = {
        "name": "SEBA Master Lecture",
        "date": datetime.datetime.now(),
    }
    es.index(index="projects-index", doc_type='project', id="seba-master", body=test)

    test = {
        "name": "Lecture",
        "date": datetime.datetime.now(),
    }
    es.index(index="projects-index", doc_type='project', id="lecture", body=test)

    test = {
        "name": "Student Similarity",
        "date": datetime.datetime.now(),
    }
    es.index(index="projects-index", doc_type='project', id="student-similarity", body=test)
