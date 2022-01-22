import discord
from discord.ext import commands
from math import sqrt


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Quadratic"])
    async def quadratic(self, ctx, a=None, b=None, c=None):
        # Calculates the quadratic roots
        # Checks not missing values, as if 1 or more is missing, c will be the first one missing
        if c is None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!quadratic <a> <b> <c>```\nFrom ax² + bx + c = 0"
            }))
            return

        a, b, c = float(a), float(b), float(c)

        # Calculates the discriminant
        dis = (b * b) - (4 * a * c)

        # Creates the embed
        embed = discord.Embed(color=discord.Colour.gold())
        embed.title = "Quadratic Calculation"
        embed.add_field(name="Input", value=f"```{a}x² + {b}x + {c} = 0```", inline=False)

        # checking condition for discriminant
        if dis > 0:
            embed.add_field(name="Solution",
                            value=f"```x = {(-b + sqrt(dis)) / (2 * a)} ; {(-b - sqrt(dis)) / (2 * a)}```")
        elif dis == 0:
            x = str(-b / (2 * a))
            embed.add_field(name="Solution",
                            value=f"```x = {x} ; {x}```")
        # when discriminant is less than 0
        else:
            x = str(- b / (2 * a))
            embed.add_field(name="Solution",
                            value=f"```x = {x}+{sqrt(abs(dis))}i ; {x}-{sqrt(abs(dis))}i```")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
