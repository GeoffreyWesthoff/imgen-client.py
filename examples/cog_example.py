"""
DANK MEMER IMGEN API CLIENT
---------------------------
Copyright: Copyright 2019 Melms Media LLC
License: MIT

"""

from discord.ext import commands
from discord import Member
from imgen import AsyncClient
from traceback import print_exc

imgen = AsyncClient(token="imgentokengoeshere")
ratelimit = imgen.tweet.ratelimit


class Tweet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=ratelimit[0], per=ratelimit[1], commands.BucketType.default)
    async def tweet(self, ctx, member: Member = None, *, text: str):
        if not member:
            member = ctx.author
        result = await imgen.tweet.get_as_discord(username1=member, avatar1=member.avatar_url, text=text)
        await ctx.send(file=result)

    @tweet.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('Please tweet some text bro')
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send('Bro we can\'t meme so fast, slow down fool. '
                                  'You gotta wait %s seconds!' % error.retry_after)
        else:
            await ctx.send('Bro something done fucked up.')
            return print_exc


def setup(bot):
    bot.add_cog(Tweet(bot))


def teardown(bot):
    imgen.session.close()
    del imgen
    return
