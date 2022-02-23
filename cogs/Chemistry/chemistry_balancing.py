import discord
from discord.ext import commands
from chemlib import Reaction, Compound


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliase=["Balance"])
    async def balance(self, ctx, *, arg):
        """Takes argument input, balances and returns the balance reaction in an embed.
            Input: aA + bB + ... -> cC + dD + ...
            It technically can take an infinite length reaction."""

        invalid = {
            "title": "Error",
            "description": "Please input a reaction.\n ```c!Balance aA + bB -> cC + dD```"
            }

        try:
            # Splits into products and reactants
            arg.replace(" ", "")
            reaction_split = arg.split("->")

            # Splits into individual compounds, no need to strip as the package does it
            rxn_reagents = reaction_split[0].split("+")
            rxn_products = reaction_split[1].split("+")

            # Converts strings to compounds and then into a reaction
            r = Reaction([Compound(reactant) for reactant in rxn_reagents],
                         [Compound(product) for product in rxn_products])

            balance_embed = discord.Embed(colour=discord.Colour.gold())

            # Checks whether the reaction is or isn't balanced before adding the field to the embed.
            if r.is_balanced:
                balance_embed.add_field(name="Balancing",
                                        value=f"The reaction ```{arg}``` is already balanced.")
            else:
                r.balance()
                balance_embed.add_field(name="Balancing",
                                        value=f"Reaction:\n```{arg}```\n\nBalanced:\n```{r.formula}```")

            await ctx.send(embed=balance_embed)

        except commands.CommandInvokeError:
            await ctx.send(embed=invalid)
        except commands.MissingRequiredArgument:
            await ctx.send(embed=invalid)
        except IndexError:
            await ctx.send(embed=invalid)
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Balancing]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
