import discord
from discord.ext import commands

class ReactionRolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot, json_data):
        self.bot = bot
        self.data = json_data

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id != 854624350900977665: return
        print(payload.emoji)
        print(payload.emoji.name)
        print(payload.emoji.is_custom_emoji())
        print(payload.emoji.id)
        print(payload.emoji == ":game_die:")
        print(payload.emoji == "game_die")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        print(payload.emoji.name)

