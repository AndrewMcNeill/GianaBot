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

client = commands.Bot(command_prefix='.', intents=intents)



@client.event
async def on_member_join(member: discord.Member):
    print(f'{member.nick} has joined a server')
    
@client.event
async def on_member_remove(member: discord.Member):
    print(f'{member.nick} has left a server')

@client.command(aliases = ['test'])
async def command_test(context: commands.Context):
    await context.send('You have tested!')

@client.command()
@commands.has_permissions(administrator=True)
async def die(context: commands.Context):
    await client.close()


@tasks.loop(minutes=1)
async def test_supporter():
    guild: Guild
    for guild in client.guilds:
        # TODO: Use Giana's server ID
        if guild.id != 134626324256915456: continue

        member: Member
        for member in guild.members:
            role: Role
            
            supporter_roles = [854637983370182676] # Twitch supporter
            server_supporter = 854638052152311808 # Server supporter
            if any(role.id in supporter_roles for role in member.roles):
                if not any(role.id == server_supporter for role in member.roles):
                    await member.add_roles(discord.utils.get(guild.roles, id=server_supporter))
                    print(f"Added supporter role to {member.display_name}")
            elif any(role.id == server_supporter for role in member.roles):
                await member.remove_roles(discord.utils.get(guild.roles, id=server_supporter))
                print(f"Removed supporter role from {member.display_name}")



# initialize
@client.event
async def on_ready():
    print('Bot is ready.')
    test_supporter.start()


client.run('ODU0NjExMTc1NjA0ODc5Mzgw.YMmcrg.GaCI887xy3bA61Fb463K6pgkjoU')