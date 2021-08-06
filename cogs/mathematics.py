import discord
from discord.ext import commands
import math
import statistics as stats


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
        sqrt_val = math.sqrt(abs(dis))

        # Creates the embed
        embed = discord.Embed(color=discord.Colour.gold())
        embed.title = "Quadratic Calculation"
        embed.add_field(name="Input", value=f"```{a}x² + {b}x + {c} = 0```", inline=False)

        # checking condition for discriminant
        if dis > 0:
            embed.add_field(name="Solution",
                            value=f"```x = {(-b + sqrt_val) / (2 * a)} ; {(-b - sqrt_val) / (2 * a)}```")
        elif dis == 0:
            x = str(-b / (2 * a))
            embed.add_field(name="Solution",
                            value=f"```x = {x} ; {x}```")
        # when discriminant is less than 0
        else:
            x = str(- b / (2 * a))
            discriminant = str(sqrt_val)
            embed.add_field(name="Solution",
                            value=f"```x = {x}+{discriminant}i ; {x}-{discriminant}i```")

        await ctx.send(embed=embed)

    @commands.command(aliases=["Average", "avg", "Avg"])
    async def average(self, ctx, *, arg=None):
        if arg is None:
            arg_none = discord.Embed.from_dict(
                {"title": "Error",
                 "description": "Please use the command in the format:\n ```c!Average <value 1>, <value 2>, ...```"}
            )
            await ctx.send(embed=arg_none)
            return

        try:
            arg.replace(" ", "")
            values_txt = arg.split(",")
            values = [float(x) for x in values_txt]

            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Average",
                "color": 0xf1c40f,
                "description": f"Mean\n```{stats.mean(values)}```\nStandard Deviation\n```{stats.stdev(values)}```"
            }))

        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                import datetime
                bug_report.write(f"{datetime.datetime} [Average]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
