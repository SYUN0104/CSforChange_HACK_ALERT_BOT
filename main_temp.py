import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🚀 로그인 성공: {bot.user.name} ({bot.user.id})')
    print('봇 시스템이 가동 중입니다...')

# Cog 로드 함수
async def load_extensions():
    # cogs 폴더에 있는 hackathon.py를 로드함
    await bot.load_extension("cogs.hackathon")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    if TOKEN:
        asyncio.run(main())
    else:
        print("❌ 에러: .env 파일에 DISCORD_TOKEN이 없습니다.")