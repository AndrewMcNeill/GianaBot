from SupporterRoles import SupporterRolesCog
from ReactionRoles import ReactionRolesCog
import discord
from discord.ext import commands, tasks
import asyncio

from discord.abc import GuildChannel
from discord.guild import Guild
from discord.member import Member
from discord.role import Role

intents: discord.Intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='.', intents=intents)



@bot.event
async def on_member_join(member: discord.Member):
    print(f'{member.nick} has joined a server')
    
@bot.event
async def on_member_remove(member: discord.Member):
    print(f'{member.nick} has left a server')

@bot.command(aliases = ['test'])
async def command_test(context: commands.Context):
    await context.send('You have tested!')

@bot.command()
@commands.has_permissions(administrator=True)
async def die(context: commands.Context):
    await bot.close()






# initialize
@bot.event
async def on_ready():
    print('Bot is ready.')


bot.add_cog(ReactionRolesCog(bot))
bot.add_cog(SupporterRolesCog(bot))
bot.run('ODU0NjExMTc1NjA0ODc5Mzgw.YMmcrg.GaCI887xy3bA61Fb463K6pgkjoU')