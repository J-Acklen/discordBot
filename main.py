import logging
import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

SECRET_ROLE = "Bot Tester Group 1"
GUILD_ID = discord.Object(id=1267513255849492480)

# List of Blacklisted words
blacklisted_words = [
    # Profanity
    "ass", "shit", "fuck", "damn", "bitch", "asshole", "bastard", "dick", "piss", "cunt", "cock",

    # Slurs (Racial, Ethnic, Gender-based — ⚠️ includes offensive terms for moderation only)
    "nigger", "nigga", "nig", "fag", "faggot", "tranny", "kike", "chink", "gook", "spic", "dyke",

    # Sexual/Explicit content
    "porn", "cum", "ejaculate", "rape", "suck", "blowjob", "handjob", "dildo", "anal", "vagina", "penis",

    # Bypass attempts / Leetspeak
    "sh1t", "f*ck", "c0ck", "n1gga", "n1gger", "d1ck", "p0rn", "b1tch", "a$$", "f u c k",

    # Hate symbols or alt spellings
    "heil", "1488", "kkk", "nazi", "hitler",
]  # Add more as needed
# Precompile a regex pattern with word boundaries for performance
blacklist_pattern = re.compile(rf"\b({'|'.join(re.escape(word) for word in blacklisted_words)})\b", re.IGNORECASE)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID {bot.user.id})")
    synced = await bot.tree.sync(guild=GUILD_ID)
    print(f"Synced {len(synced)} slash commands to guild {GUILD_ID.id}")


@bot.tree.command(name="hello", description="Say Hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


# … rest of your prefix commands …

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Use the regex pattern to check for blacklisted words
    if blacklist_pattern.search(message.content):
        await message.delete()
        await message.channel.send(f"{message.author.mention} - don't use that word!")
        return

    await bot.process_commands(message)


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {SECRET_ROLE}.")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had {SECRET_ROLE} removed.")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")


@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


@bot.command()
@commands.has_role(SECRET_ROLE)
async def secret(ctx):
    await ctx.send("Welcome to the club!")


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the permission to do that!")


# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
