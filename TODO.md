# Project Status
Roots aren't deep but seeds are planted. There is still a long way to go until the first beta release let alone stable.

This isn't the start of this project. There was a long gone scraper I wrote with BeautilfulSoup which just sucked. Luckily I burried it 3 kilometers deep, next to Margaret Thatcher.

Though to be optimistic, most ideas have formed so there will be way less rebasing and rewriting from now on.

# Not Done Yet
#### Data management
#### Moderator Tools
- Multithreading
- Add link previews to modtool
- Only add domain to the blacklist (not the whole sub+domain+tld combo)
#### Crawler
- Ignore www.
- Implement not searching already crawled sites
- Add text scraping
- Seperate site discovery and text scraping with cli args
#### Documentation
- Create README.md
- Document build process for prebuilt files like modtoolui.py
- Document database rows
#### Security
- Prevent DoS attacks that uses form spamming
- Database input sanitization
#### Web
- Create the goddamn app first
- Server load/status
#### UX
- Create a report system
- Discord style acknowledgements (thank you for making the world a better place)
- Option to exclude neocities sites
#### General Ideas
- Create a gopher service
- Donation button (someone's gotta pay the server bills)


# Done
#### Data management
- Tie everything together with MySQL, get rid of .csv madness
- MySQL schema
- Write a script to merge newly found domains with old ones
- Implement .csv output
- Download top 1M manually to avoid ToS issues
#### Moderator Tools
- Add "open in browser" option
- Add keybinds to arrow keys
- Prevent pages from rendering twice
- Fix browser link opening bug
- Selenium error handling
- Fix the empty link bug
- Adopt to MySQL
#### Crawler
- Optimize and reduce database accesses
- Rename to curatedcrawl-crawler. Scraper is something else
- Adopt to MySQL
- Implement depth and links per site variables for faster domain discovery
- Put `depth` and `linkspersite` into a config file where it's changed less (caused by: Implement not searching already crawled sites)
- Implement subdomain blocking
#### Documentation
- Document autocreated .csv files
- Add comments to modtool.py
#### Security
#### Web
#### UX
#### General Ideas
- Split retro and unique sites
