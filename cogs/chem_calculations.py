import asyncio
import discord
from discord.ext import commands
from chemlib import Compound
from discord import SelectMenu, SelectOption


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["MolarMass", "molarMass", "Molarmass"])
    async def molarmass(self, ctx, arg=None):
        if arg is None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "No input. Please use the command in the form:\n```c!Molarmass <formula>```"
            }))
            return

        try:
            compound = Compound(arg)
            embed = discord.Embed(title='Molar Mass', color=discord.Colour.gold())
            embed.add_field(name=f'Molar mass of {arg}:',
                            value=f"```{compound.molar_mass()} g/mol```",
                            inline=False)

            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "I seemed to have timed out due to the molecule. Please try with a different molecule or at another time."
            }))
        except IndexError:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!Molarmass <formula>```"
            }))
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."
                                                          }))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Molarmass]: {e}\n")

    @commands.command(aliases=["Mol"])
    async def mol(self, ctx, formula=None, arg=None):
        if formula is None or arg is None or float(arg) < 0:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!mol <formula> <number>```\nIf want to use scienteific notation, use 'E' instead of '× 10'. Example: `2.3E-3 = 2.3× 10⁻³`. Remember that the number can't be negative."
            }))
            return

        try:
            compound = Compound(formula)
            mw = compound.molar_mass()

            input_embed = {
                "title": "Your input",
                "color": 0xf1c40f,
                "description": f"Formula:\n```{formula}```\nNumber:\n```{float(arg)}```\n\nPlease select your units:"
            }

            msg = await ctx.send(embed=discord.Embed.from_dict(input_embed), components=[
                [
                    SelectMenu(custom_id='mass_units', options=[
                        SelectOption(label='mg', value='mg', description='milligrams'),
                        SelectOption(label='g', value='g', description='grams'),
                        SelectOption(label='kg', value='kg', description='kilograms'),
                        SelectOption(label='mmol', value='mmol', description='millimoles'),
                        SelectOption(label='mol', value='mol', description='moles')
                    ])
                ]])

            def check_selection(i: discord.Interaction, select_menu):
                return i.message == msg

            interaction, select_menu = await self.client.wait_for('selection_select', check=check_selection)

            units = select_menu.values[0]

            if units == "mg":
                final = f"{(float(arg)/1000)/mw} mol"
            elif units == "g":
                final = f"{float(arg)/mw} mol"
            elif units == "kg":
                final = f"{(float(arg)*1000)/mw} mol"
            elif units == "mmol":
                final = f"{(float(arg)/1000)*mw} g"
            else:
                final = f"{float(arg)*1000} g"

            final_embed = {
                "title": "Your input",
                "color": 0xf1c40f,
                "description": f"Formula:\n```{formula}```\nInput:\n```{float(arg)} {units}```\nResult:\n```{final}```"
            }

            await interaction.edit(embed=discord.Embed.from_dict(final_embed), components=[
                [
                    SelectMenu(custom_id='mass_units', options=[
                        SelectOption(label='mg', value='mg', description='milligrams'),
                        SelectOption(label='g', value='g', description='grams'),
                        SelectOption(label='kg', value='kg', description='kilograms'),
                        SelectOption(label='mmol', value='mmol', description='millimoles'),
                        SelectOption(label='mol', value='mol', description='moles')
                    ], disabled=True)
                ]])

        except IndexError:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid formula. Please use the command in the form:\n```c!mol <formula> <value>```\nIf want to use scienteific notation, use 'E' instead of '× 10'. Example: `2.3E-3 = 2.3× 10⁻³`. Remember that the number can't be negative."
            }))
        except ValueError:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid number. Please use the command in the form:\n```c!mol <formula> <value>```\nIf want to use scienteific notation, use 'E' instead of '× 10'. Example: `2.3E-3 = 2.3× 10⁻³`. Remember that the number can't be negative."
            }))
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error", "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as bug_report:
                bug_report.write(f"[Mass]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
