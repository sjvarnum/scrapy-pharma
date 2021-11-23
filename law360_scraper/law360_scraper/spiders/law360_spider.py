import datetime
import scrapy


class Law360Spider(scrapy.Spider):
    name = 'law360'
    allowed_domains = ['www.law360.com']
    start_urls = [
        'https://www.law360.com/lifesciences',
        'https://www.law360.com/appellate', 'https://www.law360.com/ip',
        'https://www.law360.com/health',
        'https://www.law360.com/access-to-justice',
        'https://www.law360.com/bankruptcy',
        'https://www.law360.com/securities',
        'https://www.law360.com/competition',
        'https://www.law360.com/employment',
        'https://www.law360.com/whitecollar',
        'https://www.law360.com/legalindustry',
        'https://www.law360.com/access-to-justice'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY':
        1,
        'AUTOTHROTTLE_ENABLED':
        True,
        'AUTOTHROTTLE_DEBUG':
        True,
        'USER_AGENT':
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    }

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    }

    def parse(self, response):
        for articles in response.css('li.hnews.hentry'):
            try:
                date = articles.css(
                    "li.hnews.hentry > span.updated.dtstamp::text").get()
                date = datetime.datetime.strptime(date, '%B %d, %Y')
                date = datetime.datetime.strftime(date, '%Y-%m-%d')
                source = self.name
                channel = articles.css(
                    "a.url.entry-title").attrib["href"].split('/')[1]
                title = articles.css("a.url.entry-title::text").get()
                link = articles.css("a.url.entry-title").attrib["href"]
                link = response.urljoin(link)

                yield {
                    'date': date,
                    'source': source,
                    'channel': channel,
                    'title': title,
                    'link': link
                }
            except (TypeError, KeyError):
                None

        try:
            next_page = response.css('.next > a')
            if next_page is not None:
                next_page = response.css('.next > a').attrib['href']
                yield response.follow(next_page, callback=self.parse)
        except KeyError:
            print('End of pages')
