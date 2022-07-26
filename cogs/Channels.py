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
        check = set_channel.find_one({"guild id":ctx.guild.id, "name":"Welcome"})
        if check is None:    
            welcome={"guild name":ctx.guild.name, "guild id":ctx.guild.id, "name":"Welcome", "channel name":channel.name, "channel id":channel.id}
            set_channel.insert_one(welcome)
            await ctx.reply(f"Welcome Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def goodbye(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"guild id":ctx.guild.id, "name":"Goodbye"})
        if check is None:
            goodbye={"guild name":ctx.guild.name, "guild id":ctx.guild.id, "name":"Goodbye", "channel name":channel.name, "channel id":channel.id}
            set_channel.insert_one(goodbye)
            await ctx.reply(f"Goodbye Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def moderation(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"guild id":ctx.guild.id, "name":"Moderation"})
        if check is None:
            logging={"guild name":ctx.guild.name, "guild id":ctx.guild.id, "name":"Moderation", "channel name":channel.name, "channel id":channel.id}
            set_channel.insert_one(logging)
            await ctx.reply(f"Moderation logging Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def chatlog(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"guild id":ctx.guild.id, "name":"Chat Log"})
        if check is None:
            chatlog={"guild name":ctx.guild.name, "guild id":ctx.guild.id, "name":"Chat Log", "channel name":channel.name, "channel id":channel.id}
            set_channel.insert_one(chatlog)
            await ctx.reply(f"Chat Log Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ghostping(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"guild id":ctx.guild.id, "name":"Ghost Ping"})
        if check is None:
            ghostping={"guild name":ctx.guild.name, "guild id":ctx.guild.id, "name":"Ghost Ping", "channel name":channel.name, "channel id":channel.id}
            set_channel.insert_one(ghostping)
            await ctx.reply(f"Ghostping Channel has been set to {channel.mention}!")
        else:
            await ctx.reply("Channel has already been set!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def rank(self, ctx, channel:discord.TextChannel):
        check = set_channel.find_one({"guild id":ctx.guild.id, "name":"Rank"})
        if check is None:    
            rank={"guild name":ctx.guild.name, "guild id":ctx.guild.id, "name":"Rank", "channel name":channel.name, "channel id":channel.id}
            set_channel.insert_one(rank)
            await ctx.reply(f"Rank Channel has been set to {channel.mention}!")
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