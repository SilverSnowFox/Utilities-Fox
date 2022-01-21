import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Constants"])
    async def constants(self, ctx):
        # TODO: Add more constants
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
