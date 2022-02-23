import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from chemlib import Element


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Element'])
    async def element(self, ctx, element: Element):
        """Displays the information about an element by its letter abbreviation. Eg: Au"""
        try:
            # Created embed and a copy for when disabling button
            embed = em1 = discord.Embed(title=element['Element'], color=discord.Colour.gold())

            embed.set_thumbnail(url=f'https://images-of-elements.com/t/{element["Element"].lower()}.png')
            embed.add_field(name='Symbol', value=element['Symbol'])
            embed.add_field(name='Atomic Number', value=f"{int(element['AtomicNumber'])}")
            embed.add_field(name='Atomic Mass', value=element['AtomicMass'])
            embed.add_field(name='Type', value=element['Type'])
            phase = element['Phase']
            embed.add_field(name='Phase', value=phase[0].upper() + phase[1:])
            embed.add_field(name='Electronegativity', value=element['Electronegativity'])
            embed.add_field(name='Electron Config', value=element['Config'])
            embed.add_field(name='Melting Point', value=f"{element['MeltingPoint']} K")
            embed.add_field(name='Boiling Point', value=f"{element['BoilingPoint']} K")

            # Sends first embed with condensed info + Button
            msg = await ctx.send(embed=embed, components=[Button(label='Full info', custom_id='element_full', style=ButtonStyle.blurple)])

            # Waits for user to click button
            def check_button(i: discord.Interaction, button):
                return i.message == msg
            interaction, button = await self.client.wait_for('button_click', check=check_button)

            # Adds the rest of the information to the embed
            embed.add_field(name='Neutrons-Protons-Electrons',
                            value=f"{int(element['Neutrons'])}, {int(element['Protons'])}, {int(element['Electrons'])}")
            embed.add_field(name='Radioactive', value=f"{element['Radioactive']}")
            embed.add_field(name='Specific Heat', value=f"{element['SpecificHeat']} J/(g°C)")
            embed.add_field(name='Phase at STP', value=f"{element['Phase']}")
            embed.add_field(name='Density', value=f"{element['Density']} g/cm³")
            embed.add_field(name='Group', value=f"{element['Group']}")
            embed.add_field(name='Period', value=f"{element['Period']}")
            frstIon = element['FirstIonization']
            embed.add_field(name='First Ionization', value=f"{frstIon} eV, {frstIon*96.49} kJ mol⁻¹")

            # Updates embed to one with disabled button, then sends hidden embed with full info.
            await interaction.respond(embed=embed, hidden=True)
            await msg.edit(embed=em1, components=[Button(label='Full info', custom_id='element_full', style=ButtonStyle.blurple, disabled=True)])

        except IndexError:
            await ctx.send("Invalid element symbol. Example of usage: `c!Element Pb`")
        except commands.MissingRequiredArgument:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "No input. Please use the command in the form:\n```c!Element <symbol>```"
            }))
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as file:
                file.write(f"[Element]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
