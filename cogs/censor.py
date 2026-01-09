import discord
from discord.ext import commands
import re

class Censor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bad_words = [
            "yes",
            "badword2",
            "badword3"
        ]

        self.pattern = re.compile(
            r"\b(" + "|".join(map(re.escape, self.bad_words)) + r")\b",
            re.IGNORECASE
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return


        if self.pattern.search(message.content):
            try:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, watch your language.",
                    delete_after=5
                )
            except (discord.Forbidden, discord.NotFound):
                pass

async def setup(bot):
    await bot.add_cog(Censor(bot))