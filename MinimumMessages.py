import discord
from discord.abc import GuildChannel
from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.guild import Guild
from discord.member import Member
from discord.message import Message


class MinimumMessagesCog(commands.Cog):
    def __init__(self, bot: commands.Bot, json_data):
        self.bot = bot
        self.data = json_data
        self.message_counts = {}

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
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        try:
            self.message_counts[message.author.id] += 1
        except KeyError:
            pass

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        try:
            self.message_counts[message.author.id] -= 1
        except KeyError:
            pass