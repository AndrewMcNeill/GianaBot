import discord
from discord.ext import commands
from discord.guild import Guild
from discord.member import Member
import emoji

class ReactionRolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot, json_data):
        self.bot = bot
        self.data = json_data['reaction_roles']
        self.messages = [x['message'] for x in self.data]
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id not in self.messages: return
        for reaction_role in self.data:
            if reaction_role['message'] == payload.message_id:
                for emoji_role in reaction_role['emoji']:
                    if emoji.demojize(payload.emoji.name).replace(':', '') == emoji_role['emoji']:
                        await payload.member.add_roles(discord.utils.get(payload.member.guild.roles, id=emoji_role['role']))
                break

        

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id not in self.messages: return
        for reaction_role in self.data:
            if reaction_role['message'] == payload.message_id:
                for emoji_role in reaction_role['emoji']:
                    if emoji.demojize(payload.emoji.name).replace(':', '') == emoji_role['emoji']:
                        member = self.get_member(payload)
                        await member.remove_roles(discord.utils.get(member.guild.roles, id=emoji_role['role']))
                break

    def get_member(self, payload: discord.RawReactionActionEvent):
        guild: Guild = [g for g in self.bot.guilds if g.id == payload.guild_id][0]
        member: Member = [m for m in guild.members if m.id == payload.user_id][0]
        return member