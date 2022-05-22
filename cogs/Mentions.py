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
          await message.channel.send(f"{message.author.mention} Bot Instrumentality Project Banzai🥂", delete_after=5)
          return

        elif message.author.id == 463780399437447200:
          await message.channel.send(f"Hisashiburi {message.author.mention}!", delete_after=5)
          await message.channel.send("https://media.giphy.com/media/5gK1hvwoutPnG/giphy.gif", delete_after=5)
          return
        
        elif message.author.id == message.guild.owner.id:
          await message.channel.send("Hello, Chief!<:FeelsFedoraMan:477838638185578496>", delete_after=5)

        else:
          await message.channel.send(random.choice(mentions_reply), delete_after=15)


def setup(client):
    client.add_cog(Mentions(client))