import discord, random, os
from resources.Lists import *
from discord.ext import commands, tasks
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://spike:sentientbot@spike.yqn3s.mongodb.net/<dbname>?retryWrites=true&w=majority")
profile = cluster["discord"]["profiles"]


class Profile(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Profile is loaded!')

  @commands.command()
  async def register(self,ctx,client:str,username:str):
    number=random.randint(0, 50000)
    new={"_id":number,"name":ctx.author.name,"id":ctx.author.id,"client":client,"username":username}
    if username and client not in bannedwords:
      profile.insert_one(new)
      await ctx.reply("Profile registered!")
    else:
      await ctx.reply("Fuck off gaaju") 
  
  @commands.command()
  async def deregister(self,ctx,client:str):
    tag=profile.find_one({"id":ctx.author.id,"client":client})
    profile.delete_one(tag)
    await ctx.reply("Profile deregistered!")        

  @commands.command()
  async def profile(self,ctx, member:discord.Member=None):
    if member is None:
      member = ctx.author
    tag=profile.find({"id":member.id})
    i=1
    eprofile=discord.Embed(title="Profile",description=f"Profile Database of {member.mention}",color=discord.Color.red())
    for x in tag:
      try:
        temp=x["client"]
        tempname=x["username"]
        eprofile.add_field(name=f"{i}: {temp}", value=f"{tempname}",inline=False)
        i+=1
      except:
        pass
    eprofile.set_thumbnail(url=member.avatar_url)
    await ctx.reply(embed=eprofile)

def setup(client):
  client.add_cog(Profile(client))
