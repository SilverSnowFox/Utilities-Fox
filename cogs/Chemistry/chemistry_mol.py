import discord
from discord.ext import commands
from chemlib import Compound
from discord import SelectMenu, SelectOption
from functions import chemlib_helper


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Mol"])
    async def mol(self, ctx, val: float = 1.0, compound: Compound = None):
        """Takes a value argument (optional), a compound (optional) and sends an embed. The user must then select
            its unit and the target unit. The program will compute the conversion unless it requires molar weight
            and the user didn't input a compound."""

        # TODO: Remake the mol calculation commmand with more instructions and text
        # TODO: Attempt to remake the unit conversion into a switch-case to improve it

        if val < 0:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. The number can't be negative."
            }))
            return

        try:
            if not chemlib_helper.molarmass_limit_check(compound):
                await ctx.send(embed=discord.Embed.from_dict({
                    "title": "Error",
                    "description": "Please limit your molecule size to 10000 molecules or less."
                }))
                return

            mw = compound.molar_mass()

            input_embed = {
                "title": "Your input",
                "color": 0xf1c40f,
                "description": f"Formula:\n```{compound}```\nNumber:\n```{float(val)}```\n\nPlease select your units:"
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
                final = f"{(float(val) / 1000) / mw} mol"
            elif units == "g":
                final = f"{float(val) / mw} mol"
            elif units == "kg":
                final = f"{(float(val) * 1000) / mw} mol"
            elif units == "mmol":
                final = f"{(float(val) / 1000) * mw} g"
            else:
                final = f"{float(val) * 1000} g"

            final_embed = {
                "title": "Your input",
                "color": 0xf1c40f,
                "description": f"Formula:\n```{compound}```\nInput:\n```{float(val)} {units}```\nResult:\n```{final}```"
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

        except commands.MissingRequiredArgument:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "Invalid input. Please use the command in the form:\n```c!mol <compound> <number (will be 1.0 if no input)>```\nIf want to use scienteific notation, use 'E' instead of '× 10'. Example: `2.3E-3 = 2.3× 10⁻³`. Remember that the number can't be negative."
            }))
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
                bug_report.write(f"[Mol]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
