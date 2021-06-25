import discord
from discord.abc import GuildChannel
from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.guild import Guild
from discord.member import Member
from discord.message import Message
from discord.role import Role


class MinimumMessagesCog(commands.Cog):
    def __init__(self, bot: commands.Bot, json_data):
        self.bot = bot
        self.data = json_data
        self.message_data = sorted(json_data['message_counts'], key=lambda x: x['count'], reverse=True)
        self.message_data = [(x['count'], x['role']) for x in self.message_data]
        self.message_counts = {}

    async def add_role(self, member):
        guild: Guild = await self.bot.fetch_guild(self.data['server_id'])
        try:
            member = await guild.fetch_member(member.id)
        except:
            return
        try:
            role_tier = max([x for x in self.message_data if x[0] <= self.message_counts[member.id]], key=lambda x:x[0])
            #print(self.message_counts[member.id], role_tier)
            if role_tier[1] not in [r.id for r in member.roles]:
                for count_role in self.message_data:
                    if count_role == role_tier:
                        continue
                    await member.remove_roles(discord.utils.get(member.guild.roles, id=count_role[1]))
                await member.add_roles(discord.utils.get(member.guild.roles, id=role_tier[1]))
        except KeyError:
            print(f"Member {member} not valid")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Counting member messages")
        guild: Guild = await self.bot.fetch_guild(self.data['server_id'])
        member: Member
        async for member in guild.fetch_members():
            self.message_counts[member.id] = 0
        channel: TextChannel
        for channel in await guild.fetch_channels():
            if not isinstance(channel, TextChannel): continue
            message: Message
            async for message in channel.history(limit=999999):
                try:
                    self.message_counts[message.author.id] += 1
                except KeyError:
                    self.message_counts[message.author.id] = 1
        async for member in guild.fetch_members():
            await self.add_role(member)
        print("Member messages counted")
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.id in self.message_counts:
            self.message_counts[message.author.id] = 0
        self.message_counts[message.author.id] += 1
        await self.add_role(message.author)

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        try:
            self.message_counts[message.author.id] -= 1
        except KeyError:
            print(f"Member {message.author} no longer in server")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        self.message_counts[member.id] = 0
        await self.add_role(member)