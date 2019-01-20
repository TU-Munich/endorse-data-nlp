import time
import datetime
from services.elastic_search import es


def init_initial_project(es: es):
    connected = False

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

    while not connected:
        time.sleep(10)
        try:
            es.info()
            connected = True
        except ConnectionError:
            print("Elasticsearch not available yet, trying again in 2s...")
            time.sleep(2)

    es.index(index="projects-index", doc_type='project', id="hillary", body=test)
