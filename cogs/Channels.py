import discord, os
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ['MONGO'])

set_channel = cluster["discord"]["channels"]

class Channels(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Channels is loaded!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def welcome(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"_id":"Welcome", "guild id":ctx.guild.id})
        if check is None:    
            welcome={"_id":"Welcome", "guild name":ctx.guild.name, "guild id":ctx.guild.id, "channel id":channel.id}
            set_channel.insert_one(welcome)
            await ctx.reply(f"Welcome Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def goodbye(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"_id":"Goodbye", "guild id":ctx.guild.id})
        if check is None:
            goodbye={"_id":"Goodbye", "guild name":ctx.guild.name, "guild id":ctx.guild.id, "channel id":channel.id}
            set_channel.insert_one(goodbye)
            await ctx.reply(f"Goodbye Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def moderation(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"_id":"Moderation", "guild id":ctx.guild.id})
        if check is None:
            logging={"_id":"Moderation", "guild name":ctx.guild.name, "guild id":ctx.guild.id, "channel id":channel.id}
            set_channel.insert_one(logging)
            await ctx.reply(f"Logging Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def chatlog(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"_id":"Chatlog", "guild id":ctx.guild.id})
        if check is None:
            chatlog={"_id":"Chatlog", "guild name":ctx.guild.name, "guild id":ctx.guild.id, "channel id":channel.id}
            set_channel.insert_one(chatlog)
            await ctx.reply(f"Chat Log Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ghostping(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"_id":"Ghost Ping", "guild id":ctx.guild.id})
        if check is None:
            ghostping={"_id":"Ghost Ping", "guild name":ctx.guild.name, "guild id":ctx.guild.id, "channel id":channel.id}
            set_channel.insert_one(ghostping)
            await ctx.reply(f"Ghostping Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def removechannel(self, ctx, channel:discord.TextChannel):
        remove={"guild id":ctx.guild.id, "channel id":channel.id}
        set_channel.delete_one(remove)
        await ctx.reply(f"{channel.mention} Channel has been removed!")

def setup(client):
  client.add_cog(Channels(client))