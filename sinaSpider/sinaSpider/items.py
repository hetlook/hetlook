# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SinaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #大标题 和url
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    #小类标题 和子url
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()
    
    #小类目录存储路径
    subFilename = scrapy.Field()

    #小类下子链接
    sonUrls = scrapy.Field()

    #文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()
