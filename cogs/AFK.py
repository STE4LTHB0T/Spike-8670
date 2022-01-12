import discord
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime, timedelta

cluster = MongoClient("mongodb+srv://spike:sentientbot@spike.yqn3s.mongodb.net/<dbname>?retryWrites=true&w=majority")

reminder = cluster["discord"]["reminder"]  


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd', 'w']:
            return (int(amount), unit)

        raise commands.BadArgument(message="Not a valid duration!")

class AFK(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('AFK is loaded!')
  
  
def setup(client):
  client.add_cog(AFK(client))