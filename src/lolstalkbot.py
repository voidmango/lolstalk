# lolstalkbot.py
# import pkgs
import os
import discord
import asyncio
import lolstalk as ls
from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="&", intents=intents)


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.command()
async def lastgame(ctx, *, arg):
    lg = ls.get_last_info(arg)
    embed = discord.Embed(title='Last Game', description=f"```\n{lg}\n```")
    await ctx.send(embed=embed)

#@bot.command()
#async def lolstalk(ctx, *, arg):


#@bot.task

def main():
    bot.run(TOKEN)

main()