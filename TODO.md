# Project Status
Roots aren't deep but seeds are planted. There is still a long way to go until the first beta release let alone stable.

This isn't the start of this project. There was a long gone scraper I wrote with BeautilfulSoup which just sucked. Luckily I burried it 3 kilometers down, next to Margaret Thatcher.

Though to be optimistic, most ideas have formed so there will be way less rebasing and rewriting from now on.

# Not Done Yet
#### Data management
- Tie everything together with MySQL, get rid of .csv madness
- Adopt `domainadd.sh` and `download_blacklist.sh` to MySQL
- Implement whitelist, which will allow domains even if they are in top 1M list. Possible addition to `download_blacklist.sh`
- Rename `download_blacklist.sh` to `update_blacklist.sh` in case of changes in functionality
- MySQL database creation script
#### Moderator Tools
- Add link previews to modtool
- Fix the empty link bug
- Adopt to MySQL
#### Scraper
- Implement not searching already crawled sites
- Add text scraping
- Adopt to MySQL
- Put `depth` and `linkspersite` into a config file where it's changed less (caused by: Implement not searching already crawled sites)
- Seperate site discovery and text scraping with cli args
#### Documentation
- Create README.md
- Document build process for prebuilt files like modtoolui.py
#### Security
- Prevent DoS attacks that uses form spamming
#### Web
- Create the goddamn app first
#### UX
- Create a report system
- Option to exclude neocities sites
#### General Ideas
- Create a gopher service
- Donation button (someone's gotta pay the server bills)


# Done
#### Data management
- Write a script to merge newly found domains with old ones
- Implement .csv output
- Download top 1M manually to avoid ToS issues
#### Moderator Tools
- Add "open in browser" option
- Add keybinds to arrow keys
- Prevent pages from rendering twice
- Fix browser link opening bug
- Selenium error handling
#### Scraper
- Implement depth and links per site variables for faster domain discovery
- Implement subdomain blocking
#### Documentation
- Document autocreated .csv files
- Add comments to modtool.py
#### Security
#### Web
#### UX
#### General Ideas
- Split retro and unique sites
