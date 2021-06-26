from discord.ext import commands
import json


class Ownercmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ServerCount", "Servers"])
    async def server_count(self, ctx):
        try:
            owners = json.load(open("../owners.json"))
            if ctx.message.author.id in owners:
                await ctx.send(f"I'm currently online in {len(self.client.guilds)} servers")
            else:
                await ctx.send("This is an owner only command.")
        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(Ownercmd(client))