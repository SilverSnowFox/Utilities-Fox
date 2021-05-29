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

            # Limiting the number of products of reactants
            if (len(reaction_products) > 4) or (len(reaction_reagents) > 4):
                await ctx.send("Please limit to at most 4 reactants or products.")
                return

            # Converts into Compound objects
            products = []
            for product in reaction_products:
                products.append(Compound(product))
            reactants = []
            for reactant in reaction_reagents:
                reactants.append(Compound(reactant))

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
