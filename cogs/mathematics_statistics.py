import statistics
import discord
from discord.ext import commands
import statistics as stats


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Statistics", "stat", "Stat"])
    async def statistics(self, ctx, *, arg):
        """Returns  the results of various statistical functions of the input list. Input must be separated by comma."""
        try:
            values_txt = arg.split(",")
            values = [float(x) for x in values_txt]

            # Helper variables
            helper = {
                "Mean": stats.fmean(values),
                "Geometric Mean": stats.geometric_mean(values),
                "Harmonic Mean": stats.harmonic_mean(values),
                "Median": stats.median(values),
                "Modes": ', '.join([str(mode) for mode in stats.multimode(values)]),
                "Quartiles": ", ".join(map(str, [x for x in statistics.quantiles(values, n=4)])),
                "Sample Standard Deviation": stats.stdev(values),
                "Sample Variance": stats.variance(values)
            }

            embed = discord.Embed(color=discord.Colour.gold())

            for info in helper.keys():
                embed.add_field(
                    name=info,
                    value=helper[info],
                    inline=False
                )

            await ctx.send(embed=embed)

        except commands.MissingRequiredArgument:
            await ctx.send(embed=discord.Embed.from_dict(
                {"title": "Error",
                 "description": "Please use the command in the format:\n ```c!Average <value 1>, <value 2>, ...```"}))
        except statistics.StatisticsError:
            await ctx.send(embed=discord.Embed.from_dict(
                {"title": "Error",
                 "description": "Invalid inputs."}))
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                import datetime
                bug_report.write(f"[Average]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
