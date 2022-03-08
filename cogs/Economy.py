import discord, os, asyncio
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]
class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy is loaded!')

    @commands.command()
    async def trade(self,ctx,member:discord.Member,woolong:int):
        await ctx.reply("Beginning Bounty Transaction!")
        async with ctx.typing():
            await asyncio.sleep(0.5)        
        async with ctx.typing():
            await asyncio.sleep(0.5)
        await ctx.reply(f"Transferring {woolong} Woolongs to {member.mention} from {ctx.author.mention}")
        sender=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
        reciever=ranking.find_one({"id":member.id, "guild id":ctx.guild.id})
        send=sender["xp"]-woolong
        recieve=reciever["xp"]+woolong
        sender=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"xp":send}})
        reciever=ranking.update_one({"id":member.id, "guild id":ctx.guild.id},{"$set":{"xp":recieve}})        
        async with ctx.typing():
            await asyncio.sleep(0.5)
        await ctx.reply("Bounty Transaction successful!")

def setup(client):
  client.add_cog(Economy(client))