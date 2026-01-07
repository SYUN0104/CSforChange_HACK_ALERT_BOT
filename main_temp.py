import discord
import os
import requests
import re
import time
from discord.ext import commands
from dotenv import load_dotenv

# 1. Environment Variable Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2. Bot Intent and Object Creation
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ==========================================
# [Added Functions] Logic imported from api_test.py
# ==========================================

def clean_html_tags(text):
    """Function to remove HTML tags"""
    if not text:
        return "0"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def get_hackathons_data(num_pages=1):
    """Function to fetch hackathon information via Devpost API"""
    base_url = "https://devpost.com/api/hackathons"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_hackathons = []
    
    # Enhanced error handling to prevent the bot from crashing
    try:
        for page in range(1, num_pages + 1):
            params = {
                'open_to[]': 'public',
                'order_by': 'recently-added',
                'page': page
            }
            
            response = requests.get(base_url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"API Request Failed: {response.status_code}")
                continue
                
            data = response.json()
            hackathon_list = data.get('hackathons', [])
            
            if not hackathon_list:
                break

            for item in hackathon_list:
                try:
                    # Data extraction logic (same as api_test.py)
                    url = item.get('url', 'N/A')
                    thumbnail = item.get('thumbnail_url', '')
                    if thumbnail and thumbnail.startswith("//"):
                        thumbnail = "https:" + thumbnail
                    
                    title = item.get('title', 'No Title')
                    status = item.get('time_left_to_submission', 'N/A')
                    
                    location_obj = item.get('displayed_location', {})
                    location = location_obj.get('location', 'Online') if location_obj else 'Online'
                    
                    # Prize processing
                    raw_prize_amount = item.get('prize_amount', '0')
                    prize_amount = clean_html_tags(raw_prize_amount)
                    
                    counts_dict = item.get('prizes_counts', {})
                    if not counts_dict: counts_dict = {}
                    prize_cash = int(counts_dict.get('cash', 0))
                    prize_other = int(counts_dict.get('other', 0))
                    
                    host = item.get('organization_name', 'Unknown')
                    period = item.get('submission_period_dates', 'N/A')
                    
                    themes_list = item.get('themes', [])
                    themes = [t['name'] for t in themes_list if 'name' in t]
                    
                    all_hackathons.append({
                        'title': title,
                        'url': url,
                        'thumbnail': thumbnail,
                        'status': status,
                        'location': location,
                        'prize_amount': prize_amount,
                        'prize_cash': prize_cash,
                        'prize_other': prize_other,
                        'host': host,
                        'period': period,
                        'themes': themes
                    })
                except Exception as e:
                    print(f"Parsing Error: {e}")
                    continue
                    
    except Exception as e:
        print(f"Critical Error: {e}")
        return []

    return all_hackathons

# ==========================================
# [Bot Events and Commands]
# ==========================================

@bot.event
async def on_ready():
    print(f'Log-in Success: {bot.user.name} ({bot.user.id})')
    print('Bot is Ready!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

# New Command: !hack
@bot.command()
async def hack(ctx):
    # 1. Notify the user
    await ctx.send("🔄 Fetching data...")
    
    # 2. Get data (Page 1 only)
    hackathons = get_hackathons_data(num_pages=1)
    
    if not hackathons:
        await ctx.send("❌ Failed to retrieve hackathon information.")
        return

    # 3. Send as Discord message (Using Embeds)
    # We only send the top 5 to avoid spamming the channel.
    count = 0
    for item in hackathons:
        if count >= 5: 
            break
            
        # Create Embed (Card Design)
        embed = discord.Embed(
            title=item['title'],
            url=item['url'],
            description=f"⏱️ **{item['status']}**",
            color=0x00ff00 # Green
        )
        
        # Set Thumbnail image
        if item['thumbnail']:
            embed.set_thumbnail(url=item['thumbnail'])
        
        # Add Fields
        embed.add_field(name="📍 Location", value=item['location'], inline=True)
        embed.add_field(name="🏢 Host", value=item['host'], inline=True)
        embed.add_field(name="📅 Period", value=item['period'], inline=True)
        
        # Prize Info (Using line breaks)
        prize_info = f"**{item['prize_amount']}**\n(Cash: {item['prize_cash']}, Other: {item['prize_other']})"
        embed.add_field(name="💰 Prize", value=prize_info, inline=False)
        
        # Themes (Convert list to string)
        themes_str = ", ".join(item['themes']) if item['themes'] else "N/A"
        embed.add_field(name="🏷️ Themes", value=themes_str, inline=False)
        
        # Send Message
        await ctx.send(embed=embed)
        count += 1
    
    await ctx.send("✅ Successfully Posted")

# Run Bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR : TOKEN READ ERROR")