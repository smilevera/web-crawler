#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-05-26 11:03:11
# Project: douban

from pyspider.libs.base_handler import *




class Handler(BaseHandler):
    crawl_config = {
    }
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://movie.douban.com/tag/2016%20%E4%B8%AD%E5%9B%BD?type=',callback=self.list_page)

    @config(age=10*24*60*60)
    def list_page(self,response):
        for each in response.doc('td > .pl2 > a').items():
            self.crawl(each.attr.href,callback=self.detail_page)
        for each in response.doc('div.article > div.paginator > span.next > a').items():
            self.crawl(each.attr.href,callback=self.list_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "title":response.doc('#content > h1 > span:nth-child(1)').text(),
            "rate":response.doc('.rating_num').text(),
            "audience":response.doc('.rating_sum span').text(),
            "year":response.doc('.year').text(),
            "director": [x.text() for x in response.doc('a[rel="v:directedBy"]').items()],
            "genre": [x.text() for x in response.doc('span[property="v:genre"]').items()],
            "starring": [x.text() for x in response.doc('a[rel="v:starring"]').items()]
        }