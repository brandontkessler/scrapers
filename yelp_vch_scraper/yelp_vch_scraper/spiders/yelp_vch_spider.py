# -*- coding: utf-8 -*-
import scrapy


class YelpVchSpiderSpider(scrapy.Spider):
    name = 'yelp_vch_spider'
    start_urls = ['https://www.yelp.com/biz/valley-community-healthcare-north-hollywood']

    def parse(self, response):
        url = 'https://www.yelp.com/biz/valley-community-healthcare-north-hollywood?start=0'
        all_reviews = response.css('.review-content p').getall()

        for review in all_reviews:
            yield {
                'rev': all_reviews
            }

        next_btn = response.css('.next::attr(href)').get()
        if next_btn is not None:
            next_btn = response.urljoin(next_btn)
            yield scrapy.Request(next_btn, callback=self.parse)
