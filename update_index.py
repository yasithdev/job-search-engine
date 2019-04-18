#!/usr/bin/env python3

# REQUIREMENTS
# 1. Elasticsearch running on port 9200

import codecs
# importing the json library
import json
import re
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
    posting_id = md5(posting['url'].encode('utf-8')).hexdigest()
    posting_str = json.dumps(posting, ensure_ascii=False)
    # try creating first
    response = requests.put(url=make_url(posting_id, True), data=posting_str.encode('utf-8'), headers=HEADERS)
    if response.status_code == 201:
        print('Added Document: ' + posting_id)
    elif response.status_code == 409:
        requests.put(url=make_url(posting_id), data=posting_str.encode('utf-8'), headers=HEADERS)
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
                        "boost": 3
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
                        "boost": 2
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


allowed_cities = r'(?i)(norfolk|chesapeake|suffolk|virginia\sbeach)[^.]'


def filter_documents():
    d = []
    with codecs.open("data/craigslist.txt", "r", "utf-8") as craigslist:
        for posting_str in craigslist.readlines():
            # Only select records that contain the term norfolk in them
            if re.search(allowed_cities, posting_str) is not None:
                d.append(json.loads(posting_str, encoding='utf-8'))

    with codecs.open("data/theladders.txt", "r", "utf-8") as theladders:
        for posting_str in theladders.readlines():
            # Only select records that contain the term norfolk in them
            if re.search(allowed_cities, posting_str) is not None:
                d.append(json.loads(posting_str, encoding='utf-8'))

    with codecs.open("data/oodle.txt", "r", "utf-8") as oodle:
        for posting_str in oodle.readlines():
            # Only select records that contain the term norfolk in them
            if re.search(allowed_cities, posting_str) is not None:
                d.append(json.loads(posting_str, encoding='utf-8'))
    return d


if __name__ == '__main__':
    drop_index()
    update_index_properties()
    documents = filter_documents()
    input('%d documents found' % len(documents))
    with codecs.open('data.json', 'w', encoding='utf=8') as out:
        out.write(json.dumps(documents, ensure_ascii=False))
    for doc in documents:
        add_to_index(doc)
