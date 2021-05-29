import discord
from discord.ext import commands
from chemlib import Compound


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["MolarMass", "molarMass", "Molarmass"])
    async def molarmass(self, ctx, arg=None):
        if arg is None:
            await ctx.send("Please select a calculation. \n c!MolarMass [compound formula]")
            return
        compound = Compound(arg)
        embed = discord.Embed(title='Molar Mass', color=discord.Colour.gold())
        embed.add_field(name='Molar mass of ' + arg + ':', value=str(compound.molar_mass()) + 'g/mol',
                        inline=False)

        percent_by_mass = ''
        i = 0
        while i < len(arg) - 1:
            if arg[i].isalpha() and arg[i].isupper() and arg[i+1].isalpha():
                chem = arg[i] + arg[i+1]
                percent_by_mass += chem + ': ' + str(compound.percentage_by_mass(chem)) + ' %\n'
                i += 1
            elif arg[i].isalpha():
                percent_by_mass += arg[i] + ': ' + str(compound.percentage_by_mass(arg[i])) + ' %\n'
            i += 1
        if arg[-1].isalpha() and arg[-1].isupper():
            percent_by_mass += arg[i] + ': ' + str(compound.percentage_by_mass(arg[i])) + ' %\n'

        embed.add_field(name='Percent by mass', value=percent_by_mass, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=["Mass"])
    async def mass(self, ctx, formula=None, *, arg=None):
        if formula is None:
            await ctx.send("Please input a chemical formula")
            return
        elif arg is None:
            await ctx.send("Please input a value. \n Valid units: g, mg, L, mL, mol, mmol")
            return

        compound = Compound(formula)
        mw = compound.molar_mass()

        value = ''
        for char in arg:
            if char in '1234567890.':
                value += char
        if value[-1] == '.':
            new_val = float(value[0:-1])
        else:
            new_val = float(value)

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
            await ctx.send("Please send the value in mg, m, mmol, or mol in the form: '100mg")

        embed = discord.Embed(title='Mass', color=discord.Colour.gold())
        embed.add_field(name='Compound', value=formula)
        embed.add_field(name='Mass', value=str(mass) + ' g')
        embed.add_field(name='Moles', value=str(moles) + ' mol')
        embed.add_field(name='Molar Mass', value=str(mw) + ' g/mol')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
