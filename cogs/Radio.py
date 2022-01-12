import discord, random
from discord.ext import commands
from discord import FFmpegPCMAudio

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
    radio=["https://listen.moe/stream", 
  
    "http://curiosity.shoutca.st:6110/",

    "http://animefm.stream.laut.fm/animefm?t302=2021-04-21_07-22-21&uuid=142de8f2-705d-4cde-9584-f8b20f7a460b",

    "http://node-17.zeno.fm/ddetxwuhkpeuv?rj-ttl=5&rj-tok=AAABePLQ_Y4AuNQxaMySAOZYjQ",

    "http://91.232.4.33:7028/",

    "http://listen.ur-radio.de/anime.mp3"]
    player.play(FFmpegPCMAudio(random.choice(radio)))

  @commands.command()
  async def rstop(self,ctx):
    player.stop()
    await ctx.guild.voice_client.disconnect()

def setup(client):
  client.add_cog(Radio(client))