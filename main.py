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
    activity = discord.Game(name="Hackathon Bot v1.02-alpha")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print(f'🚀 Login Success: {bot.user.name} ({bot.user.id})')
    print('Version: 1.02-alpha')
    print('System operational. Ready to serve.')

    # ✅ [Feature Added] Send "Bot is ready!" message to the target channel
    if CHANNEL_ID:
        try:
            target_channel = bot.get_channel(int(CHANNEL_ID))
            if target_channel:
                await target_channel.send("🚀 **System Online:** Hackathon Bot v1.02-alpha is ready!")
                print(f"✅ Startup message sent to channel {target_channel.name}")
            else:
                print(f"⚠️ Could not find channel with ID {CHANNEL_ID} for startup message.")
        except Exception as e:
            print(f"❌ Error sending startup message: {e}")

# ---------------------------------------------------
# Commands (Ping, DB Check)
# ---------------------------------------------------
@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


@bot.command()
async def db(ctx):
    """Displays all stored hackathon URLs in chunks of 10 items per message."""
    db_path = "./data/database.json"
    
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not data:
                await ctx.send("📭 The database is currently empty.")
                return

            total_items = len(data)
            chunk_size = 10
            
            for i in range(0, total_items, chunk_size):
                chunk = data[i:i + chunk_size]
                content = ""
                for j, url in enumerate(chunk):
                    index = i + j + 1
                    content += f"{index}. {url}\n"

                embed = discord.Embed(
                    title=f"📊 Database List ({i + 1} - {i + len(chunk)}) of {total_items}",
                    color=0x3498db
                )
                embed.description = f"```\n{content}\n```"
                
                if i + chunk_size >= total_items:
                    embed.set_footer(text=f"Total: {total_items} items | Path: {db_path}")

                await ctx.send(embed=embed)
            
            print(f"✅ DB checked: Displayed {total_items} items in chunks.")
            
        except Exception as e:
            await ctx.send(f"❌ Error reading database: {e}")
            print(f"❌ DB Error: {e}")
    else:
        await ctx.send("❓ database.json not found. (No data saved yet)")

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