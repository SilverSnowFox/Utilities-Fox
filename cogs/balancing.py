import discord
from discord.ext import commands
from chemlib import Reaction, Compound


class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliase=["Balance"])
    async def balance(self, ctx, *, arg=None):
        # Gets a chemical reaction and balances it
        if arg is None:
            await ctx.send("Please input a reaction")
            return

        try:
            # Create embed and send embed with instructions on input.
            start_embed = discord.Embed(colour=discord.Colour.gold())
            start_embed.title = 'Balancing'
            # Splits into products and reactants
            reaction_split = arg.split("->")
            # Splits into individual compounds, no need to strip as the package does it
            reaction_reagents = reaction_split[0].split("+")
            reaction_products = reaction_split[1].split("+")

            # Converts into Compound objects
            products = [Compound(product) for product in reaction_products]
            reactants = [Compound(reactant) for reactant in reaction_reagents]

            # Creates the reaction
            r = Reaction(reactants, products)

            balance_embed = discord.Embed(colour=discord.Colour.gold())

            if r.is_balanced:
                balance_embed.add_field(name="Balancing",
                                        value="Reaction:\n" + arg + "\n It's already balanced.")
            else:
                r.balance()
                balance_embed.add_field(name="Balancing",
                                        value="Reaction:\n" + arg + "\n\nBalanced:\n " + r.formula)

            await ctx.send(embed=balance_embed)

        except:
            await ctx.send("Something went wrong. Please check format, try again or contact my creator.")


def setup(client):
    client.add_cog(Command(client))
