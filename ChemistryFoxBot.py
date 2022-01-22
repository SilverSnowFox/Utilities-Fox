import discord
import json
import os
from functions.package_installer import install_req
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned_or("c!"))
client.remove_command('help')

# TODO: Merge the three cog commands into one
# TODO: Add in Owner commands for information

install_req()

@client.command()
async def reload(ctx, extension):
    try:
        owners = json.load(open('JSON/owners.json'))
        if ctx.message.author.id in owners:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f"cogs.{extension} reloaded.")
        else:
            await ctx.send("This is an owner only command.")
    except commands.CommandInvokeError:
        await ctx.send("Cog doesn't exist.")
    # To log all extra exceptions and later fix
    except Exception as e:
        with open("data/error_log.txt", "a") as bug_report:
            import datetime
            bug_report.write(f"{datetime.datetime} [BugReport]: {e}")


@client.command()
async def load(ctx, extension):
    try:
        owners = json.load(open('JSON/owners.json'))
        if ctx.message.author.id in owners:
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'cogs.{extension} loaded.')
        else:
            await ctx.send("This is an owner only command.")
    except commands.CommandInvokeError:
        await ctx.send("Cog doesn't exist.")
    # To log all extra exceptions and later fix
    except Exception as e:
        with open("data/error_log.txt", "a") as bug_report:
            import datetime
            bug_report.write(f"{datetime.datetime} [BugReport]: {e}")


@client.command()
async def unload(ctx, extension):
    try:
        owners = json.load(open('JSON/owners.json'))
        if ctx.message.author.id in owners:
            client.unload_extension(f'cogs.{extension}')
            await ctx.send(f'cogs.{extension} unloaded.')
        else:
            await ctx.send("This is an owner only command.")
    except commands.CommandInvokeError:
        await ctx.send("Cog doesn't exist.")
    # To log all extra exceptions and later fix
    except Exception as e:
        with open("data/error_log.txt", "a") as bug_report:
            import datetime
            bug_report.write(f"{datetime.datetime} [BugReport]: {e}")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print(f'Bot is online. Logged in as {client.user.name}')
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.Game('with some chemicals.'))

##########

with open("JSON/token.json") as json_file:
    token = json.load(json_file)

client.run(token)
