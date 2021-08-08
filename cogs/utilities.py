import discord
import time
import simplejson as json
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow, SelectMenu, SelectOption

startTime = time.time()


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Help"])
    async def help(self, ctx):
        try:
            with open("data/help.json", "r") as file:
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

            msg = await ctx.send(embed=discord.Embed.from_dict(full_embed['EN']['main']['embed']), components=menu)

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
                await interaction.respond(embed=discord.Embed.from_dict(full_embed[lang][selection]['embed']),
                                          hidden=True)

                def check_selection(i: discord.Interaction, select_menu):
                    return i.message == msg

                interaction, select_menu = await self.client.wait_for('selection_select', check=check_selection)

                selection = select_menu.values[0]
                x += 1

        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Help]: {e}\n")

    @commands.command(aliases=["Latency"])
    async def latency(self, ctx):
        await ctx.send(f"Latency: {round(self.client.latency * 1000)} ms")

    @commands.command(aliases=["Vote"])
    async def vote(self, ctx):
        vote_embed = {"color": 16766720,
                      "title": "Vote",
                      "description": "Help me by voting!"}
        await ctx.send(embed=discord.Embed.from_dict(vote_embed), components=[
            ActionRow(
                Button(label="Top.gg", style=ButtonStyle.url, url="https://top.gg/bot/846917416558788638/vote"),
                Button(label="DisBotList.xyz", style=ButtonStyle.url,
                       url="https://disbotlist.xyz/bot/846917416558788638/vote")
            )])

    @commands.command(aliases=["Invite"])
    async def invite(self, ctx):
        invite_embed = {"color": 16766720,
                        "title": "Invite",
                        "description": "Click below to invite me to your server!"}
        await ctx.send(embed=discord.Embed.from_dict(invite_embed), components=[
            Button(label="Invite me to your server", style=ButtonStyle.url,
                   url="https://discord.com/api/oauth2/authorize?client_id=846917416558788638&permissions=18432&scope=bot")
        ])

    @commands.command(aliases=["Botinfo"])
    async def botinfo(self, ctx):

        from datetime import timedelta
        import sys

        py = sys.version_info

        info = discord.Embed(colour=discord.Colour.gold())
        info.title = "Information"
        info.add_field(name="Bot Name", value=self.client.user.name, inline=False)
        info.add_field(name="Prefix", value="`c!` or `@mention`", inline=False)
        info.add_field(name="Latency", value=f"{round(self.client.latency * 1000)} ms", inline=False)
        info.add_field(name="Servers", value=f"{len(self.client.guilds)}", inline=False)
        info.add_field(name="Bot Owner", value="SevenTails#7757", inline=False)
        info.add_field(name="Uptime", value=f"{timedelta(seconds=round(time.time() - startTime))}", inline=False)
        info.add_field(name="Version", value="2", inline=False)
        info.add_field(name="Coded in", value=f"Python {py.major}.{py.minor}.{py.micro} {py.releaselevel}")
        info.set_thumbnail(url="https://cdn.discordapp.com/attachments/872274530041753651/873112938859360266/1534287126999.png")

        await ctx.send(embed=info, components=[
            Button(label="Invite me", style=ButtonStyle.url,
                   url="https://discord.com/api/oauth2/authorize?client_id=846917416558788638&permissions=18432&scope=bot")
        ])

    @commands.command(aliases=["Bugreport"])
    async def bugreport(self, ctx, *, report=None):
        if report is None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Please input a bug report. \nFormat: ```c!bugreport <report>```"
            }))
            return

        try:
            with open("data/bugreport.txt", "a") as file:
                file.write(f"{ctx.author.name}#{ctx.author.discriminator}:{report}\n")
            await ctx.send("Thank you for your feedback!")

        # To log all extra exceptions and later fix
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[BugReport]: {e}\n")

    @commands.command(aliases=["Suggestion"])
    async def suggestion(self, ctx, *, suggestion=None):
        if suggestion is None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Please input a suggestion. \nFormat: ```c!suggestion <text>```"
            }))
            return

        try:
            with open("data/suggestion.txt", "a") as file:
                file.write(f"{ctx.author.name}#{ctx.author.discriminator}:{suggestion}\n")
            await ctx.send("Thank you for your feedback!")

        # To log all extra exceptions and later fix
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[BugReport]: {e}\n")

    @commands.command(aliases=["Changelog"])
    async def changelog(self, ctx):
        with open("data/changelog.json", "r") as file:
            changelog_embed = json.load(file)
        await ctx.send(embed=discord.Embed.from_dict(changelog_embed['v2']))


def setup(client):
    client.add_cog(Commands(client))
