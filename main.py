import discord
from discord.ext import commands
from web import AramDetails
from os import getenv

from dotenv import load_dotenv

load_dotenv()

description = '''A simple bot to send messages about aram(league of legends)'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
DAILY_TOTAL_RESULTS = int(getenv("DAILY_TOTAL_RESULTS"))

bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description=description, intents=intents)

@bot.event
async def on_ready():
    '''TODO add updated hours'''
    print(f'We have logged in as {bot.user}')
    try:
        aram_details = AramDetails()
        response: list[dict] = aram_details.get_top_ten_champions(total=DAILY_TOTAL_RESULTS)
        titles = [{"name": key} for key in aram_details.keys]
        for title in titles:
            title["value"] = ""
            title["inline"] = True
        count = 3
        for data in response:

            titles.insert(count, {
                "name": "",
                "value": data.get("name"),
                "inline": True
            })
            titles.insert(count+1, {
                "name": "",
                "value": data.get("winrate"),
                "inline": True
            })
            titles.insert(count+2, {
                "name": "",
                "value": data.get("matches"),
                "inline": True
            })
            count += 4

        embed = discord.Embed(
            color=discord.Colour.green(),
        )
        embed_dict = {
            "title": f"best {DAILY_TOTAL_RESULTS} champions of patch 13.18",
            "description": f"daily stats of best {DAILY_TOTAL_RESULTS} ARAM champions",
            "color": 0xFEE75C,
            "author": {
                "name": "ARAMID",
                "icon_url": "https://github.com/Douglas-Machado.png"
            },
            "fields": titles
        }

        channel = bot.get_channel(1153332095792463922)
        await channel.send(embed=embed.from_dict(embed_dict))
    except Exception as ex:
        print('error')
        print(ex)

bot.run(getenv("TOKEN"))

text_channels_list = []
for guild in bot.guilds:
    for channel in guild.text_channels:
        text_channels_list.append(channel)

