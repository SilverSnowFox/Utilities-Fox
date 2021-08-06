import chemlib
import discord
from discord.ext import commands
from discord import Button, ButtonStyle


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Element'])
    async def element(self, ctx, arg=None):
        if arg is None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": "No input. Please use the command in the form:\n```c!Element <symbol>```"
            }))
            return

        try:
            information = chemlib.Element(arg)
            element = information['Element']

            # Created embed and a copy for when disabling button
            embed = discord.Embed(title=element, color=discord.Colour.gold())
            em1 = embed

            embed.set_thumbnail(url=f'https://images-of-elements.com/t/{element.lower()}.png')
            embed.add_field(name='Symbol', value=information['Symbol'])
            embed.add_field(name='Atomic Number', value=f"{int(information['AtomicNumber'])}")
            embed.add_field(name='Atomic Mass', value=information['AtomicMass'])
            embed.add_field(name='Type', value=information['Type'])
            phase = information['Phase']
            embed.add_field(name='Phase', value=phase[0].upper() + phase[1:])
            embed.add_field(name='Electronegativity', value=information['Electronegativity'])
            embed.add_field(name='Electron Config', value=information['Config'])
            embed.add_field(name='Melting Point', value=f"{information['MeltingPoint']} K")
            embed.add_field(name='Boiling Point', value=f"{information['BoilingPoint']} K")

            # Sends first embed with condensed info + Button
            msg = await ctx.send(embed=embed, components=[Button(label='Full info', custom_id='element_full', style=ButtonStyle.blurple)])

            # Waits for user to click button
            def check_button(i: discord.Interaction, button):
                return i.message == msg
            interaction, button = await self.client.wait_for('button_click', check=check_button)

            # Adds the rest of the information to the embed
            embed.add_field(name='Neutrons-Protons-Electrons',
                            value=f"{int(information['Neutrons'])}, {int(information['Protons'])}, {int(information['Electrons'])}")
            embed.add_field(name='Radioactive', value=f"{information['Radioactive']}")
            embed.add_field(name='Specific Heat', value=f"{information['SpecificHeat']} J/(g°C)")
            embed.add_field(name='Phase at STP', value=f"{information['Phase']}")
            embed.add_field(name='Density', value=f"{information['Density']} g/cm³")
            embed.add_field(name='Group', value=f"{information['Group']}")
            embed.add_field(name='Period', value=f"{information['Period']}")

            # Updates embed to one with disabled button, then sends hidden embed with full info.
            await interaction.respond(embed=embed, hidden=True)
            await msg.edit(embed=em1, components=[Button(label='Full info', custom_id='element_full', style=ButtonStyle.blurple, disabled=True)])

        except IndexError:
            await ctx.send("Invalid element symbol. Example of usage: `c!Element Pb`")
        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as file:
                file.write(f"[Element]: {e}\n")

    @commands.command(aliases=["Constants"])
    async def constants(self, ctx):
        try:
            constants = discord.Embed.from_dict({
                "title": "Common Constants",
                "color": 0xf1c40f,
                "fields": [
                    {"name": "Avogadro's Number", "value": "6.022 14 × 10²³ mol⁻¹"},
                    {"name": "Faraday Constant", "value": "96 485.33 C mol⁻¹"},
                    {"name": "Atomic Mass Constant", "value": "1 amu = 1.660 538 × 10⁻²⁷ kg"},
                    {"name": "Molar Gas Constant", "value": "8.3144 J mol⁻¹ K⁻¹, 0.082057 L atm K⁻¹ mol⁻¹"},
                    {"name": "Coulomb's Constant", "value": "8.987551 × 10⁹ N m² C⁻²"},
                    {"name": "Light Speed (Vacuum)", "value": "299 792 558 m s⁻¹"},
                    {"name": "Boltzmann Constant", "value": "1.38065 × 10⁻²³ J K⁻¹"},
                    {"name": "Electron Charge", "value": "1.602176 × 10⁻¹⁹ C"},
                    {"name": "Standard gravity", "value": "9.80665 m s⁻²"},
                    {"name": "Rydberg Constant", "value": "1.097373 × 10⁷ m⁻¹"},
                    {"name": "Planck's Constant", "value": "6.62607 × 10⁻³⁴ J S"}
                ],
                "footer": {"text": "Use 'c!suggestion' to suggest more constants!"}
            })
            await ctx.send(embed=constants)

        except Exception as e:
            await ctx.send(embed=discord.Embed.from_dict({"title": "Error",
                                                          "description": "Something went wrong..."}))
            with open("data/error_log.txt", "a") as file:
                file.write(f"[Constants]: {e}\n")


def setup(client):
    client.add_cog(Commands(client))
