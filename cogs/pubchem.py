import discord
import pubchempy as pcp
from discord.ext import commands
from discord import Button, ButtonStyle


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Search"])
    # Searches for a compound by name, returning the CID and some general info about the compound
    async def search(self, ctx, *, arg=None):
        # Checks if used added an argument
        if arg is None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!search <compound>```"
            }))
            return

        try:
            # Gets the results of the search
            results = pcp.get_compounds(arg, 'name')

            if len(results) == 0:
                await ctx.send("Unable to find any results.")
                return

            embed = discord.Embed(colour=discord.Colour.gold())
            embed.title = 'Top 10 Search Results'

            # Adds the information of the first 10 compounds
            if len(results) > 10:
                results = results[:10]

            for compound in results:
                chem = compound.to_dict(properties=['iupac_name', 'cid', 'molecular_weight', 'molecular_formula'])
                embed.add_field(name=chem['molecular_formula'],
                                value=f"PubChem CID: {chem['cid']}\nIUPAC Name: {chem['iupac_name']}\nMolecular Mass: {chem['molecular_weight']} g/mol",
                                inline=False)
            await ctx.send(embed=embed, components=[Button(label='PubChem Search', style=ButtonStyle.url,
                                                           url=f"https://pubchem.ncbi.nlm.nih.gov/#query={arg}")])

        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Search]: {e}\n")

    @commands.command(aliases=["information", "Information", "Info"])
    async def info(self, ctx, arg=None):
        # Gets extended information about the chemical by the PubChem CID
        if arg is None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "You didn't input a CID. Please use the command in the form:\n```c!info <CID>```"
            }))
            return
        if '.' in arg:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!info <CID>```"
            }))
            return

        try:
            # Gets the PubChem CID
            cid = int(arg)
            result = pcp.Compound.from_cid(cid).to_dict(properties=['molecular_formula', 'molecular_weight',
                                                                    'iupac_name', 'charge'])
            # Creates the image of the structure, overwrites if there is one, even from a different chemical
            pcp.download(outformat='PNG', path='data/01.png', identifier=cid, namespace='cid', overwrite=True)
            file = discord.File("data/01.png", filename="01.png")

            # Creates the embed
            embed = discord.Embed(colour=discord.Colour.gold())
            embed.title = 'Search result'
            val = f"Molecular Formula: {result['molecular_formula']}\nMolecular Weight: {result['molecular_weight']} g/mol\nIUPAC name: {result['iupac_name']}\nCharge: {result['charge']}"

            embed.add_field(name=f'PubChem CID: {cid}', value=val)
            embed.set_image(url="attachment://01.png")
            await ctx.send(embed=embed, file=file, components=[Button(label='PubChem Search', style=ButtonStyle.url,
                                                                      url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}")])
        except ValueError:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!info <CID>```"
            }))
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Info]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
