import discord
from discord.ext import commands
import asyncio

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _bot_can_manage(self, guild: discord.Guild, role: discord.Role) -> bool:
        me = guild.me
        if me is None:
            return False
        if not me.guild_permissions.manage_roles:
            return False
        return role < me.top_role

    async def _iter_members(self, guild: discord.Guild):
        # fetch_members is the reliable way (not cache-dependent)
        async for m in guild.fetch_members(limit=None):
            yield m

    @commands.command(name="role_add")
    @commands.has_permissions(manage_roles=True)
    async def role_add(self, ctx, member: discord.Member, *, role: discord.Role):
        if ctx.guild is None:
            return await ctx.send("This command only works in a server.")

        if not self._bot_can_manage(ctx.guild, role):
            return await ctx.send("I can't assign that role (hierarchy/perms).")

        if role in member.roles:
            return await ctx.send(f"{member.mention} already has **{role.name}**.")

        try:
            await member.add_roles(role, reason=f"role_add by {ctx.author}")
            await ctx.send(f"Added **{role.name}** to {member.mention}")
        except discord.Forbidden:
            await ctx.send("Forbidden: hierarchy/permissions.")
        except discord.HTTPException as e:
            await ctx.send(f"HTTP error: {e}")

    @commands.command(name="role_remove")
    @commands.has_permissions(manage_roles=True)
    async def role_remove(self, ctx, member: discord.Member, *, role: discord.Role):
        if ctx.guild is None:
            return await ctx.send("This command only works in a server.")

        if role not in member.roles:
            return await ctx.send(f"{member.mention} does not have **{role.name}**.")

        try:
            await member.remove_roles(role, reason=f"role_remove by {ctx.author}")
            await ctx.send(f"Removed **{role.name}** from {member.mention}")
        except discord.Forbidden:
            await ctx.send("Forbidden: hierarchy/permissions.")
        except discord.HTTPException as e:
            await ctx.send(f"HTTP error: {e}")

    @commands.command(name="role_all_add")
    @commands.has_permissions(manage_roles=True)
    async def role_all_add(self, ctx, *, role: discord.Role):
        if ctx.guild is None:
            return await ctx.send("This command only works in a server.")

        if not self._bot_can_manage(ctx.guild, role):
            return await ctx.send("I can't assign that role (hierarchy/perms).")

        status = await ctx.send(f"Adding **{role.name}** to everyone…")
        added = 0
        skipped = 0
        failed = 0

        async for member in self._iter_members(ctx.guild):
            if member.bot:
                skipped += 1
                continue
            if role in member.roles:
                skipped += 1
                continue

            # If the member’s top role is >= bot’s top role, Discord will block changes
            if ctx.guild.me is None or member.top_role >= ctx.guild.me.top_role:
                skipped += 1
                continue

            try:
                await member.add_roles(role, reason=f"role_all_add by {ctx.author}")
                added += 1
                await asyncio.sleep(1.0)  # safer for rate limits
            except discord.Forbidden:
                failed += 1
            except discord.HTTPException:
                failed += 1
                await asyncio.sleep(2.0)

        await status.edit(content=f"Done. Added: {added}, Skipped: {skipped}, Failed: {failed}")

    @commands.command(name="role_all_remove")
    @commands.has_permissions(manage_roles=True)
    async def role_all_remove(self, ctx, *, role: discord.Role):
        if ctx.guild is None:
            return await ctx.send("This command only works in a server.")

        if not self._bot_can_manage(ctx.guild, role):
            return await ctx.send("I can't remove that role (hierarchy/perms).")

        status = await ctx.send(f"Removing **{role.name}** from everyone…")
        removed = 0
        skipped = 0
        failed = 0

        async for member in self._iter_members(ctx.guild):
            if role not in member.roles:
                skipped += 1
                continue

            if ctx.guild.me is None or member.top_role >= ctx.guild.me.top_role:
                skipped += 1
                continue

            try:
                await member.remove_roles(role, reason=f"role_all_remove by {ctx.author}")
                removed += 1
                await asyncio.sleep(1.0)
            except discord.Forbidden:
                failed += 1
            except discord.HTTPException:
                failed += 1
                await asyncio.sleep(2.0)

        await status.edit(content=f"Done. Removed: {removed}, Skipped: {skipped}, Failed: {failed}")

async def setup(bot):
    await bot.add_cog(Roles(bot))