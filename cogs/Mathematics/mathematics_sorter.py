import discord
from discord.ext import commands
from discord import Button, ButtonStyle


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # TODO: Check that the command works for numbers, characters, and words
    # TODO: Add command names
    # TODO: Add command to help
    @commands.command()
    async def sorter(self, ctx, *arg: str):
        """Takes in a list of letters, words or numbers and sorts them. Button for ascending or descending."""
        items = str(arg).split(',')     # Makes a list of all the items
        cleaned = [item.strip() for item in items]

        msg = await ctx.send("How would you like to sort it?", components=[
            Button(label="Ascending", custom_id="ascending", style=ButtonStyle.blurple),
            Button(label="Descending", custom_id="descending", style=ButtonStyle.blurple)
        ])

        # Waits for user to click button
        def check_button(i: discord.Interaction, button):
            return i.message == msg

        interaction, button = await self.client.wait_for('button_click', check=check_button)

        await msg.edit("How would you like to sort it?", components=[
            Button(label="Ascending", custom_id="ascending", style=ButtonStyle.blurple, disabled=True),
            Button(label="Descending", custom_id="descending", style=ButtonStyle.blurple, disabled=True)
        ])

        if interaction.custom_id == "ascending":
            cleaned.sort()
        else:
            cleaned.sort(reverse=True)
        await ctx.send(','.join(cleaned))

def setup(client):
    client.add_cog(Commands(client))
