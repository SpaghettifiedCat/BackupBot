# BackupBot.py
import os
import wikipedia
import textwrap
import json
import requests
import discord

TOKEN = DISCORD_TOKEN
client = discord.Client()
sink = SINK_SERVER
backup_channel = BACKUP_CHANNEL_ID
source = SOURCE_SERVER

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(page):
    try:
        result = wikipedia.search(page, results=1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title=result[0])
        title = wkpage.title
        response = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
    except:
        return "No Image Found"



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if (not message.author == client.user) and not str(message.guild) == sink:
        backup_channel = client.get_channel(backup_channel)
        await backup_channel.send(f'```{message.author} said: \n"{message.content}" \nin {message.channel}```')
    if not message.author == client.user:
        if message.content.startswith('^wiki'):
            try:
                query = str(message.content)[5: len(message.content)]
                query = query.strip()
                print(query)
                summary = str(wikipedia.summary(query))
                summary_list = textwrap.wrap(summary, 2000, break_long_words=False)
                for i in summary_list:
                    embedVar = discord.Embed(description=i, color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                embedVar = discord.Embed(color=0x00ff00)
                embedVar.set_image(url=get_wiki_image(query))
                await message.channel.send(embed=embedVar)
                await message.channel.send(get_wiki_image(query))
            except Exception as inst:
                await message.channel.send("Error raised")
                await message.channel.send(f'You asked me to search for {query}')
                await message.channel.send(inst)
client.run(TOKEN)
