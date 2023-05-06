#!/usr/bin/env python3

# CuratedCrawl - A search engine with hand picked results
# Copyright (C) 2023 Yiğit Ayaz

# CuratedCrawl is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# CuratedCrawl is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with CuratedCrawl. If not, see <http://www.gnu.org/licenses/>.

import tldextract
from scrapy.spiders import CrawlSpider, Rule
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
for tag in config["scraper_discovery"]["tags"].split(","):
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
bannedsubdomain = []
cursor.execute('SELECT entry FROM blacklist WHERE type = "SUBDOMAIN"')
rows = cursor.fetchall()
for sub in rows:
    bannedsubdomain.append(sub[0])

blacklist = set(blacklist)
bannedsubdomain = set(bannedsubdomain)

def tldx_url(url):
    tldx = tldextract.extract(url)

    if tldx.subdomain == "" or tldx.subdomain == "www":
        fdqn = tldx.domain + '.' + tldx.suffix
    else:
        fdqn = tldx.subdomain + "." + tldx.domain + '.' + tldx.suffix
    
    fdqn_nosub = tldx.domain + '.' + tldx.suffix
    return fdqn, tldx.subdomain, fdqn_nosub

def check_blacklist(links):
    filtered_links = []

    for link in links:
        fdqn, tldx_subdomain, fdqn_nosub = tldx_url(link.url)
        if fdqn_nosub not in blacklist and fdqn not in blacklist and tldx_subdomain not in bannedsubdomain:
            if fdqn not in linkcount:
                linkcount[fdqn] = 0

            if linkcount[fdqn] <= int(config["scraper_discovery"]["links_per_site"]):
                linkcount[fdqn] += 1
                filtered_links.append(link)

    return filtered_links
    
class CuratedCrawlDiscovery(CrawlSpider):
    name = 'curatedcrawl-discover'
    start_urls = src_sites

    rules = (
        Rule(callback='output_item', follow=True, process_links=check_blacklist),
    )

    def output_item(self, response):
        fdqn, _, _ = tldx_url(response.url)
        yield {'url': response.url, 'domain': fdqn, 'depth': response.meta.get('depth', 0)}
    
    def spider_closed(self, _):
        for domain in src_domains:
            cursor.execute("UPDATE domains SET crawled = 1 WHERE domain = %s", (domain,))
        cursor.close()
        dbconn.close()
        print('Spider completed normally.')
