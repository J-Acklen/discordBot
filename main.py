import logging
import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bad_words import blacklisted_words

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

Role_test_1 = "Bot Tester Group 1"
Role_test_2 = "Bot Tester Group 2"
Role_real_beans = "Beans"
GUILD_ID = discord.Object(id=os.getenv('GUILD_ID'))

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

@bot.tree.command(name="test", description="test slash command", guild=GUILD_ID)
async def testCommand(interaction: discord.Interaction):
    await interaction.response.send_message("This is a test slash command")

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
async def assign1(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role_test_1)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {Role_test_1}.")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def assign2(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role_test_2)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {Role_test_2}.")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def remove1(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role_test_1)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had {Role_test_1} removed.")
    else:
        await ctx.send("Role doesn't exist")


@bot.command()
async def remove2(ctx):
    role = discord.utils.get(ctx.guild.roles, name=Role_test_2)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had {Role_test_2} removed.")
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


# Role-Specific bot commands

# basic Role_test_1 test
@bot.command()
@commands.has_role(Role_test_1)
async def secret1(ctx):
    await ctx.send("You have type 1 diabetes!")


# basic role_test_2 test
@bot.command()
@commands.has_role(Role_test_2)
async def secret2(ctx):
    await ctx.send("You have type 2 diabetes!")


@bot.command()
@commands.has_role(Role_real_beans)
async def secret3(ctx):
    await ctx.send("What up blud?")


@secret1.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the permission to do that!")


@secret2.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the permission to do that!")


@secret3.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the permission to do that!")


# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
