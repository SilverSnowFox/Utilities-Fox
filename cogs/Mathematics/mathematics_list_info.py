import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # TODO: Check that the command works for numbers, characters, and words
    # TODO: Add command names
    # TODO: Add command to the help menu
    @commands.command()
    async def list_info(self, ctx, *arg: str):
        """Takes in a list and returns information from the list."""
        items = str(arg).split(',')     # Makes a list of all the items
        cleaned = [item.strip() for item in items]

        length = cleaned.__len__()
        numbers, alphabetic, other = 0, 0, 0

        for item in cleaned:
            try:
                # Is an int or a float
                float(item)
                length += 1
            except ValueError:
                # Gives error when it isn't a number, or just a number
                if item.isalpha():
                    # Checks that all the characters in the string are alphabetic
                    alphabetic += 1
                else:
                    other += 1

        embed = discord.Embed(color=discord.Colour.gold())
        embed.title("List information")
        embed.add_field(name="Length", value=str(length))
        embed.add_field(name="Counts", value=f"Numbers: {numbers}\nAlphabetic-only text: {alphabetic}\nOthers: {other}")

        if numbers == length:
            # TODO: Use the stuff from mathematics_statistics.py to calculate list information, since we check that it is all numbers
            pass

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
