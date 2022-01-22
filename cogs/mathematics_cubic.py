from discord.ext import commands
import discord
import math


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Cubic"])
    async def cubic(self, ctx, a: int = None, b: int = None, c: int = None, d: int = None):
        """Solves a cubic equation of the form ax³ + bx² + cx + d = 0
            Slightly modified version taken from https://github.com/shril/CubicEquationSolver/blob/master/CubicEquationSolver.py"""
        # TODO: Add to Help Command

        def solve():
            f = ((3.0 * c / a) - ((b ** 2.0) / (a ** 2.0))) / 3.0
            g = (((2.0 * (b ** 3.0)) / (a ** 3.0)) - ((9.0 * b * c) / (a ** 2.0)) + (27.0 * d / a)) / 27.0
            h = (g ** 2.0) / 4.0 + (f ** 3.0) / 27.0

            if f == 0 and g == 0 and h == 0:  # All 3 Roots are Real and Equal
                if (d / a) >= 0:
                    x = (d / (1.0 * a)) ** (1 / 3.0) * -1
                else:
                    x = (-d / (1.0 * a)) ** (1 / 3.0)
                return [x, x, x]  # Returning Equal Roots as numpy array.

            elif h <= 0:  # All 3 roots are Real

                i = math.sqrt(((g ** 2.0) / 4.0) - h)  # Helper Temporary Variable
                j = i ** (1 / 3.0)  # Helper Temporary Variable
                k = math.acos(-(g / (2 * i)))  # Helper Temporary Variable
                L = j * -1  # Helper Temporary Variable
                M = math.cos(k / 3.0)  # Helper Temporary Variable
                N = math.sqrt(3) * math.sin(k / 3.0)  # Helper Temporary Variable
                P = (b / (3.0 * a)) * -1  # Helper Temporary Variable

                x1 = 2 * j * math.cos(k / 3.0) - (b / (3.0 * a))
                x2 = L * (M + N) + P
                x3 = L * (M - N) + P

                return [x1, x2, x3]  # Returning Real Roots as numpy array.

            elif h > 0:  # One Real Root and two Complex Roots
                R = -(g / 2.0) + math.sqrt(h)  # Helper Temporary Variable
                if R >= 0:
                    S = R ** (1 / 3.0)  # Helper Temporary Variable
                else:
                    S = (-R) ** (1 / 3.0) * -1  # Helper Temporary Variable
                T = -(g / 2.0) - math.sqrt(h)
                if T >= 0:
                    U = (T ** (1 / 3.0))  # Helper Temporary Variable
                else:
                    U = ((-T) ** (1 / 3.0)) * -1  # Helper Temporary Variable

                x1 = (S + U) - (b / (3.0 * a))
                x2 = -(S + U) / 2 - (b / (3.0 * a)) + (S - U) * math.sqrt(3) * 0.5j
                x3 = -(S + U) / 2 - (b / (3.0 * a)) - (S - U) * math.sqrt(3) * 0.5j

                return [x1, x2, x3]  # Returning One Real Root and two Complex Roots as numpy array.

        descrip = None
        if a == 0: descrip = "This is not a cubic equation."
        elif d is None: descrip = "Invalid input. Please use the command in the form:\n```c!cubic <a> <b> <c> <d>```\nFrom ax³ + bx² + cx + d = 0"

        if descrip is not None:
            await ctx.send(embed=discord.Embed.from_dict({
                "title": "Error",
                "description": descrip
            }))

        roots = solve()

        # Creates embed
        embed = discord.Embed(color=discord.Colour.gold())
        embed.title = "Cubic Calculation"
        embed.add_field(name="Input", value=f"```{a}x³ + {b}x² + {c}x + {d} = 0```", inline=False)
        embed.add_field(name="Roots", value=f"```{roots[0]} \n{roots[1]} \n{roots[2]}```")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
