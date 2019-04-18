# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.responsetypes import Response


# noinspection PyBroadException
def approximate_datetime(time, relative):
    # using simplistic year (no leap months are 30 days long.
    # WARNING: 12 months != 1 year
    unit_mapping = [('mic', 'microseconds', 1),
                    ('millis', 'microseconds', 1000),
                    ('sec', 'seconds', 1),
                    ('day', 'days', 1),
                    ('week', 'days', 7),
                    ('mon', 'days', 30),
                    ('year', 'days', 365)]
    try:
        tokens = relative.lower().split(' ')
        past = False
        if tokens[-1] == 'ago':
            past = True
            tokens = tokens[:-1]
        elif tokens[0] == 'in':
            tokens = tokens[1:]

        units = dict(days=0, seconds=0, microseconds=0)
        # we should always get pairs, if not we let this die and throw an exception
        while len(tokens) > 0:
            value = tokens.pop(0)
            if value == 'and':  # just skip this token
                continue
            else:
                value = float(value)

            unit = tokens.pop(0)
            for match, time_unit, time_constant in unit_mapping:
                if unit.startswith(match):
                    units[time_unit] += value * time_constant
            # negate timedelta if in past
            if past:
                for key in units.keys():
                    units[key] = -units[key]
        return (time + datetime.timedelta(**units)).strftime()
    except Exception:
        return None


class CraigslistSpider(scrapy.Spider):
    name = 'oodle'
    allowed_domains = ['jobs.oodle.com']
    start_urls = ['https://jobs.oodle.com/careers/norfolk-va/']

    def parse(self, response: Response):
        for result_row in response.css('li.listing'):
            result = {
                'title': result_row.css('span.listing-title a.title-link::text').get(),
                'site': 'oodle',
                'url': response.urljoin(result_row.css('span.listing-title a.title-link::attr(href)').get()),
                'datePosted': approximate_datetime(datetime.datetime.now(), result_row.css('*.posted-on > span *::text').get()),
                'description': ' '.join(result_row.css('div.listing-main div.listing-body *::text').getall()),
                'hiredBy': ' '.join(result_row.css('div.listing-attributes *::text').getall()),
            }
            yield result

        next_page = response.css('div#pagination a#pagination-next-container::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
