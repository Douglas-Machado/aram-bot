import discord
from discord.ext import commands, tasks
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, time
import os

DESCRIPTION = """A simple bot to send messages about aram(league of legends)"""

DAILY_TOTAL_RESULTS = int(os.environ["DAILY_TOTAL_RESULTS"])


class AramDetails:
    def __init__(self):
        self.keys = ["name", "winrate", "matches"]

    def get_top_champions(self, total: int):
        driver = webdriver.Chrome()
        driver.get(os.environ["ARAM_WEB_URL"])
        rows = driver.find_elements(By.CLASS_NAME, "rt-tr")
        rows.pop(0)
        rows = rows[:total]
        items = []
        for row in rows:
            values = row.text.split("\n")
            values.pop(4)
            values.pop(2)
            values.pop(0)
            items.append(values)

        driver.close()
        response_dict: [dict] = [{k: v for (k, v) in zip(self.keys, infos)} for infos in items]
        return response_dict

intents = discord.Intents.default()
intents.message_content = True

aram_client = commands.Bot(command_prefix="a!", intents=intents)
channel_ids: list[int] = []
aram_details = AramDetails()
data = []


@aram_client.event
async def on_ready():
    print(f"We have logged in as {aram_client.user} at {datetime.now().time()}")
    get_default_channel_ids()
    set_data(data, aram_details.get_top_champions(total=int(os.environ["DAILY_TOTAL_RESULTS"])))
    update_data.start(data)
    send_daily_message.start()


def get_default_channel_ids():
    for guild in aram_client.guilds:
        channel_ids.append(guild.text_channels[0].id)

def set_data(target: list, value: list):
    target.clear()
    target.append(value)



def format_data():
    titles = [{"name": key} for key in aram_details.keys]
    for title in titles:
        title["value"] = ""
        title["inline"] = True
    count = 3
    for d in data[0]:
        titles.insert(count, {"name": "", "value": d.get("name"), "inline": True})
        titles.insert(
            count + 1, {"name": "", "value": d.get("winrate"), "inline": True}
        )
        titles.insert(
            count + 2, {"name": "", "value": d.get("matches"), "inline": True}
        )
        count += 4
    return titles


def make_embed(titles: list[dict]):
    embed = discord.Embed(
        color=discord.Colour.green(),
    )
    embed_dict = {
        "title": f"best {DAILY_TOTAL_RESULTS} champions of patch 13.18",
        "description": f"daily stats of best {DAILY_TOTAL_RESULTS} ARAM champions",
        "color": 0xFEE75C,
        "author": {
            "name": "ARAMID",
            "icon_url": "https://github.com/Douglas-Machado.png",
        },
        "fields": titles,
    }

    return embed.from_dict(embed_dict)


@tasks.loop(hours=10)
async def update_data(data):
    if data:
        return
    data = await aram_details.get_top_champions(total=int(os.environ["DAILY_TOTAL_RESULTS"]))


@tasks.loop(time=time(11, 0, 0))
async def send_daily_message():
    formatted_data = format_data()
    response = make_embed(formatted_data)
    for id in channel_ids:
        channel = aram_client.get_channel(id)
        await channel.send(response)

@aram_client.event
async def on_message(message):
    if message.author.bot:
        return

    else:
        await aram_client.process_commands(message)


aram_client.run(os.environ["TOKEN"])
