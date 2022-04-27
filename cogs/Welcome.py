import discord, random, os
from discord.ext import commands
from pymongo import MongoClient
from resources.Lists import *
 
cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]

msg_channel = cluster["discord"]["channels"]

class Welcome(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Welcome is loaded!')
  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    await self.client.wait_until_ready()
    try:
      guild = member.guild
      welcome=msg_channel.find_one({"_id":"Welcome", "guild id":guild.id})
      tempid=welcome["channel id"]
      welcomechannel = await self.client.fetch_channel(tempid)
  
      await welcomechannel.send(f'Welcome to the **{guild.name}** Discord Server, {member.mention}!') 
      
      if guild.id == 414057277050585088:
        await welcomechannel.send(f"Introduce yourself at <#414057277050585090> and get yourself your favorite roles from <#772415743727370260>.")
      
      await welcomechannel.send(random.choice(welcome_reply))
    except Exception as e:
      print(e)

  @commands.Cog.listener()
  async def on_member_remove(self, member):
      guild = member.guild
      
      level=ranking.find_one({"id":member.id, "guild id":guild.id})
      tempwoolongs=level["woolongs"]

      spike=ranking.find_one({"id": "804347400004173864", "guild id":guild.id})
                               
      left=spike["woolongs"]+tempwoolongs

      spike=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":left}})        
        
      ranking.delete_one(level)
      
      try:
        goodbye=msg_channel.find_one({"_id":"Goodbye", "guild id":guild.id})
        tempid=goodbye["channel id"]
        goodbyechannel = await self.client.fetch_channel(tempid)

        await goodbyechannel.send(f'**{member}** just left the server.')
      
      except Exception as e:
        print(e)

def setup(client):
  client.add_cog(Welcome(client))