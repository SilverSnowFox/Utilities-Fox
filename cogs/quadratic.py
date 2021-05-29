import discord
from discord.ext import commands
import math


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Quadratic"])
    async def quadratic(self, ctx, a=None, b=None, c=None):
        # Calculates the quadratic roots
        if a is None or b is None or c is None:
            await ctx.send("Invalid input. Please use the command in the form:\n" +
                           "`c!quadratic [a] [b] [c]`\nFrom ax^2 + bx + c = 0")
            return

        # Calculates the discriminant
        dis = b * b - 4 * a * c
        sqrt_val = math.sqrt(abs(dis))

        # Creates the embed
        embed = discord.Embed(color=discord.Colour.gold())
        embed.title = "Quadratic Calculation"

        # checking condition for discriminant
        if dis > 0:
            embed.add_field(name="Solution", value="x = " + str((-b + sqrt_val) / (2 * a))
                                                       + " ; " + str(((-b - sqrt_val) / (2 * a))))
        elif dis == 0:
            embed.add_field(name="Solutions", value="x = " + str(-b / (2 * a)) + " ; " +
                                                        str(-b / (2 * a)))
            # when discriminant is less than 0
        else:
            embed.add_field(name="Solutions", value="x = " +
                                                    str(- b / (2 * a)) + "+" + str(sqrt_val) + "i" +
                                                    " ; " +
                                                    str(- b / (2 * a)) + "-" + str(sqrt_val) + "i")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
