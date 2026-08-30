import discord
from discord.ext import commands
import datetime
import random
import database as db

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # !bounty: Check balance
    @commands.command(name="bounty")
    async def bounty(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user = db.get_user(member.id, member.name)
        embed = discord.Embed(
            title=f"🏴‍☠️ Bounty Ledger: {member.display_name}",
            description=f"Current Bounty: **{user['balance']:,} ฿ (Berries)**",
            color=0xD4AF37
        )
        await ctx.send(embed=embed)

    # !setsail: 24h Daily reward
    @commands.command(name="setsail")
    async def setsail(self, ctx):
        user = db.get_user(ctx.author.id, ctx.author.name)
        now = datetime.datetime.utcnow()
        
        if user['last_daily']:
            last = datetime.datetime.fromisoformat(user['last_daily'])
            if now - last < datetime.timedelta(hours=24):
                remaining = datetime.timedelta(hours=24) - (now - last)
                hours, rem = divmod(int(remaining.total_seconds()), 3600)
                minutes, _ = divmod(rem, 60)
                return await ctx.send(f"⏳ Your crew is resting. Set sail again in **{hours}h {minutes}m**.")

        loot = random.randint(200, 600)
        db.update_balance(ctx.author.id, loot)
        db.set_timestamp(ctx.author.id, "last_daily")
        await ctx.send(f"⚓ You raided an imperial merchant convoy at dawn and secured **{loot:,} ฿**!")

    # !trade: Peer-to-peer transaction
    @commands.command(name="trade")
    async def trade(self, ctx, target: discord.Member, amount: int):
        if target.id == ctx.author.id or target.bot:
            return await ctx.send("❌ You cannot trade with yourself or the marine bots.")
        if amount <= 0:
            return await ctx.send("❌ Amount must be greater than 0.")

        sender = db.get_user(ctx.author.id, ctx.author.name)
        db.get_user(target.id, target.name)

        if sender['balance'] < amount:
            return await ctx.send("❌ You don't have enough Berries in your chest.")

        db.update_balance(ctx.author.id, -amount)
        db.update_balance(target.id, amount)
        await ctx.send(f"🤝 Handshake in the shadows: {ctx.author.mention} transferred **{amount:,} ฿** to {target.mention}.")

    # !raid: Attempt to rob another user
    @commands.command(name="raid")
    async def raid(self, ctx, target: discord.Member):
        if target.id == ctx.author.id or target.bot:
            return await ctx.send("❌ Pick a real rival pirate to raid.")

        attacker = db.get_user(ctx.author.id, ctx.author.name)
        victim = db.get_user(target.id, target.name)
        now = datetime.datetime.utcnow()

        if attacker['last_rob']:
            last = datetime.datetime.fromisoformat(attacker['last_rob'])
            if now - last < datetime.timedelta(hours=2):
                remaining = datetime.timedelta(hours=2) - (now - last)
                minutes = int(remaining.total_seconds() // 60)
                return await ctx.send(f"⏳ The docks are heavily guarded! Lay low for **{minutes}m**.")

        if victim['balance'] < 100:
            return await ctx.send("❌ That pirate's stash is too poor to be worth raiding.")

        db.set_timestamp(ctx.author.id, "last_rob")
        success = random.random() < 0.45  # 45% success chance

        if success:
            stolen = random.randint(50, int(victim['balance'] * 0.35))
            db.update_balance(ctx.author.id, stolen)
            db.update_balance(target.id, -stolen)
            await ctx.send(f"⚔️ **Raid Successful!** You slipped aboard {target.mention}'s ship and made off with **{stolen:,} ฿**!")
        else:
            penalty = random.randint(50, 150)
            db.update_balance(ctx.author.id, -penalty)
            await ctx.send(f"💥 **Caught red-handed!** {target.mention}'s lookouts spotted you. You dropped **{penalty:,} ฿** while escaping.")

    # !worstgeneration: Leaderboard
    @commands.command(name="worstgeneration")
    async def worstgeneration(self, ctx):
        top_pirates = db.get_top_pirates(5)
        embed = discord.Embed(title="📜 The Worst Generation — High Bounties", color=0x8B0000)
        
        for idx, row in enumerate(top_pirates, 1):
            embed.add_field(name=f"#{idx} {row['username']}", value=f"**{row['balance']:,} ฿**", inline=False)
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))