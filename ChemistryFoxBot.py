import discord
import json
import os
from discord.ext import commands

client = commands.Bot(command_prefix=["c!", "C!"])
client.remove_command('help')


@client.command()
async def reload(ctx, extension):
    try:
        if ctx.message.author.id == 231580977405624320:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f"cogs.{extension} reloaded.")
        else:
            await ctx.send("This is an owner only command.")
    except commands.CommandInvokeError:
        await ctx.send("Cog doesn't exist.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print(f'Bot is online. Logged in as {client.user.name}')
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.Game('with some ´chemicals.'))


json_file = open("token.json")
token = json.load(json_file)

client.run(token)
