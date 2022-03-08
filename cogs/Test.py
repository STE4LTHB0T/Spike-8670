import discord, random, os
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ['MONGO'])

giveaway = cluster["discord"]["giveaway"]


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Test is loaded!')
    

    @commands.command()
    async def test(self, ctx):
        await ctx.reply("This cog is active!")

    @commands.command()
    async def create(self, ctx):
        number = random.randint(0, 50000)
        creator = {"_id": number, "name": ctx.author.name, "id": ctx.author.id}
        giveaway.insert_one(creator)
        await ctx.send("Giveaway created!")

    @commands.command()
    async def enter(self, ctx):
        number = random.randint(0, 50000)
        participant = {"_id": number, "name": ctx.author.name, "id": ctx.author.id}
        giveaway.insert_one(participant)
        await ctx.send("Entered into the Giveaway!")


    @commands.command()
    async def giveaway(self, ctx):
        participants = giveaway.find({}, {"id": 1})
        for x in participants:
            try:
                win = random.choice(x)
                await ctx.send(f"{win}")
            except:
                pass

        """winner=random.choice(participants)
        if ctx.author.id == cid:
          if not cid:
            await ctx.send(f"The winner is {winner.mention}! Contact {cid.mention} for your prize!")
            giveaway.delete_one(winner)"""

    @commands.command()
    async def guild(self, ctx):
        user = self.client.get_user(463780399437447200)
        for guild in self.client.guilds:
            await user.send(guild)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 495020983267229706:
            await message.publish()

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
  client.add_cog(Test(client))