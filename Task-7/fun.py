import discord
from discord.ext import commands
import aiohttp
import random

ROASTS = [
    "couldn't find the One Piece even if Roger drew them a map with crayons.",
    "got a lower bounty than Chopper's first poster.",
    "looks like they ate the Disappointment-Disappointment Fruit.",
    "is the kind of rookie Buggy would kick off his crew.",
    "would drown in an ankle-deep puddle on the Grand Line."
]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roast")
    async def roast(self, ctx, member: discord.Member):
        insult = random.choice(ROASTS)
        await ctx.send(f"📢 {member.mention}, {insult}")

    @commands.command(name="logpose")
    async def logpose(self, ctx):
        async with aiohttp.ClientSession() as session:
            category = random.choice(["characters", "fruits"])
            url = f"https://api.api-onepiece.com/v2/{category}/en"
            
            try:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        item = random.choice(data)
                        
                        embed = discord.Embed(title="🧭 Log Pose Grand Line Intel", color=0x00A86B)
                        if category == "characters":
                            name = item.get("name", "Unknown Legend")
                            bounty = item.get("bounty", "Undisclosed")
                            job = item.get("job", "Pirate")
                            embed.add_field(name="Name", value=name, inline=True)
                            embed.add_field(name="Role", value=job, inline=True)
                            embed.add_field(name="World Bounty", value=f"{bounty} ฿" if bounty else "0 ฿", inline=False)
                        else:
                            name = item.get("name", "Mysterious Fruit")
                            desc = item.get("description", "A legendary fruit granting supernatural power.")
                            embed.add_field(name="Devil Fruit", value=name, inline=True)
                            embed.add_field(name="Effect", value=desc[:500], inline=False)

                        return await ctx.send(embed=embed)
            except Exception:
                pass
            
            # Fallback if API fails or times out
            await ctx.send("🧭 *The Log Pose spins wildly...* Intel: **Gomu Gomu no Mi** — Gives the user's body rubber-like properties.")

async def setup(bot):
    await bot.add_cog(Fun(bot))