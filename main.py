import discord
import json
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
            
            # Loop through the data in steps of 10
            for i in range(0, total_items, chunk_size):
                # Slice the list (e.g., 0-10, 10-20, 20-30)
                chunk = data[i:i + chunk_size]
                
                content = ""
                for j, url in enumerate(chunk):
                    # Calculate global index (1-based)
                    index = i + j + 1
                    content += f"{index}. {url}\n"

                # Create an Embed for this specific chunk
                embed = discord.Embed(
                    title=f"📊 Database List ({i + 1} - {i + len(chunk)}) of {total_items}",
                    color=0x3498db
                )
                embed.description = f"```\n{content}\n```"
                
                # Add footer only to the last message
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