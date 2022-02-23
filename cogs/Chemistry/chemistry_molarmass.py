import asyncio
import discord
from functions import chemlib_helper
from discord.ext import commands
from chemlib import Compound


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["MolarMass", "molarMass", "Molarmass"])
    async def molarmass(self, ctx, compound: Compound):
        """Calculates the molar mass of a compound up to 10000 molecules large."""
        try:
            # Limiting the number of molecules, as any large would start to take too long to calculate
            if not chemlib_helper.molarmass_limit_check(compound):
                await ctx.send(embed=discord.Embed.from_dict({
                    "title": "Error",
                    "description": "Please limit your molecule size to 10000 molecules or less."
                }))
                return

            embed = discord.Embed(title='Molar Mass', color=discord.Colour.gold())
            embed.add_field(name=f'Molar mass of {compound.formula}:',
                            value=f"```{compound.molar_mass()} g/mol```",
                            inline=False)

            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "I seemed to have timed out due to the molecule. Please try with a different molecule or at another time."
            }))
        except IndexError:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!Molarmass <formula>```"
            }))
        except commands.MissingRequiredArgument:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "No input. Please use the command in the form:\n```c!Molarmass <formula>```"
            }))
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."
                                                          }))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Molarmass]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))