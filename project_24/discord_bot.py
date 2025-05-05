import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Server ko alive rakhne ke liye (agar Replit ya similar platform pe ho)
from keep_alive import keep_alive

# Load token from .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Logging setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Keep alive before running
keep_alive()

# Secret role name
secret_role = "Mahnoor"

# Bot events and commands
@bot.event
async def on_ready():
    print(f"We are ready to go! {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    # 🔒 Filters Out Bad Language
    bad_words = [
        "shit", "damn", "bastard", "fuck", "fucking", "asshole", "dick", "piss",
        "crap", "bitch", "slut", "whore", "cunt", "nigger", "retard", "fag", "idiot"
    ]

    if any(bad_word in msg for bad_word in bad_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please refrain from using that language.")
        return

    # Keyword-based responses
    if msg == "hello bot":
        await message.channel.send(f"Hello {message.author.mention}! How can I help you today?")
    elif msg == "how are you":
        await message.channel.send("I'm just a bot, but I'm doing great! 😄")
    elif msg.startswith("say "):
        response = message.content[4:]
        await message.channel.send(response)

    # Respond to greetings
    elif any(greeting in msg for greeting in ["hi", "hello", "hey"]):
        await message.channel.send(f"Hello {message.author.mention}! How can I assist you today?")
    
    # Respond to goodbyes
    elif any(goodbye in msg for goodbye in ["bye", "goodbye", "see you"]):
        await message.channel.send(f"Goodbye {message.author.mention}! Have a great day! 👋")

    # Respond to compliments
    elif any(compliment in msg for compliment in ["good bot", "nice bot", "smart bot"]):
        await message.channel.send(f"Thank you {message.author.mention}! You're awesome too! 😊")

    # Respond to any command
    elif msg.startswith("!"):
        await message.channel.send(f"Command received: {msg}")

    # Respond to any question
    elif msg.endswith("?"):
        await message.channel.send(f"That's a great question, {message.author.mention}! 🤔 Let me think about it...")

    await bot.process_commands(message)

# Commands
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"Role '{secret_role}' has been assigned to you, {ctx.author.mention}!")
    else:
        await ctx.send(f"Role '{secret_role}' not found in this server.")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"Role '{secret_role}' has been removed from you, {ctx.author.mention}!")
    else:
        await ctx.send(f"You do not have the role '{secret_role}', {ctx.author.mention}.")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said '{msg}'")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send(f"Welcome to the secret channel, {ctx.author.mention}!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("🚫 You do not have permission to use this command.")

# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
