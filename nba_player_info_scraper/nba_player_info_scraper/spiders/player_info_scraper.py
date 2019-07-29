# -*- coding: utf-8 -*-
import scrapy


class PlayerInfoScraperSpider(scrapy.Spider):
    name = 'player_info_scraper'
    start_urls = ['http://espn.com/nba/players']

    def parse(self, response):
        url = "http://www.espn.com/nba/players"

        all_teams_hrefs = response.css('.small-logos div a::attr(href)').getall()

        for href in all_teams_hrefs:
            yield response.follow(href, callback=self.roster_crawler)

    def roster_crawler(self, response):
        players = len(response.css('.Table2__td+ .Table2__td a'))

        def player_sels(i):
            name_sel = f".Table2__even:nth-child({i}) .Table2__td+ .Table2__td a::text"
            pos_sel = f".Table2__even:nth-child({i}) .Table2__td:nth-child(3) span::text"
            age_sel = f".Table2__even:nth-child({i}) .Table2__td:nth-child(4) span::text"
            ht_sel = f".Table2__even:nth-child({i}) .Table2__td:nth-child(5) span::text"
            wt_sel = f".Table2__even:nth-child({i}) .Table2__td:nth-child(6) span::text"
            college_sel = f".Table2__even:nth-child({i}) .Table2__td:nth-child(7) span::text"
            salary_sel = f".Table2__even:nth-child({i}) .Table2__td:nth-child(8) span::text"

            return [name_sel, pos_sel, age_sel, ht_sel, wt_sel, college_sel, salary_sel]

        for i in range(1, players+1):
            this_player_sels = player_sels(i)

            def responder(a_sel):
                return response.css(a_sel).get()

            yield {
                'name': responder(this_player_sels[0]),
                'pos': responder(this_player_sels[1]),
                'age': responder(this_player_sels[2]),
                'height': responder(this_player_sels[3]),
                'weight': responder(this_player_sels[4]),
                'college': responder(this_player_sels[5]),
                'salary': responder(this_player_sels[6])
            }
