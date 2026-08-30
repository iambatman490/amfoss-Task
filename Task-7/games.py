import discord
from discord.ext import commands
import random
import database as db

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="duel")
    async def duel(self, ctx, choice: str = None):
        valid = {"rock": "🪨 Cutlass Clash", "paper": "📜 Tactical Maneuver", "scissors": "✂️ Flintlock Quickdraw"}
        if not choice or choice.lower() not in valid:
            return await ctx.send("⚔️ Declare your move: `!duel rock`, `!duel paper`, or `!duel scissors`")

        player_move = choice.lower()
        bot_move = random.choice(list(valid.keys()))
        user = db.get_user(ctx.author.id, ctx.author.name)

        if user['balance'] < 50:
            return await ctx.send("❌ You need at least 50 ฿ to step into the duel ring.")

        wager = 50
        result_text = f"You threw **{player_move.title()}** | The Broker countered with **{bot_move.title()}**\n\n"

        if player_move == bot_move:
            result_text += "⚔️ Steel meets steel! It's a draw—no Berries lost."
        elif (player_move == "rock" and bot_move == "scissors") or \
             (player_move == "paper" and bot_move == "rock") or \
             (player_move == "scissors" and bot_move == "paper"):
            db.update_balance(ctx.author.id, wager)
            result_text += f"🏆 **Victory!** You disarmed the broker and claimed **+{wager} ฿**!"
        else:
            db.update_balance(ctx.author.id, -wager)
            result_text += f"💀 **Defeat!** The broker knocked you flat. You lost **-{wager} ฿**."

        await ctx.send(result_text)

async def setup(bot):
    await bot.add_cog(Games(bot))