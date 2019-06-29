# @Author:王文龙

# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import urllib
import re


class NewsspiderSpider(scrapy.Spider):
    name = 'newsSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://vip.stock.finance.sina.com.cn/corp/view/vCB_BulletinGather.php?page=2']

    def parse(self, response):
        #分组
        tr_list = response.xpath("//table[@class='body_table']/tbody/tr")
        print("**"*40)

       # print(tr_list)

        for tr in tr_list:
            item =NewsItem()
            item["title"]=tr.xpath("./th/a[1]/text()").extract_first()
            item["name"]=item["title"].split('：')[0]
            item["href"] = tr.xpath("./th/a[1]/@href").extract_first()
            #item["href"] = {"http://vip.stock.finance.sina.com.cn" + tr.xpath("./th/a[1]/@href").extract_first()}

            #补充url,一定要判断，慢慢的血泪史啊！！！！！
            if item["href"] is not None:
                item["href"] = urllib.parse.urljoin(response.url,item["href"])
            print(item)

            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )

            #翻页
        next_url = urllib.parse.urljoin(response.url, response.xpath("//a[text()='下一页']/@href").extract_first())
        if next_url is not None:
            yield scrapy.Request(
                    next_url,
                    callback=self.parse
                )

    #二层爬取页面数据
    def parse_detail(self, response):  #处理详情页
        item = response.meta["item"]
        item["content"]=response.xpath("//div[@id='content']/p/text()").extract()
        #item["name"] = response.xpath("//table[@class='hqContent']/tbody/tr/th/h5/text()").extract()
        print(item)
        yield item
