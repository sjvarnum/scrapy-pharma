import scrapy


class BeckershospitalreviewSpiderSpider(scrapy.Spider):
    name = 'beckers'
    allowed_domains = ['beckershospitalreview.com']
    start_urls = ['https://beckershospitalreview.com/']

    def parse(self, response):
        pass
