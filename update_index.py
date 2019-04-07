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


if __name__ == '__main__':
    response = requests.delete(BASE_URL)
    if response.status_code == 200:
        input("Deleted all postings")
    else:
        input('Error in deleting postings')

    with open("craigslist.txt") as craigslist:
        for posting_str in craigslist.readlines():
            add_to_index(posting_str)

    with open("theladders.txt") as theladders:
        for posting_str in theladders.readlines():
            add_to_index(posting_str)
