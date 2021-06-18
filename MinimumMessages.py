import discord
from discord.ext import commands, tasks


class MinimumMessagesCog(commands.Cog):
    def __init__(self, bot: commands.Bot, json_data):
        self.bot = bot
        self.data = json_data

    @commands.Cog.listener()
    async def on_ready(self):
        
        pass