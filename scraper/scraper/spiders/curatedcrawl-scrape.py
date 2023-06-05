#!/usr/bin/env python3

# Copyright (C) 2023
# Yiğit Ayaz <yigitayaz262@gmail.com>
# This file is part of the CuratedCrawl Search Engine.

# The CuratedCrawl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# The CuratedCrawl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the CuratedCrawl Search Engine.  If not, see <http://www.gnu.org/licenses/>.

import tldextract
from scrapy.spiders import CrawlSpider, Rule
import mariadb
from configparser import ConfigParser
import re
from bs4 import BeautifulSoup

# Read globsettings.cfg
config = ConfigParser()
config.read("../globsettings.cfg")

linkcount = {}

# Connect to MariaDB using settings from globsettings.cfg
try:
    dbconn = mariadb.connect(password=config["MariaDB"]["passwd"], user=config["MariaDB"]["user"], host=config["MariaDB"]["host"], port=int(config["MariaDB"]["port"]), database=config["MariaDB"]["database"])
    dbconn.autocommit = True
except Exception as err:
    print(f"Database connection error:\n\n\n{err}")
    exit(1)

cursor = dbconn.cursor()

# Pull domains that hasn't been crawled before and was tagged as RETRO or UNIQ by the moderators and use them to find new websites 
crawlsiteshttp = []
crawldomains = []
site_type = {}
cursor.execute('SELECT domain, type FROM domains WHERE type != "UNMOD"')
rows = cursor.fetchall()
for row in rows:
    crawldomains.append(row[0])
    crawlsiteshttp.append("http://" + row[0])
    site_type[row[0]] = row[1]
    
print(crawlsiteshttp)

def tldx_url(url):
    tldx = tldextract.extract(url)

    if tldx.subdomain == "":
        fdqn = tldx.domain + '.' + tldx.suffix
    else:
        fdqn = tldx.subdomain + "." + tldx.domain + '.' + tldx.suffix
    
    fdqn_nosub = tldx.domain + '.' + tldx.suffix
    return fdqn, tldx.subdomain, fdqn_nosub

class CuratedCrawlScrape(CrawlSpider):
    name = 'curatedcrawl-scrape'
    start_urls = crawlsiteshttp
    allowed_domains = crawldomains
    DEPTH_LIMIT = 100

    custom_settings = {
        'ITEM_PIPELINES': {
            "scraper.pipelines.MariaDB_ScraperPipeline": 400,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
        }
    }

    rules = (
        Rule(callback='output_item', follow=True),
    )

    def output_item(self, response):
        fdqn, _, _ = tldx_url(response.url)
        site_content = ' '.join(BeautifulSoup(response.body, "html.parser").stripped_strings)
        # print({'url': response.url, 'title': response.css('title::text').get(), 'type': site_type[fdqn], 'content': site_content})
        yield {'url': response.url, 'title': response.css('title::text').get(), 'type': site_type[fdqn], 'content': site_content}
