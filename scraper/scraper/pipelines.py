# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


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

class ScraperPipeline:
    def process_item(self, item, spider):
        return item
