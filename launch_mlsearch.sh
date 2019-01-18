#!/usr/bin/env bash
docker-compose -f docker-compose.yml up --build --force-recreate -d
python dockerfiles/create_es_index_and_mapping.py
echo Adding the collection rules template to ElasticSearch
curl -XPUT http://localhost:9200/_template/ -T dockerfiles/collection-rules-template.json
echo Adding the template to ElasticSearch
curl -XPUT http://localhost:9200/_template/ -T dockerfiles/template.json