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

# This comment is to see if github is synced between my devices. (attempt 4)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID {bot.user.id})")
    synced = await bot.tree.sync(guild=GUILD_ID)
    print(f"Synced {len(synced)} slash commands to guild {GUILD_ID.id}")


# Creating Slash Commands (new with Discord.v2)
@bot.tree.command(name="hello", description="Say Hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@bot.tree.command(name="test", description="test slash command", guild=GUILD_ID)
async def testCommand(interaction: discord.Interaction):
    await interaction.response.send_message("This is a test slash command")


@bot.tree.command(name="assign1", description="assigns: bot tester role 1", guild=GUILD_ID)
async def assign1(interaction: discord.Interaction):
    await interaction.guild.fetch_roles()
    role = discord.utils.get(interaction.guild.roles, name=Role_test_1)
    if role:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"{interaction.user.mention} is now assigned to " + Role_test_1 + ".")
    else:
        await interaction.response.send_message("Role doesn't exist")


@bot.tree.command(name="assign2", description="assigns: bot tester role 2", guild=GUILD_ID)
async def assign2(interaction: discord.Interaction):
    await interaction.guild.fetch_roles()
    role = discord.utils.get(interaction.guild.roles, name=Role_test_2)
    if role:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"{interaction.user.mention} is now assigned to " + Role_test_2 + ".")
    else:
        await interaction.response.send_message("Role doesn't exist")


@bot.tree.command(name="remove1", description="removes: bot tester role 1", guild=GUILD_ID)
async def remove1(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name=Role_test_1)
    if role:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"{interaction.user.mention} has had {Role_test_1} removed.")
    else:
        await interaction.response.send_message("Role doesn't exist")


@bot.tree.command(name="remove2", description="removes: bot tester role 2", guild=GUILD_ID)
async def remove2(interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name=Role_test_2)
    if role:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"{interaction.user.mention} has had {Role_test_2} removed.")
    else:
        await interaction.response.send_message("Role doesn't exist")


@bot.tree.command(name="dm", description="Send yourself a DM", guild=GUILD_ID)
async def dm(interaction: discord.Interaction, msg: str):
    await interaction.user.send(f"You said \"{msg}\"")
    await interaction.response.send_message("I sent you a DM!", ephemeral=True)

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
        await ctx.send("You are not a real bean... Try Harder.")


# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
