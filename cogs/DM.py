import discord, time
from datetime import datetime
from discord.ext import commands
from discord.utils import get

class DM(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('DM is loaded!')
        
  @commands.command()
  async def dm(self, ctx, user_id=None, *, args=None):
      if user_id != None and args != None:
          try:
              target = await self.client.fetch_user(user_id)
              await ctx.message.delete()
              await target.send(args)
              await ctx.send("Delivered!", delete_after=2)

          except:
              await ctx.channel.send("Adhellam pannah mudiyadhu!")
              
          else:
              await ctx.channel.send("Aaley illa, bell'u!")

def setup(client):
  client.add_cog(DM(client))