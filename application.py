import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import os
from dotenv import load_dotenv
from aramdetails import AramDetails

load_dotenv()

DESCRIPTION = """A simple bot to send messages about aram(league of legends)"""

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
    set_data(data, aram_details.get_top_champions(total=int(os.getenv("DAILY_TOTAL_RESULTS"))))
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
        "title": f"best {os.getenv('DAILY_TOTAL_RESULTS')} champions of patch 13.18",
        "description": f"daily stats of best {os.getenv('DAILY_TOTAL_RESULTS')} ARAM champions",
        "color": 0xFEE75C,
        "author": {
            "name": "ARAMID",
            "icon_url": "https://github.com/Douglas-Machado.png",
        },
        "fields": titles,
    }

    return embed.from_dict(embed_dict)


@tasks.loop(time=time(11,0,0))
# @tasks.loop(seconds=20)
async def send_daily_message():
    formatted_data = format_data()
    response = make_embed(formatted_data)
    # channel = aram_client.get_channel(1153332095792463922)
    # await channel.send(embed=response)
    # test channel
    for id in channel_ids:
        channel = aram_client.get_channel(id)
        await channel.send(embed=response)

@aram_client.event
async def on_message(message):
    if message.author.bot:
        return

    else:
        await aram_client.process_commands(message)

if __name__ == "__main__":
    aram_client.run(os.getenv("TOKEN"))
