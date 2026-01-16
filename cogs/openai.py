import os
from discord.ext import commands
from openai import AsyncOpenAI

SYSTEM_PROMPT = (
    "You are CSforChange Helper, a Discord bot created for the CSforChange server. "
    "You are NOT ChatGPT. You must NEVER mention OpenAI, ChatGPT, GPT, or language models. "
    "When asked who you are, say: 'I am CSforChange Helper, the AI assistant for this server.' "
    "Be concise, technical, and direct. No emojis. No filler."
)


class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @commands.command()
    async def chat(self, ctx, *, prompt: str):
        if not os.getenv("OPENAI_API_KEY"):
            await ctx.send("❌ OPENAI_API_KEY not found in .env")
            return

        try:
            r = await self.client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            text = (r.output_text or "").strip()
            await ctx.send(text[:2000] if text else "(no response)")
        except Exception as e:
            await ctx.send(f"❌ OpenAI error: {type(e).__name__}")

async def setup(bot):
    await bot.add_cog(OpenAI(bot))
