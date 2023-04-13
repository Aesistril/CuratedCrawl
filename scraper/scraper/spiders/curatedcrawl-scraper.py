#!/usr/bin/env python3

# The GPLv3 License (GPLv3)
# 
# Copyright (c) 2023 Yiğit Ayaz 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import tldextract
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

src_sites = [line for line in open("crawl_src.csv").read().split("\n") if line != ""]
blacklist = [line for line in open("blacklist.csv").read().split("\n") if line != ""]
blacklist_mod = [line for line in open("blacklist_mod.csv").read().split("\n") if line != ""]
crawled = [line for line in open("crawled.csv").read().split("\n") if line != ""]
bannedsubdomain = [line for line in open("bannedsubdomain.csv").read().split("\n") if line != ""]
print(bannedsubdomain)
bannedsubdomain_regex = []
linkcount = {}

for sub in bannedsubdomain:
    bannedsubdomain_regex.append(rf'^https?:\/\/{sub}\.')

class CuratedCrawlSpider(CrawlSpider):
    name = 'curatedcrawl-spider'
    start_urls = src_sites
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'found_urls.csv'
    }

    rules = (
            Rule(LinkExtractor(deny_domains=blacklist + crawled + blacklist_mod, deny=bannedsubdomain_regex), callback='output_item', follow=True),
        # Rule(LinkExtractor(deny_domains=blacklist)),
    )

    def output_item(self, response):
        yield {'url': response.url}

# while True:
#     for url in discovered_urls:
#         if url not in crawled_urls:
#             print("Crawling: " + url)
#             crawl(url)
#     if set(discovered_urls) == set(crawled_urls):
#         print("All links searched!")
#         break

