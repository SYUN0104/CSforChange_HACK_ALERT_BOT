import discord
from discord.ext import commands, tasks
import requests
import json
import os
import re
import traceback
import asyncio

class Hackathon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "./data/database.json"
        self.sent_urls = self.load_data()
        self.target_channel_id = int(os.getenv('CHANNEL_ID', 0))
        
        # Start the loop immediately
        self.check_new_hackathons.start()

    def load_data(self):
        """Loads the list of sent hackathon URLs from the JSON file."""
        if not os.path.exists("./data"):
            os.makedirs("./data")
        
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"✅ Data loaded successfully. {len(data)} items found.")
                    return data
            except Exception as e:
                print(f"❌ Failed to load data: {e}")
                return []
        return []

    def save_data(self):
        """Saves the current list of URLs to the JSON file with a limit of 30 items."""
        if len(self.sent_urls) > 30:
            self.sent_urls = self.sent_urls[-30:]
            print("⚠️ Data limit reached (Max 30). Oldest entries removed.")
        
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.sent_urls, f, indent=4)
            print("💾 Database updated successfully.")
        except Exception as e:
            print(f"❌ Failed to save data: {e}")

    def clean_html_tags(self, text):
        """Removes HTML tags and cleans up currency strings."""
        if not text: return "N/A"
        # Remove HTML tags like <span>
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', text)
        # Decode unicode characters if necessary (though usually handled by json)
        return text.strip()

    def get_hackathons_from_api(self):
        """Fetches and parses hackathon data based on the provided JSON structure."""
        url = "https://devpost.com/api/hackathons"
        
        params = {
            'open_to[]': 'public',
            'order_by': 'recently-added',
            'page': 1
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # The API returns a dictionary with a 'hackathons' list
                raw_hackathons = data.get('hackathons', [])
                
                formatted_data = []
                for item in raw_hackathons:
                    # 1. Thumbnail URL fix (add https:)
                    thumbnail_url = item.get('thumbnail_url', '')
                    if thumbnail_url and thumbnail_url.startswith("//"):
                        thumbnail_url = "https:" + thumbnail_url
                    
                    # 2. Extract nested location
                    location_info = item.get('displayed_location', {})
                    location = location_info.get('location', 'Online')
                    
                    # 3. Extract Themes (List of Dicts -> List of Names)
                    raw_themes = item.get('themes', [])
                    theme_names = [t['name'] for t in raw_themes]
                    
                    # 4. Extract Prize Counts
                    prizes_counts = item.get('prizes_counts', {})
                    cash_count = prizes_counts.get('cash', 0)
                    other_count = prizes_counts.get('other', 0)
                    
                    formatted_item = {
                        'title': item.get('title', 'No Title'),
                        'url': item.get('url'),
                        'status': item.get('time_left_to_submission', 'N/A'),
                        'thumbnail': thumbnail_url,
                        'location': location,
                        'host': item.get('organization_name', 'Devpost'),
                        'period': item.get('submission_period_dates', 'N/A'),
                        'prize_amount': self.clean_html_tags(item.get('prize_amount', '0')),
                        'prize_cash': f"{cash_count} prizes",
                        'prize_other': f"{other_count} prizes",
                        'themes': theme_names
                    }
                    formatted_data.append(formatted_item)
                    
                return formatted_data
            else:
                print(f"⚠️ API Request failed: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ API Connection Error: {e}")
            return []

    def create_embed(self, item):
        """Creates the specific Discord Embed design."""
        embed = discord.Embed(
            title=item['title'],
            url=item['url'],
            description=f"⏱️ **{item['status']}**",
            color=0x00ff00 # Green
        )
        
        if item['thumbnail']:
            embed.set_thumbnail(url=item['thumbnail'])
        
        # Fields layout
        embed.add_field(name="📍 Location", value=item['location'], inline=True)
        embed.add_field(name="🏢 Host", value=item['host'], inline=True)
        embed.add_field(name="📅 Period", value=item['period'], inline=True)
        
        # Prize Info
        prize_info = f"**{item['prize_amount']}**\n(Cash: {item['prize_cash']}, Other: {item['prize_other']})"
        embed.add_field(name="💰 Prize", value=prize_info, inline=False)
        
        # Themes
        themes_str = ", ".join(item['themes']) if item['themes'] else "N/A"
        embed.add_field(name="🏷️ Themes", value=themes_str, inline=False)
        
        embed.set_footer(text="Devpost Hackathon Alert")
        return embed

    # ====================================================
    # 🕹️ Command: !hack (Manual Fetch)
    # ====================================================
    @commands.command()
    async def hack(self, ctx):
        """Manually fetches top 3 hackathons."""
        await ctx.send("🔍 Fetching latest hackathons from Devpost...")
        
        hackathons = self.get_hackathons_from_api()
        
        if not hackathons:
            await ctx.send("⚠️ Failed to retrieve data.")
            return

        top_3 = hackathons[:3]
        new_count = 0
        
        for item in top_3:
            embed = self.create_embed(item)
            await ctx.send(embed=embed)
            
            if item['url'] not in self.sent_urls:
                self.sent_urls.append(item['url'])
                new_count += 1
        
        if new_count > 0:
            self.save_data()
            await ctx.send(f"✅ Database updated with {new_count} new item(s).")
        else:
            await ctx.send("👌 These hackathons are already in the database.")
    # ====================================================
    # 📊 Command: !db (Check Database)
    # ====================================================
    @commands.command()
    async def db(self, ctx):
        """Displays all stored hackathon URLs in chunks of 10 items per message."""
        # Use the path defined in __init__
        db_path = self.db_path
        
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

    # ====================================================
    # ⏰ Loop Task: Runs every 1 hour
    # ====================================================
    @tasks.loop(hours=1)
    async def check_new_hackathons(self):
        await self.bot.wait_until_ready()
        print("\n🔄 [Auto] Checking for new hackathons...")
        
        channel = self.bot.get_channel(self.target_channel_id)
        if not channel:
            print(f"⚠️ [Error] Could not find channel with ID: {self.target_channel_id}")
            return

        hackathons = self.get_hackathons_from_api()
        new_count = 0

        if not hackathons:
            print("⚠️ No data retrieved.")
            return

        for item in reversed(hackathons):
            url = item.get('url')
            if url in self.sent_urls:
                continue

            try:
                embed = self.create_embed(item)


                await channel.send("New Hackathon Alert!")
                
                await channel.send(embed=embed)
                print(f"✅ Alert Sent: {item['title']}")
                
                self.sent_urls.append(url)
                new_count += 1
                await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Error sending message: {e}")
                traceback.print_exc()

        if new_count > 0:
            self.save_data()
            print(f"📊 Processed {new_count} new hackathons.")
        else:
            print(f"💤 No new hackathons found.")

    @check_new_hackathons.error
    async def check_new_hackathons_error(self, error):
        print("❌ CRITICAL ERROR in loop!")
        traceback.print_exc()
        print("⚠️ Emergency shutdown for auto-restart...")
        os._exit(1)

async def setup(bot):
    await bot.add_cog(Hackathon(bot))