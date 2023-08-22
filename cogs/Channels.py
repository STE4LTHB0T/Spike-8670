import discord, os, logging
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from pymongo import MongoClient

cluster = MongoClient(os.environ["MONGO"])

set_channel = cluster["discord"]["channels"]

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class Channels(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Channels is loaded!')

    @commands.hybrid_command(name = "welcome", with_app_command = True, description = "Sets the welcome channel")
    @commands.has_permissions(kick_members = True)
    async def welcome(self, ctx, channel : discord.TextChannel):
        check = set_channel.find_one({"guild id" : ctx.guild.id, "name" : "welcome"})
        if check is None:    
            welcome = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "welcome", "channel name" : channel.name, "channel id" : channel.id}
            set_channel.insert_one(welcome)
            await ctx.reply(f"Welcome Channel has been set to {channel.mention}!", ephemeral = False)
        else:
            await ctx.reply("Channel has already been set!", ephemeral = False)
    
    @welcome.error
    async def welcome_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "goodbye", with_app_command = True, description = "Sets the goodbye channel")
    @commands.has_permissions(kick_members = True)
    async def goodbye(self, ctx, channel : discord.TextChannel):
        check = set_channel.find_one({"guild id" : ctx.guild.id, "name" : "goodbye"})
        if check is None:
            goodbye = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "goodbye", "channel name" : channel.name, "channel id" : channel.id}
            set_channel.insert_one(goodbye)
            await ctx.reply(f"Goodbye Channel has been set to {channel.mention}!", ephemeral = False)
        else:
            await ctx.reply("Channel has already been set!", ephemeral = False)

    @goodbye.error
    async def goodbye_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "moderation", with_app_command = True, description = "Sets the moderation channel")
    @commands.has_permissions(kick_members = True)
    async def moderation(self, ctx, channel : discord.TextChannel):
        check = set_channel.find_one({"guild id" : ctx.guild.id, "name" : "moderation"})
        if check is None:
            logging = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "moderation", "channel name" : channel.name, "channel id" : channel.id}
            set_channel.insert_one(logging)
            await ctx.reply(f"Moderation logging Channel has been set to {channel.mention}!", ephemeral = False)
        else:
            await ctx.reply("Channel has already been set!", ephemeral = False)

    @moderation.error
    async def moderation_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "chatlog", with_app_command = True, description = "Sets the chatlog channel")
    @commands.has_permissions(kick_members = True)
    async def chatlog(self, ctx, channel : discord.TextChannel):
        check = set_channel.find_one({"guild id" : ctx.guild.id, "name" : "chatlog"})
        if check is None:
            chatlog = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "chatlog", "channel name" : channel.name, "channel id" : channel.id}
            set_channel.insert_one(chatlog)
            await ctx.reply(f"Chat Log Channel has been set to {channel.mention}!", ephemeral = False)
        else:
            await ctx.reply("Channel has already been set!", ephemeral = False)

    @chatlog.error
    async def chatlog_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "ghostping", with_app_command = True, description = "Sets the ghostping channel")
    @commands.has_permissions(kick_members = True)
    async def ghostping(self, ctx, channel : discord.TextChannel):
        check = set_channel.find_one({"guild id" : ctx.guild.id, "name" : "ghostping"})
        if check is None:
            ghostping = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "ghostping", "channel name" : channel.name, "channel id" : channel.id}
            set_channel.insert_one(ghostping)
            await ctx.reply(f"Ghostping Channel has been set to {channel.mention}!", ephemeral = False)
        else:
            await ctx.reply("Channel has already been set!", ephemeral = False)

    @ghostping.error
    async def ghostping_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "rank", with_app_command = True, description = "Sets the rank channel")
    @commands.has_permissions(kick_members = True)
    async def rank(self, ctx, channel : discord.TextChannel):
        check = set_channel.find_one({"guild id" : ctx.guild.id, "name" : "rank"})
        if check is None:    
            rank = {"guild name" : ctx.guild.name, "guild id" : ctx.guild.id, "name" : "rank", "channel name" : channel.name, "channel id" : channel.id}
            set_channel.insert_one(rank)
            await ctx.reply(f"Rank Channel has been set to {channel.mention}!", ephemeral = False)
        else:
            await ctx.reply("Channel has already been set!", ephemeral = False)

    @rank.error
    async def rank_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "removechannel", with_app_command = True, description = "Removes the mentioned channel")
    @commands.has_permissions(kick_members = True)
    async def removechannel(self, ctx, name : str):
        try:
            remove = {"guild id" : ctx.guild.id, "name" : name}
            set_channel.delete_one(remove)
            await ctx.reply(f"`{name}` Channel has been removed!", ephemeral = False)
        except Exception as e:
            await ctx.reply("An error occurred! Please check the usage of the command", ephemeral = False)

    @removechannel.error
    async def removechannel_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

async def setup(client):
    await client.add_cog(Channels(client))