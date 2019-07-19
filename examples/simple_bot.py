"""
DANK MEMER IMGEN API CLIENT
---------------------------
Copyright: Copyright 2019 Melms Media LLC
License: MIT

"""

from discord import Client
from imgen import AsyncClient


bot = Client()
memegen = AsyncClient(token='tokengoeshere')


@bot.event
async def on_ready():
    print('Logged in as %s' % bot.user)


@bot.event
async def on_message(msg):
    if msg.content.lower().startswith('!magik'):
        magik = await memegen.magik.get_as_discord(avatar1=msg.author.avatar_url)
        return await msg.channel.send(file=magik)
    elif msg.content.lower().startswith('!crab'):
        parsed = msg.content.replace('!crab ', '')
        parsed = parsed.replace(', ', ',')
        if len(parsed.split(',')) != 2:
            return await msg.channel.send('Please split the text with a comma, e.g. !crab upper, bottom')
        crab = await memegen.crab.get_as_discord(text=parsed)
        return await msg.channel.send(file=crab)

bot.run('bottokengoeshere')
