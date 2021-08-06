import discord
from discord.ext import commands
from chemlib import Reaction, Compound


class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliase=["Balance"])
    async def balance(self, ctx, *, arg=None):
        invalid = {
            "title": "Error",
            "description": "Please input a reaction.\n ```c!Balance aA + bB -> cC + dD```"
            }
        # Gets a chemical reaction and balances it
        if arg is None:
            await ctx.send(embed=discord.Embed.from_dict(invalid))
            return

        try:
            # Create embed and send embed with instructions on input.
            start_embed = discord.Embed(colour=discord.Colour.gold())
            start_embed.title = 'Balancing'

            # Splits into products and reactants
            arg.replace(" ", "")
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
                                        value=f"The reaction ```{arg}``` is already balanced.")

            # Checks that the products and reactants are related. If they aren't the is_balance would fail and the
            # balancing would result in the same reaction.
            # a = r
            r.balance()
            balance_embed.add_field(name="Balancing",
                                    value=f"Reaction:\n```{arg}```\n\nBalanced:\n```{r.formula}```")
            await ctx.send(embed=balance_embed)

        except commands.CommandInvokeError:
            await ctx.send(embed=invalid)
        except IndexError:
            await ctx.send(embed=invalid)
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Balancing]: {e}\n")


def setup(client):
    client.add_cog(Command(client))
