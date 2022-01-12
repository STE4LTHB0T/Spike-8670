import discord, random
from discord.ext import commands


class Mentions(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Mentions is loaded!')

  @commands.Cog.listener()
  async def on_message(self, message):
    
    mentions=["<:GWfroggyKermitReee:477838636054872064>yare yare daze",

    "Stop tagging me and do some productive work!<:FeelsCopMan:477774218797383696>",
    
    "Stop tagging me!<:GWfroggyKermitReee:477838636054872064>",
    
    "I am busy unlike you tagging a bot<:immaputinher:477774164321894440>",
    
    "It seems that a lifeless person is tagging me. Get a life dude!<:lmao:477783011094560778>", 

    "if you want help, do **spike help** dont't tag me<:facepalms:888372972757348372>",
    
    "https://tenor.com/view/franklin-lamar-lamar-roasts-franklin-gif-19948223"]
    
    for x in message.mentions:
      if (x == self.client.user):
        if message.author == self.client.user:
          return
        if message.author.id == 310366898678136832:
          await message.channel.send(f"{message.author.mention} Bot Instrumentality Project Banzai🥂")
          return

        elif message.author.id == 463780399437447200:
          await message.channel.send(f"hisashiburi {message.author.mention}!")
          await message.channel.send("https://media.giphy.com/media/5gK1hvwoutPnG/giphy.gif")
          return
        
        elif message.author.id == 261143180387287040:
          await message.channel.send("big fan, saar<:pepe:477838638185578496>")

        else:
          await message.channel.send(random.choice(mentions))


def setup(client):
    client.add_cog(Mentions(client))