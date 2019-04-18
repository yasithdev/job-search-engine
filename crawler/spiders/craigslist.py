# -*- coding: utf-8 -*-
import scrapy
from scrapy.responsetypes import Response


class CraigslistSpider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['norfolk.craigslist.org']
    start_urls = ['https://norfolk.craigslist.org/d/jobs/search/jjj']

    @staticmethod
    def parse_content(response):
        item = response.meta['item']
        item['description'] = ' '.join(
            response.xpath('//section[@id="postingbody"]//text()[normalize-space()]').getall())
        return item

    def parse(self, response: Response):
        for result_row in response.css('li.result-row'):
            item = {
                'title': result_row.css('a.result-title::text').get(),
                'site': 'craigslist',
                'url': response.urljoin(result_row.css('a.result-title::attr(href)').get()),
                'datePosted': result_row.css('time.result-date::attr(datetime)').get(),
                'description': None,  # description added in sub crawl
                'hiredBy': None,
            }
            request = scrapy.Request(item['url'], callback=self.parse_content)
            request.meta['item'] = item
            yield request

        next_page = response.css('.paginator a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
