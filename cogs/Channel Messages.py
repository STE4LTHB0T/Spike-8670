import discord, os, logging
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from pymongo import MongoClient
from resources.Lists import *
 
cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]

msg_channel = cluster["discord"]["channels"]

msg = cluster["discord"]["messages"]

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class ChannelMessages(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Channel Messages is loaded!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.client.wait_until_ready()
        try:
            guild = member.guild
            welcome = msg_channel.find_one({"guild id" : guild.id, "name" : "welcome"})
            tempid = welcome["channel id"]
            welcomechannel = await self.client.fetch_channel(tempid)
            try:
                channel = msg.find_one({"guild id" : guild.id, "name" : "wmsg"})
                temp = channel["message"]
                await welcomechannel.send(f"{temp}")
            except:
                await welcomechannel.send(f'Welcome to the **{guild.name}** Discord Server, {member.mention}!')  
                await welcomechannel.send(random.choice(welcome_reply))
        except Exception as e:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild

        level = ranking.find_one({"id" : member.id, "guild id" : guild.id})
        tempwoolongs = level["woolongs"]

        spike = ranking.find_one({"id" : "self.client.user.id", "guild id" : guild.id})

        left = spike["woolongs"]+tempwoolongs

        spike = ranking.update_one({"id": "self.client.user.id", "guild id" : member.guild.id}, {"$set" : {"woolongs" : left}})        

        ranking.delete_one(level)

        try:
            goodbye = msg_channel.find_one({"guild id" : guild.id, "name" : "goodbye"})
            tempid = goodbye["channel id"]
            goodbyechannel = await self.client.fetch_channel(tempid)
            try:
                channel = msg.find_one({"guild id" : guild.id, "name" : "lmsg"})
                temp = channel["message"]
                await welcomechannel.send(f"{temp}")
            except:    
                await goodbyechannel.send(f"**{member.display_name}** just left the server.")
        except Exception as e:
            pass

    @commands.hybrid_command(name = "greeting", with_app_command = True, description = "Sets the welcome message for the channel")
    @commands.has_permissions(kick_members = True)
    async def greeting(self, ctx, *, message):
        try:
            check = msg.find_one({"guild id" : ctx.guild.id, "name" : "greeting"})
            if check is None:
                welcome_message = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "greeting", "message": message}
                await ctx.reply("Welcome message has been set!", ephemeral = False)
            else:
                msg.update_one({"guild id" : ctx.guild.id, "name" : "greeting"}, {"$set" : {"message" : message}})
                await ctx.reply("Welcome message has been updated!", ephemeral = False)
        except:
            await ctx.reply("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "leaving", with_app_command = True, description = "Sets the leaving message for the channel")
    @commands.has_permissions(kick_members = True)
    async def leaving(self, ctx, *, message):
        try:
            check = msg.find_one({"guild id" : ctx.guild.id, "name" : "leaving"})
            if check is None:
                leaving_message = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "leaving", "message": message}
                await ctx.reply("Leaving message has been set!", ephemeral = False)
            else:
                msg.update_one({"guild id" : ctx.guild.id, "name" : "leaving"}, {"$set" : {"message" : message}})
                await ctx.reply("Leaving message has been updated!", ephemeral = False)
        except:
            await ctx.reply("You can't do that!", ephemeral = False)

async def setup(client):
    await client.add_cog(ChannelMessages(client))