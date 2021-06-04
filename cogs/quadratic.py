import discord
from discord.ext import commands
import math


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Quadratic"])
    async def quadratic(self, ctx, a=None, b=None, c=None):
        # Calculates the quadratic roots
        # Checks not missing values, as if 1 or more is missing, c will be the first one missing
        if c is None:
            await ctx.send("Invalid input. Please use the command in the form:\n" +
                           "`c!quadratic [a] [b] [c]`\nFrom ax^2 + bx + c = 0")
            return

        a, b, c = float(a), float(b), float(c)

        # Calculates the discriminant
        dis = (b * b) - (4 * a * c)
        sqrt_val = math.sqrt(abs(dis))

        # Creates the embed
        embed = discord.Embed(color=discord.Colour.gold())
        embed.title = "Quadratic Calculation"

        # checking condition for discriminant
        if dis > 0:
            embed.add_field(name="Solution", value="x = {} ; {}".format(
                (-b + sqrt_val) / (2 * a), (-b - sqrt_val) / (2 * a)))
        elif dis == 0:
            x = str(-b / (2 * a))
            embed.add_field(name="Solutions", value="x = {x} ; {x}".format(x=x))
        # when discriminant is less than 0
        else:
            x = str(- b / (2 * a))
            discriminant = str(sqrt_val)
            embed.add_field(name="Solutions", value="x = {x}+{im}i ; {x}-{im}i".format(
                x=x, im=discriminant))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
