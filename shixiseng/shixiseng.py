
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-05-26 11:03:11
# Project: shixiseng

from pyspider.libs.base_handler import *




class Handler(BaseHandler):
    crawl_config = {
    }
    @every(minutes=24 * 60)
    def on_start(self):
        for i in range(32):
            url = 'http://www.shixiseng.com/interns?k=%E4%BA%A7%E5%93%81&p=' + str(i)
            self.crawl(url,callback=self.list_page)

    @config(age=10*24*60*60)
    def list_page(self,response):
        for each in response.doc('body > div.wrap > div.container > div.content > div.position > div.posi-list > div > div.po-name > div.names > a').items():
            self.crawl(each.attr.href,callback=self.detail_page)
           
    @config(priority=2)
    def detail_page(self, response):
        return {
            "period":response.doc('span[class="month"]').text(),
            "job name":response.doc('span[class="job_name"]').text(),
            "frequency":response.doc('span[class="days"]').text(),
            "company":response.doc('div.jb_det_right_top > p > a').text()
            
        }