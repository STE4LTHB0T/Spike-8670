import discord, random
from discord.ext import commands
from discord import FFmpegPCMAudio
from resources.Lists import *

class Radio(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Radio is loaded!')

  @commands.command()
  async def rplay(self,ctx):
    channel = ctx.message.author.voice.channel
    global player
    try:
      player = await channel.connect()
    except:
      pass
    player.play(FFmpegPCMAudio(random.choice(radio)))

  @commands.command()
  async def rstop(self,ctx):
    player.stop()
    await ctx.guild.voice_client.disconnect()

def setup(client):
  client.add_cog(Radio(client))