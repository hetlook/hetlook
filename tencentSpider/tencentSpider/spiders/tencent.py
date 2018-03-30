# -*- coding: utf-8 -*-
import scrapy
from tencentSpider.items import TencentspiderItem
import re


class TencentSpider(scrapy.Spider):
    name = 'tencent1'
    allowed_domains = ['hr.tencent.com']
    url= 'http://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self,response):
        for each in response.xpath('//*[@class="even"]|//*[@class="odd"]'):
	    item = TencentspiderItem()
	    name = each.xpath('./td[1]/a/text()').extract()[0]
	    detailLink = each.xpath('./td[1]/a/@href').extract()[0]
	    positionInfo = each.xpath('./td[2]/text()').extract()
	    peopleNumber = each.xpath('./td[3]/text()').extract()
	    workLocation = each.xpath('./td[4]/text()').extract()
	    publishTime = each.xpath('./td[5]/text()').extract()
            item['name'] = name
	    item['detailLink'] = detailLink
	    item['positionInfo'] = positionInfo
            item['peopleNumber'] = peopleNumber
	    item['workLocation'] = workLocation
            item['publishTime'] = publishTime
	    yield item

        if self.offset<3810:
            self.offset += 10
        url = self.url + str(self.offset)
            

        yield scrapy.Request(url, callback = self.parse)
