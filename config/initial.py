import datetime
from elasticsearch import Elasticsearch


def init_initial_project(es: Elasticsearch):
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
