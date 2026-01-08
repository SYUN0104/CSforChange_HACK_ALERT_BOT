import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Set Discord Status (Activity)
    activity = discord.Game(name="Hackathon Bot v1.01-alpha")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print(f'🚀 Login Success: {bot.user.name}')
    print('Version: 1.01-alpha')
    
    print(f'🚀 Login Success: {bot.user.name} ({bot.user.id})')
    print('System operational. Ready to serve.')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

async def load_extensions():
    if os.path.exists('./cogs'):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Extension Loaded: {filename}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    if TOKEN:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n🛑 Bot shutdown manually.")
    else:
        print("❌ Error: DISCORD_TOKEN not found in .env file.")