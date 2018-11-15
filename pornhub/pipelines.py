# -*- coding: utf-8 -*-
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
import re


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PornhubPipeline(object):
    def process_item(self, item, spider):
        return item


class GetVideoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for url in item['file_urls']:
            print(url)
            print(item['name'])
            yield Request(url, meta={'meta': item['name']})

    def file_path(self, request, response=None, info=None):
        name = request.meta['meta']
        name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        return u'{0}'.format(name)
