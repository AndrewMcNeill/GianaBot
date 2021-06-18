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
        self.message_counts = {}

    async def add_role(self, member: Member):
        try:
            role_tier = next(x for x in self.message_data if x['count'] <= self.message_counts[member.id])
            if role_tier['role'] not in [r.id for r in member.roles]:
                for count_role in self.message_data:
                    await member.remove_roles(discord.utils.get(member.guild.roles, id=count_role['role']))
                await member.add_roles(discord.utils.get(member.guild.roles, id=role_tier['role']))
            pass
        except KeyError:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        guild: Guild = self.bot.get_guild(self.data['server_id'])
        member: Member
        for member in guild.members:
            self.message_counts[member.id] = 0
        channel: TextChannel
        for channel in guild.text_channels:
            message: Message
            async for message in channel.history(limit=999999):
                try:
                    self.message_counts[message.author.id] += 1
                except KeyError:
                    pass
        for member in guild.members:
            await self.add_role(member)
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        try:
            self.message_counts[message.author.id] += 1
            await self.add_role(message.author)
        except KeyError:
            pass

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        try:
            self.message_counts[message.author.id] -= 1
        except KeyError:
            pass