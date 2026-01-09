import discord
import os
import asyncio
import json
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID') # Load Channel ID here too

# Setup Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Set Discord Status (Activity)
    activity = discord.Game(name="CSforChangeHelper v1.02-alpha")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print(f'🚀 Login Success: {bot.user.name} ({bot.user.id})')
    print('Version: 1.02-alpha')
    print('System operational. Ready to serve.')

    # ✅ [Feature Added] Send "Bot is ready!" message to the target channel
    if CHANNEL_ID:
        try:
            target_channel = bot.get_channel(int(CHANNEL_ID))
            if target_channel:
                await target_channel.send("🚀 **System Online:** CSforChangeHelper v1.02-alpha is ready!")
                print(f"✅ Startup message sent to channel {target_channel.name}")
            else:
                print(f"⚠️ Could not find channel with ID {CHANNEL_ID} for startup message.")
        except Exception as e:
            print(f"❌ Error sending startup message: {e}")

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