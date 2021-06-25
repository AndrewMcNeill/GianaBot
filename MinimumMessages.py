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
        print(self.message_data)
        self.message_counts = {}

    async def add_role(self, member: Member):
        try:
            role_tier = max([x for x in self.message_data if x[0] <= self.message_counts[member.id]], key=lambda x:x[0])
            print(self.message_counts[member.id], role_tier)
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
                    #print(f"Member {message.author} no longer in server")
                    pass
        for member in guild.members:
            await self.add_role(member)
    
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