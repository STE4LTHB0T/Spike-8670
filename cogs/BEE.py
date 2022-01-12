import aiofiles, asyncio
from discord.ext import commands

class Bee(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Bee is loaded!')
  
  @commands.command()
  async def thinkingbee(self,ctx):
    user = self.client.get_user(463780399437447200)
    await ctx.send("Please wait for a minute for confirmation!\nTo shutdown the bot, please message **STE4LTH_B0T#3622**.")
    await user.send("**THINKINGBEE** command is about to be used. Be ready!")
    await asyncio.sleep(15)
    async with aiofiles.open(f"./resources/BEE.txt", mode="r") as file:
      lines = await file.readlines()
      for line in lines:
        await ctx.send(line)

def setup(client):
  client.add_cog(Bee(client))