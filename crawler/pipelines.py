# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import re

from scrapy.exceptions import DropItem

re_nrt = re.compile(r'\\[nrt]')
re_space = re.compile(r'\s+')
re_non_alnum = re.compile(r'([^\w\s]|\s)+')


def trim_spaces(t):
    return re_space.sub(' ', t).strip()


def trim_description(d):
    return re_non_alnum.sub(' ', trim_spaces(d)).strip()


class CrawlerPipeline(object):

    def __init__(self) -> None:
        super().__init__()
        self.file = None

    def open_spider(self, spider):
        name = spider.name
        self.file = codecs.open("data/" + spider.name + '.txt', 'w', 'utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        item['description'] = trim_description(item['description']) if item['description'] else None
        item['title'] = trim_spaces(item['title']) if item['title'] else None
        item['hiredBy'] = trim_spaces(item['hiredBy']) if item['hiredBy'] else None
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['url'])
            return item
