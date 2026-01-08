import asyncio
import discord
import traceback
from discord.ext import commands, tasks
import requests
import json
import os
import re

class Hackathon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Path to store the database of sent hackathons
        self.db_path = "./data/database.json"
        
        # Load existing data when the bot starts
        self.sent_urls = self.load_data()
        
        # Load Target Channel ID from Environment Variable
        self.target_channel_id = int(os.getenv('CHANNEL_ID', 0))
        
        # Start the background task immediately
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
        # FIFO Logic: Keep only the last 30 items
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
        """Removes HTML tags from a string."""
        if not text: return "Unknown"
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()

    def get_hackathons_from_api(self):
        """Fetches REAL hackathon data from Devpost API."""
        url = "https://devpost.com/api/hackathons"
        
        # Parameters to get the latest public hackathons
        params = {
            'open_to[]': 'public',
            'order_by': 'recently-added',
            'page': 1
        }
        
        # Headers are crucial to avoid being blocked by Devpost
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('hackathons', [])
            else:
                print(f"⚠️ API Request failed: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ API Connection Error: {e}")
            return []

    # ====================================================
    # ⏰ Loop Task: Runs every 1 hour
    # ====================================================
    @tasks.loop(hours=1)
    async def check_new_hackathons(self):
        # Wait until the bot is fully ready
        await self.bot.wait_until_ready()
        
        print("\n🔄 [Auto] Checking for new hackathons from Devpost...")
        
        channel = self.bot.get_channel(self.target_channel_id)
        
        if not channel:
            print(f"⚠️ [Error] Could not find channel with ID: {self.target_channel_id}")
            return

        # Fetch data
        hackathons = self.get_hackathons_from_api()
        new_count = 0

        if not hackathons:
            print("⚠️ No data retrieved from Devpost.")
            return

        # Iterate in reverse (Oldest -> Newest)
        for item in reversed(hackathons):
            url = item.get('url')
            
            # Duplicate Check
            if url in self.sent_urls:
                continue

            # Process NEW hackathon
            try:
                title = item.get('title', 'No Title')
                thumbnail = item.get('thumbnail_url', '')
                if thumbnail and thumbnail.startswith("//"): thumbnail = "https:" + thumbnail
                
                status = item.get('time_left_to_submission', 'N/A')
                prize = self.clean_html_tags(item.get('prize_amount', '0'))
                
                # Retrieve dates if available
                period = item.get('submission_period_dates', 'N/A')
                
                # Create Embed
                embed = discord.Embed(title=title, url=url, color=0x00ff00)
                if thumbnail: embed.set_thumbnail(url=thumbnail)
                embed.add_field(name="Status", value=status, inline=True)
                embed.add_field(name="Prize", value=prize, inline=True)
                embed.add_field(name="Period", value=period, inline=True)
                embed.set_footer(text="Devpost New Alert")

                # Send Message
                await channel.send(embed=embed)
                print(f"✅ Alert Sent to #{channel.name}: {title}")
                
                self.sent_urls.append(url)
                new_count += 1
                
                # Sleep briefly to avoid rate limits (optional)
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Error sending message: {e}")

        # Save data if updated
        if new_count > 0:
            self.save_data()
            print(f"📊 Processed {new_count} new hackathons.")
        else:
            print(f"💤 No new hackathons found in #{channel.name}.")
        pass

    @check_new_hackathons.error
    async def check_new_hackathons_error(self, error):
        print("❌ CRITICAL ERROR in hackathon loop!")
        traceback.print_exc() # ERROR LOG PRINT

        print("⚠️ Initiating emergency shutdown to trigger Railway auto-restart...")
        os._exit(1) # Process Auto-shutdown -> Railway dectect and restart

async def setup(bot):
    await bot.add_cog(Hackathon(bot))