import discord
from discord.ext import commands, tasks
import requests
import json
import os
import re
import traceback
import asyncio

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx):
        article = {
            "author": "Zak Doffman",
            "title": "Samsung Silently Changes Android On Hundreds Of Millions Of Phones - Forbes",
            "description": "Samsung issues update now warning for most Galaxy smartphone owners.",
            "url": "https://www.forbes.com/sites/zakdoffman/2026/01/08/samsung-silently-changes-android-on-hundreds-of-millions-of-phones/",
            "urlToImage": "https://imageio.forbes.com/specials-images/imageserve/67155e6d2508edcb3450b4d7/0x0.jpg?format=jpg&crop=862,485,x654,y234,safe&height=900&width=1600&fit=bounds",
            "publishedAt": "2026-01-08T21:16:00Z",
            "content": "Update now warning issued for most Galaxy users..."
        }

        embed = discord.Embed(
            title=article["title"],
            url=article["url"],
            description=article["description"],
            color=0x2ecc71
        )

        if article.get("author"):
            embed.set_author(name=article["author"])

        if article.get("publishedAt"):
            embed.add_field(name="Published", value=article["publishedAt"], inline=False)

        if article.get("urlToImage"):
            embed.set_image(url=article["urlToImage"])

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(News(bot))