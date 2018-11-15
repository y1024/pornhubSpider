# -*- coding: utf-8 -*-
import scrapy
from pornhub.items import PornhubItem
from scrapy.selector import Selector
import json
import re


class PornhubSpiderSpider(scrapy.Spider):
    name = 'pornhub_spider'
    allowed_domains = ['pornhub.com']
    start_urls = ['https://pornhub.com/video']

    def parse(self, response):
        ul = response.css('#videoCategory')
        for li in ul:
            content_url = li.css('.videoPreviewBg a::attr(href)').extract_first()
            next_page_url = response.css('.firstPage li.page_next a::attr(href)').extract_first()
            if next_page_url is not None:
                yield response.follow(next_page_url, callback=self.parse)
            yield scrapy.Request(response.urljoin(content_url), callback=self.content)

    def content(self, response):
        print(response)
        item = PornhubItem()
        info = re.search('var flashvars(.*)=(.*?);\n', Selector(response).extract()).group()
        result = json.loads(re.findall('(\{.*?\});', info)[0])
        mediaDefinitions = result.get('mediaDefinitions')
        count = len(mediaDefinitions)
        for i in range(0, count):
            videoUrl = mediaDefinitions[i]['videoUrl']
            if videoUrl != '':
                item['file_urls'] = [videoUrl]
        item['name'] = result.get('video_title')
        yield item