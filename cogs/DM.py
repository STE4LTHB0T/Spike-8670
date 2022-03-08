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
                  await member.send("Hey! This is Spike from Otaku Nadu OwO. I know this is kinda awkward but man you really should talk there!\nI ain't leaving you alone until you atleast have a role or something.")
          pastDate = datetime.now()
      time.sleep(43200)        



def setup(client):
  client.add_cog(DM(client))