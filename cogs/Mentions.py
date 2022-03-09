import discord, random
from discord.ext import commands
from resources.Lists import *


class Mentions(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Mentions is loaded!')

  @commands.Cog.listener()
  async def on_message(self, message):    
    for x in message.mentions:
      if (x == self.client.user):
        if message.author == self.client.user:
          return
        if message.author.id == 310366898678136832:
          await message.channel.send(f"{message.author.mention} Bot Instrumentality Project Banzai🥂")
          return

        elif message.author.id == 463780399437447200:
          await message.channel.send(f"Hisashiburi {message.author.mention}!")
          await message.channel.send("https://media.giphy.com/media/5gK1hvwoutPnG/giphy.gif")
          return
        
        elif message.author.id == 261143180387287040:
          await message.channel.send("big fan, saar<:FeelsHypeMan:477783011887153182>")

        else:
          await message.channel.send(random.choice(mentions_reply))


def setup(client):
    client.add_cog(Mentions(client))