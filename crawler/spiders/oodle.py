# -*- coding: utf-8 -*-
import datetime
import re

import scrapy
from scrapy.responsetypes import Response

from crawler.spiders.common import approximate_datetime

re_non_alnum = re.compile(r'[^\w\s]')


class CraigslistSpider(scrapy.Spider):
    name = 'oodle'
    allowed_domains = ['jobs.oodle.com']
    start_urls = ['https://jobs.oodle.com/careers/norfolk-va/']

    def parse(self, response: Response):
        for result_row in response.css('li.listing'):
            date_str = ' '.join(
                ' '.join(x.strip() for x in result_row.css('span.posted-on ::text').getall() if x.strip()).split(' ')[
                :3])
            result = {
                'title': result_row.css('span.listing-title a.title-link::text').get(),
                'site': 'oodle',
                'url': response.urljoin(result_row.css('span.listing-title a.title-link::attr(href)').get()),
                'datePosted': approximate_datetime(datetime.datetime.now(), date_str),
                'description': ' '.join(result_row.css('div.listing-main div.listing-body *::text').getall()),
                'hiredBy': ' '.join(result_row.css('div.listing-attributes *::text').getall()),
            }
            yield result

        next_page = response.css('div#pagination a#pagination-next-container::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
