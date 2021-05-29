import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Help"])
    async def help(self, ctx):
        embed = discord.Embed(colour=discord.Colour.gold())
        embed.title = 'Help'
        embed.add_field(name='c!Element [symbol]',
                        value='Lists the element\'s information.\n',
                        inline=False)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name='c!Molarmass [formula]',
                        value='Displays the molar mass of the compound and its percent by mass.\n',
                        inline=False)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name='c!Mass [formula] [values][units]',
                        value='Calculates the missing information according to the units given.\n'+
                        'For example: `c!Mass H2O 2g` would return its mass and moles.\n\n' +
                        'Valid units: g, mg, L, mL, mol, mmol\n',
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def latency(self, ctx):
        await ctx.send(f"Time taken: {round(self.client.latency * 1000)} ms")


def setup(client):
    client.add_cog(Commands(client))
