from discord.ext import commands
import discord
import math


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Polynomial", "poly", "Poly"])
    async def polynomial(self, ctx, a: float = None, b: float = None, c: float = None, d: float = None, *, e=None):
        """Solves a polynomial equation from linear to cubic."""

        def solve_cubic():
            """Solves a cubic equation, including imaginary roots, from the equation:
            'ax**3 + bx**2 + cx + d = 0'
            Slightly modified version taken from https://github.com/shril/CubicEquationSolver/blob/master/CubicEquationSolver.py"""
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

        def solve_quadratic():
            """Solves the quadratic equation, including imaginary roots, using the general quadratic formula, from
            the form: ax**2 + bx + c = 0"""
            dis = (b**2) - (4 * a * c)  # Helper Variable

            if dis > 0:
                R = math.sqrt(dis)  # Helper Variable

                x1 = (-b + R) / (2 * a)
                x2 = (-b - R) / (2 * a)
            elif dis == 0:
                x1, x2 = -b / (2 * a)
            else:
                R = - b / (2 * a)  # Helper Variable
                S = math.sqrt(abs(dis))*1.0j  # Helper Variable

                x1 = R + S
                x2 = R - S

            return [x1, x2]

        def solve_linear():
            """Solves a linear equation in the form: ax + b = 0."""
            return -b/a

        embed = discord.Embed(color=discord.Colour.gold())

        if e is None:
            # Limit to cubic polynomial
            if d is not None:
                # Cubic Equation
                roots = solve_cubic()

                embed.title = "Cubic Calculation"
                embed.add_field(name="Input", value=f"```{a}x³ + {b}x² + {c}x + {d} = 0```", inline=False)
                embed.add_field(name="Roots", value=f"```{roots[0]} \n{roots[1]} \n{roots[2]}```")

                await ctx.send(embed=embed)
                return

            elif c is not None:
                # Quadratic Equation
                roots = solve_quadratic()

                embed.title = "Quadratic Calculation"
                embed.add_field(name="Input", value=f"```{a}x² + {b}x + {c} = 0```", inline=False)
                embed.add_field(name="Roots", value=f"```{roots[0]} \n{roots[1]}```")

                await ctx.send(embed=embed)
                return

            elif b is not None:
                # Linear
                root = solve_linear()

                embed.title = "Linear Calculation"
                embed.add_field(name="Input", value=f"```{a}x + {b} = 0```", inline=False)
                embed.add_field(name="Roots", value=f"```{root}```")

                await ctx.send(embed=embed)
                return

            else:
                # Error, no input
                error = "There was input. Please input an equation in the form ax**n + bx**(n-1) + cx**(n-2) + d = 0"
        else:
            # Error, larger than cubic
            error = "I'm currently unable to solve a polynomial above a cubic."

        await ctx.send(embed=discord.Embed.from_dict({
            "title": "Error",
            "description": error
        }))


def setup(client):
    client.add_cog(Commands(client))
