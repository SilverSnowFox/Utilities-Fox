import chemlib
import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Element'])
    async def element(self, ctx, arg=None):
        if arg is None:
            await ctx.send("Please select an element by its symbol")

        information = chemlib.Element(arg)
        element = information['Element']

        embed = discord.Embed(title=element, color=discord.Colour.gold())
        embed.set_thumbnail(url=f'https://images-of-elements.com/t/{element.lower()}.png')
        embed.add_field(name='Symbol', value=information['Symbol'])
        embed.add_field(name='Atomic Number', value=str(int(information['AtomicNumber'])))
        embed.add_field(name='Atomic Mass', value=information['AtomicMass'])
        embed.add_field(name='Type', value=information['Type'])
        phase = information['Phase']
        fixed_phase = phase[0].upper() + phase[1:]
        embed.add_field(name='Phase', value=fixed_phase)
        embed.add_field(name='Electronegativity', value=information['Electronegativity'])
        embed.add_field(name='Electron Config', value=information['Config'])
        embed.add_field(name='Melting Point', value=information['MeltingPoint']+' K')
        embed.add_field(name='Boiling Point', value=information['BoilingPoint'] + ' K')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
