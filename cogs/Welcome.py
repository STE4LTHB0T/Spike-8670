import discord, random, os
from discord.ext import commands
from pymongo import MongoClient
from resources.Lists import *
 
cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]

class Welcome(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Welcome is loaded!')
  
  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    await self.client.wait_until_ready()
    
    guild = member.guild
    
    welcome_channel = discord.utils.get(guild.text_channels, name="👋🏽︱welcome")
    
    await welcome_channel.send(f'Welcome to the **{guild.name}** Discord Server, {member.mention}!') 
    if guild.id == 414057277050585088:
      await welcome_channel.send(f"Introduce yourself at <#414057277050585090> and get yourself your favorite roles from <#772415743727370260>.")
    await welcome_channel.send(random.choice(welcome_reply))
    

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    guild = member.guild
    if guild.id == 414057277050585088:
      level=ranking.find_one({"id":member.id})
      ranking.delete_one(level)
      guild = member.guild
      left_channel = discord.utils.get(guild.text_channels, name="goodbye-👋🏽")
      await left_channel.send(f'**{member}** just left the server.')
    else:
      guild = member.guild
      left_channel = discord.utils.get(guild.text_channels, name="goodbye-👋🏽")
      await left_channel.send(f'**{member}** just left the server.')
  		


def setup(client):
  client.add_cog(Welcome(client))