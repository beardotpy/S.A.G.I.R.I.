import discord
from discord.ext import commands
import sqlite3
from SAGIRI import DB, cursor, register_if_new

class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx, *args):
        register_if_new(ctx.author)

        cursor.execute(f"SELECT role_id FROM users WHERE id = {ctx.author.id}")
        role_id = cursor.fetchone()[0]
        name_arg = ""
        color_arg = args[0]
        if color_arg[0] == "#":
            color_arg = color_arg[1:]
        if len(color_arg) == 6:
            try:
                color = int(color_arg, 16)
            except:
                color = None
                name_arg = " ".join(args)
            else:
                if len(args) == 1:
                    name_arg = None
                else:
                    name_arg = " ".join(args[1:])
        else:
            color = None
            name_arg = " ".join(args)

        if role_id == None:
            if color == None:
                color = 0x0
            if name_arg == None:
                await ctx.send("Please specify a name for your role")
            role = await ctx.guild.create_role(name=name_arg, color=color)
            cursor.execute("UPDATE users SET role_id = ? WHERE id = ?", (role.id, ctx.author.id))
            DB.commit()
            await ctx.author.add_roles(role)
            await ctx.send(f"I made you your role, Master! It has the name \"**{role.name}**\" and the color **#{hex(role.color.value)[2:]}**")
            return
        
        role = ctx.guild.get_role(role_id)
        
        if color == None:
            color = role.color
        if name_arg == None:
            name_arg = role.name
        
        await role.edit(name=name_arg, color=color)
        await ctx.send(f"I edited your role, Master! Now it has the name \"**{role.name}**\" and the color **#{hex(role.color.value)[2:]}**")

        

async def setup(bot):
    await bot.add_cog(Color(bot))
     