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
    """Command to check the status of database.json on Railway."""
    db_path = "./data/database.json"
    
    # Check if the file exists in the current environment
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            count = len(data)
            # Show the last 3 URLs for verification
            last_three = "\n".join(data[-3:]) if count > 0 else "None"
            
            embed = discord.Embed(title="📊 Database Status", color=0x3498db)
            embed.add_field(name="Stored Count", value=f"{count} / 30", inline=False)
            embed.add_field(name="Recent URLs", value=f"```{last_three}```", inline=False)
            embed.set_footer(text="Verification for Alpha v1.01")
            
            await ctx.send(embed=embed)
            print(f"✅ DB status reported: {count} items.")
            
        except Exception as e:
            await ctx.send(f"❌ Error reading database: {e}")
    else:
        await ctx.send("❓ database.json not found. The bot might not have saved any data yet.")

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