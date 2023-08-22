import discord, random, os, logging
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ['MONGO'])

warnings = cluster["discord"]["warnings"]

msg_channel = cluster["discord"]["channels"]

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class Cases(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cases is loaded!")

    @commands.hybrid_command(name = "caseregister", with_app_command = True, description = "Registers a case on the user")
    @commands.has_permissions(kick_members = True)
    async def caseregister(self, ctx, member : discord.Member = None, *,reason = None):        
        if member is None:
            return await ctx.reply("Time to increase wanted level for somebody!<:MingoPepe:502444849442586644>")

        number = random.randint(0, 50000)
        warn = {"_id" : number,"guild" : ctx.guild.id, "warned" : member.name, "memid" : member.id, "mod" : ctx.author.name, "modid" : ctx.author.id, "reason" : reason}
        warnings.insert_one(warn)

        warn = discord.Embed(title = "Case Registered!", color = ctx.author.color)
        warn.add_field(name = "Moderator", value = f"{ctx.author.mention}", inline = True)
        warn.add_field(name = "Member", value = f"{member.mention}", inline = True)
        warn.add_field(name = "Reason", value = f"{reason}", inline = True)
        warn.set_thumbnail(url = member.avatar.url)
        await ctx.reply(embed = warn, ephemeral = False)
        try:
            case = msg_channel.find_one({"guild id" : ctx.guild.id, "name":"Moderation"})
            tempid = case["channel id"]
            casechannel = await self.client.fetch_channel(tempid)
            await casechannel.send(embed = warn)
        except Exception as e:
            pass

    @commands.hybrid_command(name = "deletecase", with_app_command = True, description = "Deletes a case of the user")
    @commands.has_permissions(kick_members = True)
    async def deletecase(self, ctx, id : int):
        deletion = warnings.find_one({"_id" : id})
        tempguild = deletion["guild"]
        if ctx.guild.id == tempguild:
            warnings.delete_one(deletion)
            await ctx.reply("Case Closed!", ephemeral = False)
        else:
            await ctx.reply("https://tenor.com/view/bar-fight-brawl-cowboy-bebop-fight-action-gif-22945279", ephemeral = False)

    @commands.hybrid_command(name = "cases", with_app_command = True, description = "Shows the cases of the user")
    async def cases(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("https://tenor.com/view/edward-cowboy-bebop-web-jamming-gif-14503901")
        if warnings.count_documents({"memid" : member.id}) == 0:
            pathetic = discord.Embed(description = "No cases registered!")
            await ctx.reply(embed = pathetic, ephemeral = False)
        else:
            i=1
            warns = warnings.find({"memid" : member.id})
            warnembed = discord.Embed(title = f"Displaying cases for {member.name}", description = "", colour = 0xff0000)
            warnembed.set_thumbnail(url = member.avatar.url)						
            for x in warns:
                tempreason = x["reason"]
                tempid = x["_id"]
                warnembed.description += f"**Case {i} : ID {tempid}** given for **{tempreason}**.\n"
                i+=1
            await ctx.reply(embed = warnembed, ephemeral = False)
      
async def setup(client):
    await client.add_cog(Cases(client))