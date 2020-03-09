import scrapy
from ..items import VideosextractionItem

class VideosextractionSpider(scrapy.Spider):
    name = "videos"
    start_urls = [
        'https://www.radiocity.in/film/watch-online-video/Judwaa-2-Official-Trailer/2866'
    ]

    def parse(self, response):
        items = VideosextractionItem()
        #allvideos = response.css('li+ .col-xs-12  a::attr(href)').extract()
        allvideos = response.css('#video_player iframe::attr(src)').extract()
        allvideos = [x for x in allvideos]
        allvideos = '\n'.join(allvideos)
        items['allvideos'] = allvideos
        yield items