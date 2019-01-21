#!/bin/bash
# start.sh

set -e

# This script assumes that Logstash will become active once Elasticsearch has booted up properly.
# Once Logstash has created a successful connection to Elasticsearch, and the API is running on port 9600
# We can imply that the connection to Elasticsearch has successfully started.
# Once Elasticsearch is properly running, the endorse-data-nlp backend can start without timing issues in the connection

is_not_connected=0
PORT=9600
HOST=http://logstash

while [ $is_not_connected -lt 1 ];
do
    response=$(curl -I $HOST:$PORT 2> /dev/null | head -n 1 | cut -d ' ' -f 2)
    if [ "$response" == "200" ]; then
      is_not_connected=$(( is_not_connected + 1 ))
      echo "Logstash on port $PORT is ready! Connection to elasticsearch is possible now!"
    else
      echo "Connection to Elasticsearch on port 9200 booting up!"
      sleep 10;
    fi
done

python main.py
