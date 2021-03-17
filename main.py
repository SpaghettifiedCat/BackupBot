# BackupBot.py
import textwrap
import os
from dotenv import load_dotenv
import traceback
import discord
import wptools
from mediawiki import MediaWiki
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='^')
wikipage = MediaWiki()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def wiki(ctx, *args):
    try:
        page = ""
        for i in args:
            page = page + i + ' '
        page = page.strip()
        print(page)
        summary = wikipage.summary(page, auto_suggest=False)
        summary_list = textwrap.wrap(summary, 2000, break_long_words=False)
        for i in summary_list:
            embedvar = discord.Embed(description=i, color=0x00ff00)
            await ctx.channel.send(embed=embedvar)
        try:
            embedvar = discord.Embed(color=0x00ff00)
            image = wptools.page(page).get_query()
            embedvar.set_image(url=image.image('page')['url'])
            await ctx.channel.send(embed=embedvar)
        except (ValueError, Exception):
            print(traceback.format_exc())
            try:
                embedvar = discord.Embed(color=0x00ff00)
                image = wptools.page(page).get_query()
                embedvar.set_image(url=image.image('thumb')['url'])
                await ctx.channel.send(embed=embedvar)
            except (ValueError, Exception):
                print(traceback.format_exc())
                pass

    except Exception as inst:
        page = ""
        for i in args:
            page = page + i + ' '
        page = page.strip()
        await ctx.channel.send("Error raised")
        await ctx.channel.send(f'You asked me to search for {page}')
        await ctx.channel.send(inst)


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong!")


@bot.command()
async def xkcd(ctx, *args):
    try:
        url = r'https://xkcd.com/'
        if args == ():
            rndm = str(random.randint(1, 2473))
            url = url + rndm
            await ctx.channel.send(url)
        else:
            await ctx.channel.send(url + args[0])
    except Exception as e:
        await ctx.channel.send(e)

bot.run(TOKEN)
