import discord
from discord.ext import commands, tasks

from discord.guild import Guild
from discord.member import Member
from discord.role import Role

SUPPORTER_ROLES = [854637983370182676, 854657267479871498] # Twitch/Patreon
SERVER_SUPPORTER = 854638052152311808 # Server supporter

class SupporterRolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot, json_data):
        self.bot = bot
        self.data = json_data

        self.test_supporter.start()
        
    async def test(self, member: Member):
        for supporter_role in self.data['supporter_roles']:
            main_role = supporter_role['main_role']
            sub_roles = supporter_role['sub_roles']
            
            if any(role.id in sub_roles for role in member.roles):
                if not any(role.id == main_role for role in member.roles):
                    await member.add_roles(discord.utils.get(member.guild.roles, id=main_role))
            elif any(role.id == main_role for role in member.roles):
                await member.remove_roles(discord.utils.get(member.guild.roles, id=main_role))

    @tasks.loop(minutes=1)
    async def test_supporter(self):
        guild: Guild
        for guild in self.bot.guilds:
            if guild.id != self.data["server_id"]: continue

            member: Member
            for member in guild.members:
                role: Role
                await self.test(member)
    
    @test_supporter.before_loop
    async def before_test_supporter(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if after.guild.id == self.data["server_id"]:
            await self.test(after)
