import json

import scrapy
from scrapy.crawler import CrawlerProcess


class FierceBiotechSpider(scrapy.Spider):
    name = 'fiercebiotech'

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'COOKIES_ENABLED': False,
    }

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    }

    def start_requests(self):
        yield scrapy.Request('https://www.fiercebiotech.com/api/v1/fronts/node?_format=json&page=0&sectionId=137&heroArticleCount=5&sponsoredCount=0&limit=100')

    def parse(self, response):
        response_json = response.json()
        data = response_json['data']
        page_count = response_json['pager']['pages']['total']
        total_count = response_json['pager']['total']

        for article in data:
            yield {
                'Date': article['publishedDate'].split('T')[0],
                'Source': article['primaryTaxonomy']['label'],
                'Title': article['title'],
                'Link': article['uri']
            }

        page_count = round((total_count/100)+1)
        for page_num in range(1, page_count):
            yield(scrapy.Request(f'https://www.fiercebiotech.com/api/v1/fronts/node?_format=json&page={page_num}&sectionId=137&heroArticleCount=5&sponsoredCount=0&limit=100',
                                 callback=self.parse))

process = CrawlerProcess(settings={
    'FEEDS': {
        'FireceBiotech.csv': {'format': 'csv'}
    },
})

process.crawl(FierceBiotechSpider)
process.start()
