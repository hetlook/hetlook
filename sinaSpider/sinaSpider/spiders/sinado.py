# -*- coding: utf-8 -*-
import time
import scrapy
from sinaSpider.items import SinaspiderItem
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SinaSpider(scrapy.Spider):
    name = 'sinatime'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']
    def parse(self, response):
        items = []
        #parent
        parentUrls = response.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()
        parentTitle = response.xpath("//div[@id=\"tab01\"]/div/h3/a/text()").extract()
        #little
        subUrls  = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/text()').extract()
        #crawl parent
        for i in range(0, len(parentTitle)):

            parentFilename = "./Data/" + parentTitle[i]
    
            if(not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            for j in range(0,len(subUrls)):
                item = SinaspiderItem()

                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]
       
                if_belong = subUrls[j].startswith(item['parentUrls'])
                if(if_belong):
                    subFilename = parentFilename + '/' + subTitle[j]
                    if(not os.path.exists(subFilename)):
                        os.makedirs(subFilename)
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] = subTitle[j]
                    item['subFilename'] = subFilename

                    items.append(item)
            for item in items:
                yield scrapy.Request( url = item['subUrls'], meta={'meta_1':item}, callback=self.second_parse)

    def second_parse(self, response):
        meta_1 = response.meta['meta_1']
    
        sonUrls = response.xpath('//a/@href').extract()
    
        items = []
        for i in range(0,len(sonUrls)):
           # print('*'*50)
           # print(sonUrls[i])
           # print('*'*50)
          #  if_belong =  sonUrls[i].startswith(meta_1['parentUrls'])
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])
            if(if_belong):
                item = SinaspiderItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)
        for item in items:
            yield scrapy.Request(url=item['sonUrls'],meta={'meta_2':item},callback=self.detail_parse)
    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ""
        head = response.xpath('//h1[@id=\"main_title\"]/text()')
        content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()
        
        for content_one in content_list:
            content += content_one
        item['head'] = head
        item['content'] = content

        yield item
