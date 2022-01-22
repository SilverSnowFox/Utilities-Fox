import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Constants"])
    async def constants(self, ctx):
        """Displays a list of the more common constants"""
        try:
            constants = discord.Embed.from_dict({
                "title": "Common Constants",
                "color": 0xf1c40f,
                "fields": [
                    {"name": "Atomic Mass Constant", "value": "1.660 538 × 10⁻²⁷ kg"},
                    {"name": "Avogadro's Number", "value": "6.022 14 × 10²³ mol⁻¹"},
                    {"name": "Boltzmann Constant", "value": "1.38065 × 10⁻²³ J K⁻¹"},
                    {"name": "Coulomb's Constant", "value": "8.987551 × 10⁹ N m² C⁻²"},
                    {"name": "Electron Charge", "value": "1.602176 × 10⁻¹⁹ C"},
                    {"name": "Electron Rest Mass", "value": "9.109 × 10⁻³¹ kg"},
                    {"name": "Faraday Constant", "value": "96 485.33 C mol⁻¹"},
                    {"name": "Light Speed (Vacuum)", "value": "299 792 558 m s⁻¹"},
                    {"name": "Molar Gas Constant", "value": "8.3144 J mol⁻¹ K⁻¹, 0.082057 L atm K⁻¹ mol⁻¹"},
                    {"name": "Neutron Rest mass", "value": "1.6749273 × 10⁻²⁷ kg"},
                    {"name": "Permeability of Free Space", "value": "4π× 10⁻⁷ H m⁻¹"},
                    {"name": "Permittivity of Free Space", "value": "8.854 × 10⁻¹² F m⁻¹"},
                    {"name": "Planck's Constant", "value": "6.62607 × 10⁻³⁴ J S"},
                    {"name": "Proton Rest Mass", "value": "1.6726 × 10⁻²⁷ kg"},
                    {"name": "Rydberg Constant", "value": "1.097373 × 10⁷ m⁻¹"},
                    {"name": "Standard gravity", "value": "9.80665 m s⁻²"},
                    {"name": "Water Self-ionization Constant", "value": "1.0 × 10⁻¹⁴"}
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
