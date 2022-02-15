import discord
import time
import simplejson as json
from discord.ext import commands
from discord import SelectMenu, SelectOption

startTime = time.time()
lang = 'EN'


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Help"])
    # TODO: Explain more on the help command about how to use
    # TODO: Try do the 'help command' for each command
    async def help(self, ctx):
        try:
            with open("JSON/help.json", "r") as file:
                full_embed = json.load(file)

            lang = 'EN'
            menu = [[
                SelectMenu(custom_id='help_menu', placeholder='Categories', options=[
                    SelectOption(label=full_embed[lang]["botinfo"]['label'],
                                 value=full_embed[lang]["botinfo"]['value'],
                                 description=full_embed[lang]["botinfo"]['description']),
                    SelectOption(label=full_embed[lang]["chem"]['label'],
                                 value=full_embed[lang]["chem"]['value'],
                                 description=full_embed[lang]["chem"]['description']),
                    SelectOption(label=full_embed[lang]["pubchem"]['label'],
                                 value=full_embed[lang]["pubchem"]['value'],
                                 description=full_embed[lang]["pubchem"]['description']),
                    SelectOption(label=full_embed[lang]["mathematics"]['label'],
                                 value=full_embed[lang]["mathematics"]['value'],
                                 description=full_embed[lang]["mathematics"]['description']),
                    SelectOption(label=full_embed[lang]["all_commands"]['label'],
                                 value=full_embed[lang]["all_commands"]['value'],
                                 description=full_embed[lang]["all_commands"]['description'])
                ])
            ]]

            msg = await ctx.send(embed=discord.Embed.from_dict(full_embed[lang]['main']['embed']), components=menu)

            def check_selection(i: discord.Interaction, select_menu):
                return i.message == msg

            interaction, select_menu = await self.client.wait_for('selection_select', check=check_selection)

            selection = select_menu.values[0]

            # Allow for up to 10 times
            i, x = 5, 0

            while x < i:
                if x == (i-1):
                    await interaction.edit(components=[[SelectMenu(custom_id='none',
                                                                   disabled=True,
                                                                   placeholder='Disabled',
                                                                   options=[SelectOption(label='Filler', value='filler')])]])

                await ctx.send(embed=discord.Embed.from_dict(full_embed[lang][selection]['embed']))
                await interaction.defer()
                # await interaction.respond(embed=discord.Embed.from_dict(full_embed[lang][selection]['embed']), hidden=True)

                def check_selection(i: discord.Interaction, select_menu):
                    return i.message == msg

                interaction, select_menu = await self.client.wait_for('selection_select', check=check_selection)

                selection = select_menu.values[0]
                x += 1

        except Exception as e:
            print(e)
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Help]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
