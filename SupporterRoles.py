import discord
from discord.ext import commands, tasks

from discord.guild import Guild
from discord.member import Member
from discord.role import Role

GUILD_ID = 134626324256915456
SUPPORTER_ROLES = [854637983370182676, 854657267479871498] # Twitch/Patreon
SERVER_SUPPORTER = 854638052152311808 # Server supporter

class SupporterRolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.test_supporter.start()
        
    async def test(member: Member):
        if any(role.id in SUPPORTER_ROLES for role in member.roles):
            if not any(role.id == SERVER_SUPPORTER for role in member.roles):
                await member.add_roles(discord.utils.get(member.guild.roles, id=SERVER_SUPPORTER))
                print(f"Added supporter role to {member.display_name}")
        elif any(role.id == SERVER_SUPPORTER for role in member.roles):
            await member.remove_roles(discord.utils.get(member.guild.roles, id=SERVER_SUPPORTER))
            print(f"Removed supporter role from {member.display_name}")

    @tasks.loop(minutes=1)
    async def test_supporter(self):
        guild: Guild
        for guild in self.bot.guilds:
            # TODO: Use Giana's server ID
            if guild.id != GUILD_ID: continue

            member: Member
            for member in guild.members:
                role: Role
                await SupporterRolesCog.test(member)
    
    @test_supporter.before_loop
    async def before_test_supporter(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if after.guild.id == GUILD_ID:
            await SupporterRolesCog.test(after)
