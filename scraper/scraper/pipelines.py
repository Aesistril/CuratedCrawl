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



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
# useful for handling different item types with a single interface
from scrapy.exceptions import CloseSpider
from configparser import ConfigParser
import mariadb

class MariaDB_DiscoveryPipeline:
    def open_spider(self, _):
        # Read globsettings.cfg
        config = ConfigParser()
        config.read("../globsettings.cfg")

        # Connect to MariaDB using settings from globsettings.cfg
        try:
            self.dbconn = mariadb.connect(password=config["MariaDB"]["passwd"], user=config["MariaDB"]["user"], host=config["MariaDB"]["host"], port=int(config["MariaDB"]["port"]), database=config["MariaDB"]["database"])
            self.dbconn.autocommit = True
        except Exception as err:
            raise CloseSpider("Exception in pipeline: %s" % err)

        self.cursor = self.dbconn.cursor()

    def close_spider(self, _):
        pass # This is handled in curatedcrawl-crawler.py
        
    def process_item(self, item, _):
        self.cursor.execute("SELECT * FROM domains WHERE domain = %s", (item['domain'],))
        if self.cursor.fetchall() == []:
            self.cursor.execute('INSERT INTO domains (domain, type, crawled, scraped) VALUES (%s, "UNMOD", 0, 0)', (item['domain'],))
        return item

class MariaDB_ScraperPipeline:
    def open_spider(self, _):
        # Read globsettings.cfg
        config = ConfigParser()
        config.read("../globsettings.cfg")

        # Connect to MariaDB using settings from globsettings.cfg
        try:
            self.dbconn = mariadb.connect(password=config["MariaDB"]["passwd"], user=config["MariaDB"]["user"], host=config["MariaDB"]["host"], port=int(config["MariaDB"]["port"]), database=config["MariaDB"]["database"])
            self.dbconn.autocommit = True
        except Exception as err:
            raise CloseSpider("Exception in pipeline: %s" % err)

        self.cursor = self.dbconn.cursor()

    def close_spider(self, _):
        pass # This is handled in curatedcrawl-crawler.py
        
    def process_item(self, item, _):
        self.cursor.execute("SELECT * FROM scraped_content WHERE url = %s", (item['url'],))
        if self.cursor.fetchall() == []:
            self.cursor.execute('INSERT INTO scraped_content (url, text, title, type) VALUES (%s, %s, %s, %s)', (item['url'], item['content'], item['title'], item['type']))
        return item

class ScraperPipeline:
    def process_item(self, item, spider):
        return item
