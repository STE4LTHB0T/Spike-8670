import discord, random, os
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ['MONGO'])

warnings = cluster["discord"]["warnings"]

class Warnings(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        print("Warnings is loaded!")

    @commands.command(aliases=["casereg", "cr"])
    @commands.has_permissions(kick_members=True)
    async def caseregister(self,ctx, member:discord.Member=None, *,reason=None):
        guild=ctx.guild
        log_channel = discord.utils.get(guild.text_channels, name="log-channel")    
        
        if member is None:
            return await ctx.reply("Time to increase wanted level for somebody!<:MingoPepe:502444849442586644>")

        number=random.randint(0, 50000)
        warn={"_id":number,"guild":ctx.guild.id, "warned":member.name, "memid":member.id, "mod":ctx.author.name, "modid":ctx.author.id, "reason":reason}
        warnings.insert_one(warn)

        warn=discord.Embed(title="Case Registered!", color=ctx.author.color)
        warn.add_field(name="Moderator",value=f"{ctx.author.mention}",inline=True)
        warn.add_field(name="Member",value=f"{member.mention}",inline=True)
        warn.add_field(name="Reason",value=f"{reason}",inline=True)
        warn.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=warn)
        await log_channel.send(embed=warn)

    @commands.command()
    async def cases(self,ctx, member: discord.Member=None):
        if member is None:
          return await ctx.send("https://tenor.com/view/edward-cowboy-bebop-web-jamming-gif-14503901")

        warns= warnings.find({"memid":member.id})
        if warns is None:
          await ctx.reply("No cases found!")
        else:
          i=1
          try:
            warnembed = discord.Embed(title=f"Displaying cases for {member.name}", description="", colour=discord.Colour.red())
            warnembed.set_thumbnail(url=member.avatar_url)						
            for x in warns:
                #tempmod=warn["modid"]
                #mod=ctx.guild.get_member(tempmod)
                tempreason=x["reason"]
                tempid=x["_id"]
                warnembed.description += f"**Case {i}: ID {tempid}** given for **{tempreason}**.\n"
                i+=1
            await ctx.reply(embed=warnembed)          
          except KeyError:
                pass
								
    @commands.command(aliases=["delcase", "dc"])
    @commands.has_permissions(kick_members=True)
    async def deletecase(self,ctx,id:int):
        deletion=warnings.find_one({"_id":id})
        tempguild=deletion["guild"]
        if ctx.guild.id == tempguild:
          warnings.delete_one(deletion)
          await ctx.reply("Case Closed!")
        else:
          await ctx.reply("https://tenor.com/view/bar-fight-brawl-cowboy-bebop-fight-action-gif-22945279")
      
def setup(client):
    client.add_cog(Warnings(client))  