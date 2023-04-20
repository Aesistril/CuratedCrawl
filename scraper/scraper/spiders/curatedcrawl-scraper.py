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
import mariadb
from configparser import ConfigParser

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
src_sites = []
src_domains = []
for tag in ["RETRO", "UNIQ"]:
    cursor.execute('SELECT domain FROM domains WHERE type = %s AND crawled = 0', (tag,))
    rows = cursor.fetchall()
    for row in rows:
        src_domains.append(row[0])
        src_sites.append("https://" + row[0])

# Pull banned domains
blacklist = []
cursor.execute('SELECT entry FROM blacklist WHERE type = "DOMAIN"')
rows = cursor.fetchall()
for domain in rows:
    blacklist.append(domain[0])

# Pull and convert banned subdomains list to a list of regex statements
bannedsubdomain_regex = []
cursor.execute('SELECT entry FROM blacklist WHERE type = "SUBDOMAIN"')
rows = cursor.fetchall()
for sub in rows:
    bannedsubdomain_regex.append(rf'^https?:\/\/{sub[0]}\.')

class CuratedCrawlCrawler(CrawlSpider):
    name = 'curatedcrawl-crawler'
    start_urls = src_sites

    rules = (
        Rule(LinkExtractor(deny_domains=blacklist, deny=bannedsubdomain_regex), callback='output_item', follow=True),
    )

    def output_item(self, response):
        tldx = tldextract.extract(response.url)
        if tldx.subdomain == "":
            domain = tldx.domain + '.' + tldx.suffix
        else:
            domain = tldx.subdomain + "." + tldx.domain + '.' + tldx.suffix

        if domain not in linkcount:
            linkcount[domain] = 0

        if response.meta.get('depth', 0) <= int(config["scraper_discovery"]["depth"]) and linkcount[domain] <= int(config["scraper_discovery"]["links_per_site"]):
            linkcount[domain] += 1
            yield {'url': response.url, 'domain': domain, 'depth': response.meta.get('depth', 0)}
    
    def closed(self, reason):
        if reason == 'finished':
            for domain in src_domains:
                cursor.execute("UPDATE domains SET crawled = 1 WHERE domain = %s", (domain,))
            cursor.close()
            dbconn.close()
            print('Spider completed normally.')
        else:
            print('Spider was terminated. Crawled sites will not be marked as "crawled"')
