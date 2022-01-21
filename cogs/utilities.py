import discord
import time
import simplejson as json
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow

startTime = time.time()


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        info.set_thumbnail(url=self.client.user.avatar_url)

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
