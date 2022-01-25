import discord
import json
import os
from functions.package_installer import install_req
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned_or("c!"))
client.remove_command('help')

# TODO: Add in Owner commands for information

install_req()


@client.command(aliases=["Cog"])
async def cog(ctx, action, cogType, folder, extension):

    # To check that cog exists
    if not os.path.isfile(f"{cogType}/{folder}/{extension}.py"):
        await ctx.send("Cog doesn't exist.")
        return

    try:
        # Checks that user is an admin
        with open("JSON/owners.json") as file:
            admins = json.load(file)
            if str(ctx.message.author.id) not in admins:
                await ctx.send("This is an admin only command.")
                return

        # Checks for each Cog action. If use one cog more than the other can change their order.
        if action == "reload":
            client.unload_extension(f'{cogType}.{folder}.{extension}')
            client.load_extension(f'{cogType}.{folder}.{extension}')
            await ctx.send(f"Cog {extension} reloaded")
        elif action == "load":
            client.load_extension(f'{cogType}.{folder}.{extension}')
            await ctx.send(f"Cog {extension} loaded.")
        elif action == "unload":
            client.unload_extension(f'{cogType}.{folder}.{extension}')
            await ctx.send(f"Cog {extension} unloaded.")
        else:
            await ctx.send("That cog action doesn't exist.")

    except FileNotFoundError:
        await ctx.send("admin.json doesn't exist.")
    except discord.ext.commands.ExtensionAlreadyLoaded:
        await ctx.send(f"Cog {extension} already loaded.")
    except discord.ext.commands.ExtensionNotLoaded:
        await ctx.send(f"Cog {extension} already unloaded.")
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
