import discord, time
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

class DM(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('DM is loaded!')


  @commands.Cog.listener()
  async def beactive(self):
      guild=414057277050585088
      pastDate = 0
      check_role = get(guild.message.server.roles, name='Shinobi')
      if (datetime.now() - pastDate).days>1:       
          for member in guild.members:
              if check_role not in member.roles:
                  try:
                      await member.send("Hey! This is Spike from Otaku Nadu OwO. I know this is kinda awkward but man you really should talk there!\nI ain't leaving you alone until you atleast have a role or something.")
                  except:
                      continue
          pastDate = datetime.now()
      time.sleep(43200)

        
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