import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot configuration (Intents: Set permissions for what information the bot can access in the server)
intents = discord.Intents.default()
intents.message_content = True # Allow the bot to read message content

# Create bot object (Command prefix is set to '!')
bot = commands.Bot(command_prefix='!', intents=intents)

# Event triggered when the bot is online
@bot.event
async def on_ready():
    print(f'Login Success: {bot.user.name} ({bot.user.id})')
    print('Bot is ready!')

# Test command: Outputs 'pong!' when '!ping' is typed
@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

# Run the bot (Raises an error if the token is missing)
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in .env file.")