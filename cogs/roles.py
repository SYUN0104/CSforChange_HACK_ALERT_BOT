import discord
from discord.ext import commands
import asyncio

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _bot_can_manage(self, guild, role):
        me = guild.me
        if me is None:
            return False
        if not me.guild_permissions.manage_roles:
            return False
        return role < me.top_role

    @commands.command(name="role_add")
    @commands.has_permissions(manage_roles=True)
    async def role_add(self, ctx, member: discord.Member, *, role: discord.Role):
        if ctx.guild is None:
            await ctx.send("This command only works in a server.")
            return

        if not self._bot_can_manage(ctx.guild, role):
            await ctx.send("I can't assign that role.")
            return

        if role in member.roles:
            await ctx.send(f"{member.mention} already has **{role.name}**.")
            return

        try:
            await member.add_roles(role, reason=f"role_add by {ctx.author}")
            await ctx.send(f"Added **{role.name}** to {member.mention}")
        except:
            await ctx.send("Failed to assign role.")

    @commands.command(name="role_remove")
    @commands.has_permissions(manage_roles=True)
    async def role_remove(self, ctx, member: discord.Member, *, role: discord.Role):
        if ctx.guild is None:
            await ctx.send("This command only works in a server.")
            return

        if role not in member.roles:
            await ctx.send(f"{member.mention} does not have **{role.name}**.")
            return

        try:
            await member.remove_roles(role, reason=f"role_remove by {ctx.author}")
            await ctx.send(f"Removed **{role.name}** from {member.mention}")
        except:
            await ctx.send("Failed to remove role.")

    @commands.command(name="role_all_add")
    @commands.has_permissions(manage_roles=True)
    async def role_all_add(self, ctx, *, role: discord.Role):
        if ctx.guild is None:
            await ctx.send("This command only works in a server.")
            return

        if not self._bot_can_manage(ctx.guild, role):
            await ctx.send("I can't assign that role.")
            return

        status = await ctx.send(f"Adding **{role.name}** to everyone…")
        count = 0

        for member in ctx.guild.members:
            if member.bot:
                continue
            if role in member.roles:
                continue
            try:
                await member.add_roles(role, reason=f"role_all_add by {ctx.author}")
                count += 1
                await asyncio.sleep(0.35)
            except:
                pass

        await status.edit(content=f"Role **{role.name}** added to {count} users.")

    @commands.command(name="role_all_remove")
    @commands.has_permissions(manage_roles=True)
    async def role_all_remove(self, ctx, *, role: discord.Role):
        if ctx.guild is None:
            await ctx.send("This command only works in a server.")
            return

        status = await ctx.send(f"Removing **{role.name}** from everyone…")
        count = 0

        for member in ctx.guild.members:
            if role not in member.roles:
                continue
            try:
                await member.remove_roles(role, reason=f"role_all_remove by {ctx.author}")
                count += 1
                await asyncio.sleep(0.35)
            except:
                pass

        await status.edit(content=f"Role **{role.name}** removed from {count} users.")

async def setup(bot):
    await bot.add_cog(Roles(bot))