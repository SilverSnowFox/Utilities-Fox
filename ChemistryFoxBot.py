import discord
import json
import os
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned_or("c!"))
client.remove_command('help')


@client.command()
async def reload(ctx, extension):
    try:
        owners = json.load(open('data/owners.json'))
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
        owners = json.load(open('data/owners.json'))
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
        owners = json.load(open('data/owners.json'))
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


## Top.gg server count

import topgg

dbl_token = json.load(open("data/TopggToken.json"))
client.topggpy = topgg.DBLClient(client, dbl_token, autopost=True, post_shard_count=True)


@client.event
async def on_autopost_success():
    print(f"Posted server count ({client.topggpy.guild_count}), shard count ({client.shard_count})")


##########


json_file = open("data/token.json")
token = json.load(json_file)

client.run(token)
