# What are these files?
These files are configuration files and URL lists for the spider

bannedsubdomain.csv: Blacklisted subdomains.
blacklist.csv: Top 1 million visited domains. Sourced from Cloudflare Radar with some manual edits.
blacklist_mod.csv: Blacklist entries added by the moderators.
crawl_src: start_urls for Scrapy.
crawled.csv: Manually edited. Same functionality as blacklist.csv but for domains that are already crawled.
domainadd.sh: Extracts domains from URLs and adds them on top of found_domains.csv
found_domains.csv: Found domains that will be inputted to CuratedCrawl Modtool
found_urls.csv: Scrapy output. Processed by domainadd.sh. Deleted regularly.
scrapy.cfg: Scrapy config file
download_blacklist.sh: Downloads the Cloudflare Radar Top 1000000 domains list using wget. I'm doing this instead of shipping it with this project because I'm not sure if it's permitted to do so.
