# -*- coding: utf-8 -*-
import scrapy
from scrapy.responsetypes import Response


class CraigslistSpider(scrapy.Spider):
    name = 'theladders'
    allowed_domains = ['www.theladders.com']
    start_urls = ['https://www.theladders.com/jobs/virginia-jobs']

    def parse(self, response: Response):
        for result_row in response.css('div.job-card-text-container'):
            result = {
                'title': result_row.css('a.job-card-title::text').get(),
                'site': 'theladders',
                'url': response.urljoin(result_row.css('a.job-card-title::attr(href)').get()),
                'datePosted': None,
                'description': result_row.css('p.job-card-description::text').get(),
                'hiredBy': result_row.css('div.job-card-sub-header *::text').get(),
            }
            yield result

        next_page = response.css('a.pagination__item-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
