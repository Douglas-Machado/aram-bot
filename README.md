# ARAMID

## this is a simple project build to send daily messages in discord channels about best champion in ARAM ([lol](https://www.leagueoflegends.com/pt-br/news/tags/aram/))

<img src="./.github/aram-bg.jpg">

### This app runs on [discloud](https://discloudbot.com) but you can run locally with the steps below

## GOAL

This project was made with discord.py library and selenium to simply open a url, get data from the page, and then send it to discord channels in any server 

### Set environment Variables (.env)

the environment variables are:
* TOKEN ( discord bot token )
* ARAM_WEB_URL ( url to get data with selenium)
* DAILY_TOTAL_RESULTS ( daily total results)

### Run

I recommend you to use a virtual environment like conda or virtualenv

```bash
pip install -r requirements.txt
```

then 

```bash
python application.py
```

made with 💖 by Douglas
