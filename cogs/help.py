import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Help"])
    async def help(self, ctx):
        embed = discord.Embed(colour=discord.Colour.gold())
        embed.title = 'Help'
        embed.add_field(name='c!Element [symbol]', value='Lists the element\'s information.')
        await ctx.send(embed=embed)

    @commands.command()
    async def latency(self, ctx):
        await ctx.send(f"Time taken: {round(self.client.latency * 1000)} ms")


def setup(client):
    client.add_cog(Commands(client))
