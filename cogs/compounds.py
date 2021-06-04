import discord
from discord.ext import commands
from chemlib import Compound


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["MolarMass", "molarMass", "Molarmass"])
    async def molarmass(self, ctx, arg=None):
        try:
            compound = Compound(arg)
            embed = discord.Embed(title='Molar Mass', color=discord.Colour.gold())
            embed.add_field(name='Molar mass of {formula}:'.format(formula=arg),
                            value="{mw} g/mol".format(mw=compound.molar_mass()),
                            inline=False)

            await ctx.send(embed=embed)

        except IndexError:
            await ctx.send("Invalid formula. Ex: `c!MolarMass H2O`")
        except commands.CommandInvokeError:
            await ctx.send("Please select a formula. Ex: `c!MolarMass H2O`")

    @commands.command(aliases=["Mass"])
    async def mass(self, ctx, formula=None, *, arg=None):
        if formula is None:
            await ctx.send("Please input a chemical formula. Ex: `c!mass H2O 1g`")
            return
        elif arg is None:
            await ctx.send("Please input a value. Ex: `c!mass H2O 1g`\nValid units: g, mg, mol, mmol.")
            return

        try:
            compound = Compound(formula)
            mw = compound.molar_mass()

            value = ''
            for char in arg:
                if char in '1234567890.':
                    value += char

            new_val = float(value.rstrip('.'))

            moles, mass = 0, 0
            if "mg" in arg:
                mass = new_val/1000
                moles = mass/mw
            elif "g" in arg:
                mass = new_val
                moles = mass/mw
            elif "mmol" in arg:
                moles = new_val/1000
                mass = new_val*mw
            elif "mol" in arg:
                moles = new_val
                mass = new_val*mw
            else:
                await ctx.send("Please send the value in mg, m, mmol, or mol in the form: `100mg` or `100 mg`")

            embed = discord.Embed(title='Mass', color=discord.Colour.gold())
            embed.add_field(name=formula,
                            value="Mass: {mass} g\nMoles: {moles} mol\nMolar Weight: {mw} g/mol".format(
                                mass=mass, moles=moles, mw=mw
                            ))
            await ctx.send(embed=embed)

        except IndexError:
            await ctx.send("Invalid formula. Ex: `c!mass H2O 1g`")


def setup(client):
    client.add_cog(Commands(client))
