import discord
from discord.ext import commands
import statistics as stats


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Average", "avg", "Avg"])
    # TODO: Rename 'average' to statistics
    # TODO: Add in the rest of the statistic functions
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
