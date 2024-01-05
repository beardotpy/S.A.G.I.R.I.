import discord
from discord.ext import commands
from SAGIRI import DB, cursor, register_if_new

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["level", "levels", "profile"])
    async def rank(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author

        register_if_new(ctx.author)

        cursor.execute(f"SELECT xp FROM users WHERE id = {member.id}")
        xp = cursor.fetchone()

        embed = discord.Embed(title = f"{member}'s Rank", color = member.color)
        embed.set_thumbnail(url = member.display_avatar.url)
        embed.add_field(name="Total XP", value = xp[0])
        await ctx.send(embed=embed)


    @commands.command(aliases=["lb, leaderboards"])
    async def top(self, ctx):
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        result.sort(key=lambda elem: elem[2], reverse=True)
        
        embed = discord.Embed(title = "Leveling Leaderboard")
        leaderboard_str = ""
        i = 1
        for user in result:
            leaderboard_str += f"`{i}.` **{user[0]}** — {user[2]} xp\n"
            i += 1
        embed.add_field(name = "Page One", value = leaderboard_str)
        
        await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Leveling(bot))