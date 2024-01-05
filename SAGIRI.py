from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import random
import sqlite3
import asyncio
import subprocess

DB = sqlite3.connect("db.sqlite3")
cursor = DB.cursor()

bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    with os.scandir("cogs") as cogs_dir:
        for cog_file in cogs_dir:
            cog_name = os.path.splitext(cog_file.name)[0]
            if cog_name == "__pycache__":
                continue
            await bot.load_extension(f"cogs.{cog_name}")
            
    async with bot:
        await bot.start(BOT_TOKEN)

_cd = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.member)
def get_ratelimit(message: discord.Message):
        """Returns the ratelimit left"""
        bucket = _cd.get_bucket(message)
        return bucket.update_rate_limit()

def register_if_new(member):
    cursor.execute(f"SELECT xp FROM users WHERE id = {member.id}")
    result = cursor.fetchone()

    if result == None:
        cursor.execute(f"INSERT INTO users (name, id) VALUES (?, ?)", (member.name, member.id))
        DB.commit()
    
@bot.event
async def on_ready():
    print(f"I'm ready for you Onii-chan!")

@bot.event
async def on_member_join(member):
    holoseggs = bot.get_guild(1147155469656399872)
    degenizen = holoseggs.get_role(1148029420263714846)
    degeneral = holoseggs.get_channel(1147155471275393026)
    
    await member.add_roles(degenizen)
    await degeneral.send(f"{member.mention} Welcome! Please enjoy your stay with us :)")

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    await bot.process_commands(message)

    register_if_new(message.author)

    if message.content.lower() in ["thanks sagiri", "thanks, sagiri"]:
        await message.reply("You're welcome, Onii-chan!")
    
    if message.content.lower() in ["gm sagiri", "good morning sagiri", "gm, sagiri", "good morning, sagiri"]:
        await message.reply("Morning, Onii-chan!")
        await message.send("You're going to have a great day today. I can feel it!")

    if message.content.lower() in ["gn sagiri", "good night sagiri", "gn, sagiri", "good night, sagiri"]:
        replies = ["Sleep well Onii-chan!", "Good night, Onii-chan!"]
        await message.reply(random.choice(replies))
    if message.content.lower() == "i love you sagiri":
        await message.reply("Baka!!! Did you have to say it like that?? Umm...I guess I love you too, Onii-chan >.<")



    if message.channel.id in [1149914562330632302, 1148726052433187057]:
        return

    ratelimit = get_ratelimit(message)
    if ratelimit != None:
        return
    
    cursor.execute(f"SELECT xp FROM users WHERE id = {message.author.id}")
    result = cursor.fetchone()

    xp_amount = random.randint(10,15)
    cursor.execute("UPDATE users SET xp = ? WHERE id = ?", (result[0] + xp_amount, message.author.id))
    DB.commit()


@bot.command(aliases=["store"])
async def store_cunny(ctx):
    if ctx.channel.id != 1148358387864702998:
        await ctx.send("not the cunny channel baka")
        return

    async with ctx.typing():
        cunny_channel = bot.get_channel(1186910775911141406)
        for attachment in ctx.message.attachments:
            file = await attachment.to_file()
            message = await cunny_channel.send(file = file)
            cursor.execute(f"INSERT INTO cunny (message_id) VALUES ({message.id})")
            id = cursor.lastrowid
            DB.commit()
            await ctx.send(f"{ctx.author} has stored a little sexy cunny with id `{id}`")

    await ctx.message.delete()
    
@bot.command(aliases=["get"])
async def get_cunny(ctx, id:int):
    cursor.execute(f"SELECT message_id FROM cunny WHERE id = {id}")
    result = cursor.fetchone()
    
    if result == None:
        await ctx.send("doesn't exist retard")
        return
    
    async with ctx.typing():
        cunny_channel = bot.get_channel(1186910775911141406)
        cunny_channel_message = await cunny_channel.fetch_message(result[0])
        cunny_file = await cunny_channel_message.attachments[0].to_file()
        cunny_message = await ctx.author.send(file=cunny_file)
        await ctx.reply(cunny_message.jump_url)


@bot.command()
async def test(ctx):
    pass


@bot.command()
async def cheermeup(ctx):
    await ctx.reply("Onii-chan, I believe in you!!!")

@bot.command()
async def cheerup(ctx, member:discord.Member):
    await ctx.send(f"{member.mention} Hey umm...I don't really know you, but my Onii-chan asked me to cheer you up. Well, if you're a friend of bear_ then you must be really hot and sexy...and strong um what am I saying. Ummm just feel better, ok? >.<")

@bot.command()
async def convert(ctx, temp:int):
    await ctx.reply(temp*9/5+32)

@bot.command()
async def quote(ctx):
    pass
    quote_message = ctx.channel.get_message(ctx.message.reference.message_id)
    author = quote_message.author.id
    content = quote_message.content
    date = quote_message.created_at
    
    cursor.execute("INSERT INTO quotes VALUES (?, ?, ?)", (author, content, date))
    DB.commit()
    
    await ctx.send("Added quote")
    
@bot.command()
async def get_quote(ctx, member:discord.Member):
    pass
    

@bot.command(aliases=["av", "pfp"])
async def avatar(ctx):
    pass

@bot.command()
@commands.is_owner()
async def echo(ctx, *, msg):
    await ctx.send(msg)

@bot.command()
@commands.is_owner()
async def say(ctx, *, msg):
   await ctx.send(msg)
   await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send("Hey...You're not my Onii-chan!! >.< This command is only for him >:(")
        return
    if ctx.author.id in [bot.owner_id, 1075931747587473510]:
        await ctx.send(f"Baka!!! <@!623396579960946690> you coded me wrong!!! >\_> Maybe this will help you? `{error}`")
        return
    await ctx.send(f"I'm sowwy...<@!623396579960946690> coded me wrong!!! Please forgive my Onii-chan >.<\n`{error}`")

if __name__ == "__main__":
    asyncio.run(main())
