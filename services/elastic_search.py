import os

from elasticsearch import Elasticsearch

ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

# es = Elasticsearch()
es = None
if ES_USERNAME != None and ES_PASSWORD != None:
    es = Elasticsearch(
        ES_HOST,
        http_auth=(ES_USERNAME, ES_PASSWORD),
        scheme="http",
    )
else:
    es = Elasticsearch(
        ES_HOST,
    )
