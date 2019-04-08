#!/usr/bin/env python3

# REQUIREMENTS
# 1. Elasticsearch running on port 9200

# importing the json library
import json
from hashlib import md5

# importing the requests library
import requests

# define base url and headers
BASE_URL = "http://localhost:9200/postings"
HEADERS = {"Content-Type": "application/json"}


def make_url(posting_id: str, create: bool = False):
    return BASE_URL + "/_doc/" + posting_id + ("/_create" if create else "")


def add_to_index(posting):
    # calculate id for posting
    posting_id = md5(json.loads(posting)['url'].encode()).hexdigest()
    # try creating first
    response = requests.put(url=make_url(posting_id, True), data=posting, headers=HEADERS)
    if response.status_code == 201:
        print('Added Document: ' + posting_id)
    elif response.status_code == 409:
        requests.put(url=make_url(posting_id), data=posting, headers=HEADERS)
        print('Updated Document: ' + posting_id)
    else:
        input(str(response.status_code) + ': ' + str(response.json()))


def drop_index():
    response = requests.delete(BASE_URL)
    if response.status_code == 200:
        input("Deleted all postings")
    else:
        input('Error in deleting postings')


def update_index_properties():
    data = {
        "mappings": {
            "_doc": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "text_analyzer",
                        "search_analyzer": "text_analyzer",
                        "boost": 2
                    },
                    "site": {
                        "type": "keyword"
                    },
                    "url": {
                        "type": "keyword"
                    },
                    "datePosted": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm"
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "text_analyzer",
                        "search_analyzer": "text_analyzer",
                    },
                    "hiredBy": {
                        "type": "text"
                    }
                }
            }
        },
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "analysis": {
                "analyzer": {
                    "text_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stemmer_filter"]
                    }
                },
                "filter": {
                    "stemmer_filter": {
                        "type": "stemmer",
                        "name": "english"
                    }
                }
            }
        }
    }
    response = requests.put(BASE_URL, data=json.dumps(data), headers=HEADERS)
    if response.status_code == 200:
        input("Updated index properties")
    else:
        print(response)
        input('Error in updating index properties')


def add_documents():
    with open("data/craigslist.txt") as craigslist:
        for posting_str in craigslist.readlines():
            add_to_index(posting_str)

    with open("data/theladders.txt") as theladders:
        for posting_str in theladders.readlines():
            add_to_index(posting_str)

    with open("data/oodle.txt") as oodle:
        for posting_str in oodle.readlines():
            add_to_index(posting_str)


if __name__ == '__main__':
    drop_index()
    update_index_properties()
    add_documents()
