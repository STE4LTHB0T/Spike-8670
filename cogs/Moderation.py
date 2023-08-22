import discord, asyncio, random, os, datetime, logging
import humanfriendly
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from pymongo import MongoClient
from resources.Lists import *

cluster = MongoClient(os.environ["MONGO"])

msg_channel = cluster["discord"]["channels"]

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ["s", "m", "h", "d"]:
            return (int(amount), unit)

        raise commands.BadArgument(message = "Not a valid duration!")

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation is loaded!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.author.bot:
            return
        try:
            message_link = message.jump_url

            chatlog = discord.Embed(title = "Chat Log", color = 0xff0000)
            chatlog.add_field(name = "User", value = f"{message.author.mention}", inline = True)
            chatlog.add_field(name = "Channel", value = f"{message.channel.mention}", inline = True)
            chatlog.add_field(name = "Message Link", value = f"[Jump to message]({message_link})", inline = True)
            chatlog.add_field(name = "Message",value = f"{message.content}", inline = False)
            chatlog.set_thumbnail(url = message.author.avatar.url)
            try:
                if len(message.attachments)>0:
                    chatlog.set_image(url = message.attachments[0].url)
            except:
                pass
        
            chat = msg_channel.find_one({"guild id" : message.guild.id, "name" : "chatlog"})
            tempid = chat["channel id"]
            chatchannel = await self.client.fetch_channel(tempid)
        
            await chatchannel.send(embed = chatlog)
        except:
            pass

    @commands.hybrid_command(name = "setup", with_app_command = True, description = "Gives the instruction for the setup of the bot")
    async def setup(self, ctx):
        mod = discord.Embed(title = "Prepping the server for the bot", color = 0xff0000)
        mod.add_field(name = "Welcome", value = "To welcome new members, do `spike welcome [Mention channel]`", inline = False)
        mod.add_field(name = "Goodbye", value = "To send off leaving members, do `spike goodbye [Mention channel]`", inline = False)
        mod.add_field(name = "Log Channel",value = "To log moderation, do `spike moderation [Mention channel]`", inline = False)
        mod.add_field(name = "Chat Logs", value = "To log chats, do `spike chatlog [Mention channel]`", inline = False)
        mod.add_field(name = "Ghost Pings", value = "To detect and log ghost-pings, do `spike ghostping [Mention channel]`", inline = False)
        mod.add_field(name = "Rank", value = "To log ranks of a member, do `spike rank [Mention channel]`", inline = False)
        mod.add_field(name = "Remove a channel", value = "To remove a channel from the database, do `spike removechannel [command]`",inline = False)
        await ctx.reply(embed = mod, ephemeral = False)

    @commands.hybrid_command(name = "clear", with_app_command = True, description = "Clears the number of messages specified")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, number):
        number = int(number)
        await ctx.channel.purge(limit = number + 1)
        await ctx.send("Cleared!", delete_after = 5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "kick", with_app_command = True, description = "Kicks a member of the server")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member = None, *, reason = None):
        if member is None:
            return await ctx.reply("Time to yeet somebody!<:FeelsEvilMan:477783012428349441>", ephemeral = False)
        if member is ctx.author:
            return await ctx.reply("You can't kick yourself!", ephemeral = False)

        await member.kick(reason = reason)
        kick = discord.Embed(title = "Kicked!", color = ctx.author.color)
        kick.add_field(name = "Moderator", value = f"{ctx.author.mention}", inline = True)
        kick.add_field(name = "Member", value = f"{member.mention}", inline = True)
        kick.add_field(name = "Reason", value = f"{reason}", inline = True)
        kick.set_thumbnail(url = member.avatar.url)
        await ctx.reply(embed = kick, ephemeral = False)
        try:
            await member.send(f"You've been banned from the {ctx.guild.name} server for the following reason: {reason}.")
        except Exception as e:
            pass
        try:
            mod = msg_channel.find_one({"guild id" : ctx.guild.id, "name" : "moderation"})
            tempid = mod["channel id"]
            modchannel = await self.client.fetch_channel(tempid)
            await modchannel.send(embed = kick)
        except Exception as e:
            pass

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You can't do that!", ephemeral = False)

    @commands.hybrid_command(name = "ban", with_app_command = True, description = "Bans a member of the server")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        if member is None:
            return await ctx.reply("Time to put the ban hammer on somebody!<:vadistyle:794639310062092308>", ephemeral = False)
        if member is ctx.author:
            return await ctx.reply("You can't ban yourself!", ephemeral = False)

        await member.ban(reason = reason)
        ban = discord.Embed(title = "Banned!", color = ctx.author.color)
        ban.add_field(name = "Moderator", value = f"{ctx.author.mention}", inline = True)
        ban.add_field(name = "Member", value = f"{member}", inline = True)
        ban.add_field(name = "Reason", value = f"{reason}", inline = True)
        ban.set_thumbnail(url = member.avatar.url)
        await ctx.reply(embed = ban, ephemeral = False)
        try:
            await member.send(f"You've been banned from the {ctx.guild.name} server for the following reason: {reason}.")
        except Exception as e:
            pass
        try:
            mod = msg_channel.find_one({"guild id" : ctx.guild.id, "name" : "moderation"})
            tempid = mod["channel id"]
            modchannel = await self.client.fetch_channel(tempid)
            await modchannel.send(embed = ban)
        except Exception as e:
            pass

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("There is a reason why there are moderators in servers<:vadiivanvera:771439425862893640>", ephemeral = False)

    @commands.hybrid_command(name = "unban", with_app_command = True, description = "Unbans a member")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, user):
            banned_members = ctx.guild.bans()
            async for ban_entry in banned_members:
                member = ban_entry.user
                try:
                    if (member.name) == (user) or (member.id) == (int(user)):
                        await ctx.guild.unban(member)
                        await ctx.reply(f"Unbanned {member.mention}!", ephemeral = False)
                        return
                except Exception as e:
                    await ctx.reply("Please check if all the details are correct!")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("https://media.giphy.com/media/USNlL9p2fxY6Q/giphy.gif", ephemeral = False)

    @commands.hybrid_command(name = "nickname", with_app_command = True, description = "Changes the nickname of the member")
    @commands.has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, member: discord.Member, *, nick):
        await member.edit(nick = nick)
        await ctx.send(f"You will be now called as {member.mention}!", ephemeral = False)

    @nickname.error
    async def nickname_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("You don't have the right to call anybody with other names!", ephemeral = False)

    @commands.hybrid_command(name = "mute", with_app_command = True, description = "Mutes a member of the server")
    @commands.has_permissions(mute_members = True)
    async def mute(self, ctx, member: discord.Member = None, *, reason = None):
        if member is None:
            await ctx.reply("Time to mute somebody!<:FeelsSmugMan:477783012172365864>")
            await ctx.send("https://tenor.com/view/boom-youre-all-muted-south-park-pandemic-special-s24e1-s24e2-gif-19438992")
        try:
            guild = ctx.guild
            muted_role = discord.utils.get(guild.roles, name = "Muted")
            await member.add_roles(muted_role)
            mute = discord.Embed(title = "Muted!", color = ctx.author.color)
            mute.add_field(name = "Moderator", value = f"{ctx.author.mention}", inline = True)
            mute.add_field(name = "Member", value=f"{member.mention}", inline = True)
            mute.add_field(name = "Reason", value=f"{reason}", inline = True)
            mute.set_thumbnail(url = member.avatar.url)
            await ctx.reply(embed = mute, ephemeral = False)
            try:
                mod = msg_channel.find_one({"guild id" : ctx.guild.id, "name" : "moderation"})
                tempid = mod["channel id"]
                modchannel = await self.client.fetch_channel(tempid)
                await modchannel.send(embed = mute)
            except Exception as e:
                pass
        except Exception as e:
            await ctx.reply("Muted role was not found in the server!", ephemeral = False)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("https://tenor.com/view/silent-silence-shh-quiet-loki-gif-5018528", ephemeral = False)

    @commands.hybrid_command(name = "unmute", with_app_command = True, description = "Unmutes a muted member of the server")
    @commands.has_permissions(mute_members = True)
    async def unmute(self, ctx, member : discord.Member):

        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name = "Muted")
        await member.remove_roles(muted_role)
        umute = discord.Embed(title = "Unmuted!", color = ctx.author.color)
        umute.add_field(name = "Moderator", value = f"{ctx.author.mention}", inline = True)
        umute.add_field(name = "Member", value = f"{member.mention}", inline = True)
        umute.set_thumbnail(url = member.avatar.url)
        await ctx.reply(embed = umute, ephemeral = False)
        try:
            mod = msg_channel.find_one({"guild id" : ctx.guild.id, "name" : "moderation"})
            tempid = mod["channel id"]
            modchannel = await self.client.fetch_channel(tempid)
            await modchannel.send(embed = umute)
        except Exception as e:
            pass 

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("https://tenor.com/view/silent-silence-shh-quiet-loki-gif-5018528", ephemeral = False)

    @commands.hybrid_command(mname = "timeout", with_app_command = True, description = "Times out a member of the server")
    @commands.has_permissions(mute_members = True)
    async def timeout(self, ctx, member : discord.Member = None, time = None, * , reason = None):
        timeout_time = humanfriendly.parse_timespan(time)
        to = discord.utils.utcnow() + datetime.timedelta(seconds=timeout_time)
        await member.timeout(to, reason = reason)

        timed_out = discord.Embed(title = "Timeout!", color = ctx.author.color)
        timed_out.add_field(name = "Moderator", value = f"{ctx.author.mention}", inline = True)
        timed_out.add_field(name = "Member", value = f"{member.mention}", inline = True)
        timed_out.add_field(name = "Duration", value = f"{time}", inline = True)
        timed_out.add_field(name = "Reason", value = f"{reason}", inline = True)
        timed_out.set_thumbnail(url = member.avatar.url)
        await ctx.reply(embed = timed_out, ephemeral = False)
        try:
            mod = msg_channel.find_one({"guild id" : ctx.guild.id, "name" : "moderation"})
            tempid = mod["channel id"]
            modchannel = await self.client.fetch_channel(tempid)
            await modchannel.send(embed = timed_out)
        except Exception as e:
            pass
        
    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("https://tenor.com/view/silent-silence-shh-quiet-loki-gif-5018528", ephemeral = False)

    @commands.hybrid_command(mname = "remove timeout", with_app_command = True, description = "Removes the timeout of a member of the server")
    @commands.has_permissions(kick_members = True)
    async def removetimeout(self, ctx, member : discord.Member):
        await member.timeout(None)

        remove_timed_out = discord.Embed(title = "Removed Timeout!", color = ctx.author.color)
        remove_timed_out.add_field(name = "Moderator", value = f"{ctx.author.mention}", inline = True)
        remove_timed_out.add_field(name = "Member", value = f"{member.mention}", inline = True)
        remove_timed_out.set_thumbnail(url = member.avatar.url)
        await ctx.reply(embed = remove_timed_out, ephemeral = False)
        try:
            mod = msg_channel.find_one({"guild id" : ctx.guild.id, "name" : "moderation"})
            tempid = mod["channel id"]
            modchannel = await self.client.fetch_channel(tempid)
            await modchannel.send(embed = remove_timed_out)
        except Exception as e:
            pass

    @removetimeout.error
    async def removetimeout_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply("https://tenor.com/view/silent-silence-shh-quiet-loki-gif-5018528", ephemeral = False)

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        try:
            synced = await self.client.tree.sync()
            await ctx.reply(f"Synced {len(synced)} commands")
        except Exception as e:
            await ctx.reply(e)

    @commands.command()
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.client.get_command(command)

        if command is None:
            await ctx.send("Rule not found!")

        elif ctx.command == command:
            await ctx.send("You cannot disable this rule.")

        else:
            command.enabled = not command.enabled
            status = "enabled" if command.enabled else "disabled"
            await ctx.send(f"`{command.qualified_name}` has been {status}.")

async def setup(client):
    await client.add_cog(Moderation(client))