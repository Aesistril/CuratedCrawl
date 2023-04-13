#!/bin/bash

cut -d',' -f1 found_urls.csv > found_domains.csv
sed -i 's/^[^/]*\/\/\([^@]*@\)\?\([^:/]*\).*/\2/' found_domains.add.csv
sort found_domains.add.csv | uniq > curatedcrawldomainsorter.tmp && mv curatedcrawldomainsorter.tmp found_domains.add.csv
cat found_domains.add.csv >> found_domains.csv
sort found_domains.csv | uniq > curatedcrawldomainsorter.tmp && mv curatedcrawldomainsorter.tmp found_domains.csv
