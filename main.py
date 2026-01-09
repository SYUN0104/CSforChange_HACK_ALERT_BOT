import discord
import os
import asyncio
import json
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# =====================================================================
# 🔒 Cog Whitelist Configuration
# =====================================================================
# Load the list of allowed cogs from the .env file (e.g., "hackathon,music")
# If the variable is missing, it defaults to an empty string.
allowed_cogs_env = os.getenv('ENABLED_COGS', '')

# Convert the comma-separated string into a clean list
# Example: "hackathon, music " -> ['hackathon', 'music']
ALLOWED_COGS = [cog.strip() for cog in allowed_cogs_env.split(',') if cog.strip()]

# Setup Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Set Discord Status (Activity)
    activity = discord.Game(name="CSforChange Helper v1.02-alpha")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print(f'🚀 Login Success: {bot.user.name} ({bot.user.id})')
    print('Version: 1.02-alpha')
    print('System operational. Ready to serve.')
    
    # Print the list of cogs allowed for this session
    print(f'🔒 Allowed Cogs for this session: {ALLOWED_COGS}')

    # Send a startup message to the specific channel
    if CHANNEL_ID:
        try:
            target_channel = bot.get_channel(int(CHANNEL_ID))
            if target_channel:
                await target_channel.send("🚀 **System Online:** CSforChange Helper v1.02-alpha is ready!")
                print(f"✅ Startup message sent to channel: {target_channel.name}")
            else:
                print(f"⚠️ Could not find channel with ID {CHANNEL_ID} for startup message.")
        except Exception as e:
            print(f"❌ Error sending startup message: {e}")


# ---------------------------------------------------
# Commands
# ---------------------------------------------------
@bot.command()
async def ping(ctx):
    """Simple ping command to check bot latency."""
    await ctx.send('pong!')

async def load_extensions():
    """
    Loads cogs from the ./cogs directory.
    Only loads cogs that are listed in the 'ALLOWED_COGS' list.
    """
    if os.path.exists('./cogs'):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                # Remove .py extension to get the cog name
                cog_name = filename[:-3]
                
                # ✅ [Logic] Check if the cog is in the whitelist
                if cog_name in ALLOWED_COGS:
                    try:
                        await bot.load_extension(f'cogs.{cog_name}')
                        print(f'✅ Extension Loaded: {filename}')
                    except Exception as e:
                        print(f'❌ Failed to load extension {filename}: {e}')
                else:
                    # Skip if not in the allowed list
                    print(f'🚫 Skipped Extension: {filename} (Not in ENABLED_COGS)')

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