import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import os
from dotenv import load_dotenv
from aram_data import AramData
from pagination_view import PaginationView

load_dotenv(override=True)

DESCRIPTION = """A simple bot to send messages about aram(league of legends)"""

intents = discord.Intents.default()
intents.message_content = True

aram_client = commands.Bot(command_prefix="a!", intents=intents)
channel_ids: list[int] = []

aram_data = AramData()
commands_list = ["top <number>", "champion <name>"]


@aram_client.event
async def on_ready():
    print(f"We have logged in as {aram_client.user} at {datetime.now().time()}")
    get_default_channel_ids()
    aram_data.fetch_mongo_data()
    send_message.start()


def get_default_channel_ids():
    for guild in aram_client.guilds:
        channel_ids.append(guild.text_channels[0].id)


@tasks.loop(hours=3)
async def update_data():
    aram_data.fetch_mongo_data()


# TODO compare champions


# @tasks.loop(seconds=20)
@tasks.loop(time=time(12, 0, 0))
async def send_message():
    data = aram_data.get_top_champions(int(os.getenv("DAILY_TOTAL_RESULTS")))
    pagination_view = PaginationView()
    pagination_view.data = data
    embed = pagination_view.create_embed(data)
    try:
        guilds = []
        for id in channel_ids:
            channel = aram_client.get_channel(id)
            guilds.append(channel.guild.name)
            await channel.send(embed=embed)
            print(f"message sent to {channel.name}")
    except Exception as ex:
        print(ex)


@aram_client.command()
async def top(ctx, msg):
    try:
        number = int(msg)
    except ValueError:
        await ctx.send("Must be a number")
        return

    data = aram_data.get_top_champions(number)
    pagination_view = PaginationView()
    pagination_view.data = data
    await pagination_view.send(ctx)


@aram_client.command(name="champion")
async def get_champion(ctx, *, message: str):
    if not message.lower() in aram_data.champions_list:
        await ctx.send("Champion not found")
        return

    champion_data = {}
    for champion in aram_data.data:
        if champion.get("name").lower() == message.lower():
            champion_data = champion
            break

    title = f"{champion_data.get('name')} - TOP {champion_data.get('rank')}"
    description = f"{champion_data.get('name')} global stats"
    message = f"""
**{title}**
*{description}*
**-----------------**
Rank - {champion_data.get("rank")}
Tier - {champion_data.get("tier")}
Win Rate - {champion_data.get("winrate")}
Pick Rate - {champion_data.get("pickrate")}
Matches - {champion_data.get("matches")}
    """
    await ctx.send(message)


@aram_client.command()
async def commands(ctx):
    for command in commands_list:
        await ctx.send(f" a! + {command}")


@aram_client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("a!champions"):
        await message.channel.send("coming soon")
    else:
        await aram_client.process_commands(message)


if __name__ == "__main__":
    aram_client.run(os.getenv("TOKEN"))
