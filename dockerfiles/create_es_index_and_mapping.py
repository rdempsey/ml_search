#!/usr/bin/env python
# encoding: utf-8

import time
import requests
import json


def add_es_indexes():
    index_data = {
        "settings": {
            "index": {
                "number_of_shards": 5,
                "number_of_replicas": 0
            }
        }
    }

    # Add the collection rules index
    try:
        print("Adding the collection rules index to ElasticSearch")
        r = requests.put("http://localhost:9200/collection-rules", data=json.dumps(index_data))
        if r.status_code == requests.codes.ok:
            print("Collection Rules index added to ElasticSearch")
        else:
            print("Unable to add the collection rules index to ElasticSearch. Response: {}".format(r))
    except Exception as err:
        print("ERROR: Unable to add the collection rules index to ElasticSearch: {}".format(err))

    # Add the index
    try:
        print("Adding the index to ElasticSearch")
        r = requests.put("http://localhost:9200/smdata", data=json.dumps(index_data))
        if r.status_code == requests.codes.ok:
            print("SMData index added to ElasticSearch")
        else:
            print("Unable to add the SMData index to ElasticSearch. Response: {}".format(r))
    except Exception as err:
        print("ERROR: Unable to add the collection rules index to ElasticSearch: {}".format(err))


def add_index_patterns():
    print("Adding logs index patterns to ElasticSearch")

    try:
        print("Adding logs index")
        x2 = {
            "title": "logs-*",
            "timeFieldName": "@timestamp",
            "fields": "[{\"name\":\"_index\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"level\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"logger\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"message\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"tags\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"path\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"@timestamp\",\"type\":\"date\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"@version\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"host\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"_source\",\"type\":\"_source\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"timestamp\",\"type\":\"date\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"content.public_format\",\"type\":\"boolean\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"content.status\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":true,\"analyzed\":false,\"doc_values\":true},{\"name\":\"_id\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"_type\",\"type\":\"string\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false},{\"name\":\"_score\",\"type\":\"number\",\"count\":0,\"scripted\":false,\"indexed\":false,\"analyzed\":false,\"doc_values\":false}]"
        }
        r = requests.put("http://localhost:9200/.kibana/index-pattern/logs-*", data=json.dumps(x2))
        if 200 <= r.status_code <= 300:
            print("Logs index added to ElasticSearch")
        else:
            print("Unable to add logs index to ElasticSearch. Response: {}".format(r))
    except Exception as err:
        print("ERROR: Unable to add the logs index to ElasticSearch: {}".format(err))

    try:
        print("Adding logs index to the config")
        x = {
            "buildNum": 10148,
            "defaultIndex": "logs-*"
        }
        r = requests.put("http://localhost:9200/.kibana/config/4.6.2", data=json.dumps(x))
        if 200 <= r.status_code <= 300:
            print("Logs index added to the ElasticSearch config")
        else:
            print("Unable to add logs index to the ElasticSearch config. Response: {}".format(r))
    except Exception as err:
        print("ERROR: Unable to add the logs index to the ElasticSearch config: {}".format(err))


es_status_page = "http://localhost:9200/"
es_status = False

print("Adding the collection rules index and mapping to ElasticSearch")

while es_status is False:
    # Check to see if we can get the ES status page
    try:
        ep_status_response = requests.get(es_status_page)
        # If we can get to the ES page let's roll
        if ep_status_response.status_code == requests.codes.ok:
            es_status = True
            # Add the indexes
            add_es_indexes()
            # Add the index patterns
            add_index_patterns()
        else:
            print("ElasticSearch isn't available yet. Waiting 15 seconds...")
            time.sleep(15)
    except Exception as e:
        print("ElasticSearch isn't available yet. Waiting 15 seconds...")
        time.sleep(15)
