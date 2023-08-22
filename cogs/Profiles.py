import discord, random, os, logging
from discord.ext import commands, tasks
from pymongo import MongoClient

cluster = MongoClient(os.environ["MONGO"])

profile = cluster["discord"]["profiles"]

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profiles is loaded!")

    @commands.hybrid_command(name = "register", with_app_command = True, description = "Registers a gaming profile of the user")
    async def register(self, ctx, client : str, username : str):
        number = random.randint(0, 50000)
        new = {"_id" : number , "name" : ctx.author.name, "id" : ctx.author.id, "client" : client, "username" : username}
        profile.insert_one(new)
        await ctx.reply("Profile registered!", ephemeral = False)
  
    @commands.hybrid_command(name = "deregister", with_app_command = True, description = "Deregisters a gaming profile of the user")
    async def deregister(self, ctx, client : str):
        tag = profile.find_one({"id" : ctx.author.id, "client" : client})
        profile.delete_one(tag)
        await ctx.reply("Profile deregistered!", ephemeral = False)        

    @commands.hybrid_command(name = "profile", with_app_command = True, description = "Shows the profile of a member")
    async def profile(self, ctx, member : discord.Member = None):
        try:
            if member is None:
                member = ctx.author
            if profile.count_documents({"id" : member.id}) == 0:
                pathetic = discord.Embed(description = "No profile found!")
                await ctx.channel.send(embed = pathetic, ephemeral = False)      
            else:
                tag = profile.find({"id" : member.id})
                i=1
                eprofile = discord.Embed(title = "Profile", description = f"Profile Database of {member.mention}", color = 0xff0000)
                for x in tag:
                    try:
                        temp = x["client"]
                        tempname = x["username"]
                        eprofile.add_field(name = f"{i} : {temp}", value = f"{tempname}", inline = False)
                        i+=1
                    except:
                        pass
                eprofile.set_thumbnail(url = member.avatar.url)
                await ctx.reply(embed = eprofile, ephemeral = False)
        except Exception as e:
            print(e)

async def setup(client):
  await client.add_cog(Profile(client))