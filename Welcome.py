import discord
from discord.abc import GuildChannel
from discord.ext import commands, tasks
import random

from discord.member import Member

class WelcomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot, json_data):
        self.bot = bot
        self.data = json_data["welcome"]

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        await self.bot.get_channel(self.data["channel"]).send(random.choice(self.data["messages"]).format(member.display_name))
        pass