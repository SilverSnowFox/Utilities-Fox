import discord
from discord.ext import commands
import pubchempy as pcp


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Search"])
    # Searches for a compound by name, returning the CID and some general info about the compound
    async def search(self, ctx, *, arg=None):
        # Checks if used added an argument
        if arg is None:
            await ctx.send("Please input the command with a valid compound name. Ex: `c!Search Water`")
            return

        # Gets the results of the search
        results = pcp.get_compounds(arg, 'name')

        if len(results) == 0:
            await ctx.send("Unable to find any results.")
            return

        embed = discord.Embed(colour=discord.Colour.gold())
        embed.title = 'Search Results'

        # Adds the information of the first 10 compounds
        if len(results) > 10:
            results = results[:10]

        for compound in results:
            indv = compound.to_dict(properties=['iupac_name', 'cid', 'molecular_weight', 'molecular_formula'])
            embed.add_field(name=indv['molecular_formula'],
                            value="PubChem CID: {cid}\nIUPAC Name: {iupac}\nMolecular Mass: {mw} g/mol".format(
                                cid=indv['cid'], iupac=indv['iupac_name'], mw=indv['molecular_weight']
                            ),
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["information", "Information", "Info"])
    async def info(self, ctx, arg=None):
        # Gets extended information about the chemical by the PubChem CID
        if arg is None:
            await ctx.send("Please use the command with a CID")
            return
        if '.' in arg:
            await ctx.send("Invalid CID.")
            return

        try:
            # Gets the PubChem CID
            cid = int(arg)
            result = pcp.Compound.from_cid(cid).to_dict(properties=['molecular_formula', 'molecular_weight',
                                                                    'iupac_name', 'charge'])

            # Creates the image of the structure, overwrites if there is one, even from a different chemical
            pcp.download(outformat='PNG', path='images\\01.png', identifier=cid, namespace='cid', overwrite=True)
            file = discord.File("images\\01.png")

            # Creates the embed
            embed = discord.Embed(colour=discord.Colour.gold())
            embed.title = 'Search result'
            val = 'Molecular Formula: {}\nMolecular Weight: {} g/mol\nIUPAC name: {}\nCharge: {}'.format(
                result['molecular_formula'], result['molecular_weight'], result['iupac_name'], result['charge'])

            embed.add_field(name='PubChem CID: ' + str(cid), value=val)
            await ctx.send(embed=embed)
            await ctx.send(file=file)
        except ValueError:
            await ctx.send("Invalid CID.")


def setup(client):
    client.add_cog(Commands(client))
