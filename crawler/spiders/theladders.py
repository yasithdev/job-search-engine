# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.responsetypes import Response

from crawler.spiders.common import approximate_datetime


class CraigslistSpider(scrapy.Spider):
    name = 'theladders'
    allowed_domains = ['www.theladders.com']
    start_urls = ['https://www.theladders.com/jobs/virginia-jobs']

    def parse(self, response: Response):
        for result_row in response.css('div.job-card-text-container'):
            date_str = ' '.join(
                ' '.join(x.strip() for x in result_row.css('p.posted-date ::text').getall() if x.strip()).split(' ')[
                1:4])
            result = {
                'title': result_row.css('a.job-card-title::text').get(),
                'site': 'theladders',
                'url': response.urljoin(result_row.css('a.job-card-title::attr(href)').get()),
                'datePosted': approximate_datetime(datetime.datetime.now(), date_str),
                'description': result_row.css('p.job-card-description::text').get(),
                'hiredBy': result_row.css('div.job-card-sub-header *::text').get(),
            }
            yield result

        next_page = response.css('a.pagination__item-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
