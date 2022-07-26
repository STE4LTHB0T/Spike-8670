import discord, asyncio, random, os
from cogs.Bounty import spam_channels
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from main import is_it_trustees, is_it_me
from pymongo import MongoClient
from resources.Lists import *

cluster = MongoClient(os.environ['MONGO'])

msg_channel = cluster["discord"]["channels"]

class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
            return (int(amount), unit)

        raise commands.BadArgument(message="Not a valid duration!")


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation is loaded!')

    @commands.Cog.listener()
    async def on_message(self,message):
      if message.author == self.client.user:
        return
      if message.author.bot:
        return
      if message.channel.id in spam_channels:
        return

      try:
        chatlog=discord.Embed(title="Chat Log")
        chatlog.add_field(name="User", value=f"{message.author.mention}")
        chatlog.add_field(name="Channel", value=f"{message.channel.mention}")
        chatlog.add_field(name="Message",value=f"{message.content}")
        chatlog.set_thumbnail(url=message.author.avatar_url)
        
        chat=msg_channel.find_one({"guild id":message.guild.id, "name":"Chat Log"})
        tempid=chat["channel id"]
        chatchannel = await self.client.fetch_channel(tempid)
        
        await chatchannel.send(embed=chatlog)

      except Exception as e:
        print(e)
    
    @commands.command()
    async def setup(self, ctx):
      mod = discord.Embed(title="Prepping the server for the bot.",color=discord.Color.red())
      mod.add_field(name="Welcome",value="To welcome new members, do `spike welcome [Mention channel]`",inline=False)
      mod.add_field(name="Goodbye",value="To send off leaving members, do `spike goodbye [Mention channel]`",inline=False)
      mod.add_field(name="Log Channel",value="To log moderation, do `spike moderation [Mention channel]`",inline=False)
      mod.add_field(name="Chat Logs", value="To log chats, do `spike chatlog [Mention channel]`",inline=False)
      mod.add_field(name="Ghost Pings",value="To detect and log ghost-pings, do `spike ghostping [Mention channel]`",inline=False)
      mod.add_field(name="Rank",value="To log ranks of a member, do `spike rank [Mention channel]`",inline=False)
      mod.add_field(name="Remove a channel",value="To remove a channel from the database, do `spike removechannel [Mention channel]`",inline=False)
      await ctx.reply(embed=mod)


    @commands.command()
    @commands.check(is_it_trustees)
    async def addto(self,ctx,variable_name:str,itemtoAdd:str):
      if variable_name in defined_lists:
        if variable_name == 'bannedwords'and variable_name not in bannedwords:
          bannedwords.append(itemtoAdd)
          await ctx.send('Swear added')
        elif variable_name == 'welcome' and variable_name not in welcome_reply:
          welcome_reply.append(itemtoAdd)
          await ctx.send('GIF added')
        else:
          await ctx.send('Invalid Variable Name to modify')
      else:
        await ctx.send('Error')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, number):
        number = int(number)
        await ctx.channel.purge(limit=number + 1)
        await ctx.send('Cleared!', delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send('LMAO, you cant do that bruh!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            return await ctx.reply(
                "Time to yeet somebody!<:FeelsEvilMan:477783012428349441>")
        if member is ctx.author:
            return await ctx.reply("You can't kick yourself!")

        await member.send(
            f"You've been kicked from the {ctx.guild.name} server for the following reason: {reason}."
        )
        await member.kick(reason=reason)
        kick = discord.Embed(title="Kicked!", color=ctx.author.color)
        kick.add_field(name="Moderator",
                       value=f"{ctx.author.mention}",
                       inline=True)
        kick.add_field(name="Member", value=f"{member.mention}", inline=True)
        kick.add_field(name="Reason", value=f"{reason}", inline=True)
        kick.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=kick)
        try:
          mod=msg_channel.find_one({"guild id":ctx.guild.id, "name":"Moderation"})
          tempid=mod["channel id"]
          modchannel = await self.client.fetch_channel(tempid)
          await modchannel.send(embed=kick)
        except Exception as e:
          print(e)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                'Ever heard of admin powers?<:FeelsThinkMan:477783009651851284>')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            return await ctx.reply(
                "Time to put the ban hammer on somebody!<:vadistyle:794639310062092308>"
            )
        if member is ctx.author:
            return await ctx.reply("You can't ban yourself!")

        await member.send(
            f"You've been banned from the {ctx.guild.name} server for the following reason: {reason}."
        )
        await member.ban(reason=reason)
        ban = discord.Embed(title="Banned!", color=ctx.author.color)
        ban.add_field(name="Moderator",
                      value=f"{ctx.author.mention}",
                      inline=True)
        ban.add_field(name="Member", value=f"{member}", inline=True)
        ban.add_field(name="Reason", value=f"{reason}", inline=True)
        ban.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=ban)
        try:
          mod=msg_channel.find_one({"guild id":ctx.guild.id, "name":"Moderation"})
          tempid=mod["channel id"]
          modchannel = await self.client.fetch_channel(tempid)
          await modchannel.send(embed=ban)
        except Exception as e:
          print(e)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                "There is a reason why moderators are there in servers<:vadiivanvera:771439425862893640>"
            )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name,
                                                   member_discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(f'Unbanned{user.mention}!')
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                "https://media.giphy.com/media/USNlL9p2fxY6Q/giphy.gif")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def nickname(self, ctx, member: discord.Member, *, nick):
        await member.edit(nick=nick)
        reply = random.randint(0,1)
        if reply == 0:
          await ctx.send(f'Indru mudhal nee {member.mention} endru alaikkpaduveer!')
        else:
          await ctx.send(f'Ne ellam porandhadhey saaba kedu, idhula {member.mention} nu peru onnuh dhan kedu!')
  
    @commands.command()
    async def mutepass(self,ctx, member:discord.Member = None, *, reason=None):
        if member is None:
            await ctx.send("Time to flex my power")
        if reason is None:
            reason="with great power, comes great responsibility."
        tm= discord.utils.get(ctx.guild.roles, name="The Mute Pass")
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if tm in ctx.author.roles:
            await member.add_roles(muted_role)
            await ctx.reply(f"{ctx.author.mention} muted {member.mention} using {tm.mention} because {reason}")
        else:
            await ctx.reply("Try getting a pass!")
        await ctx.author.remove_roles(tm)    

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.reply(
                "Time to mute somebody!<:FeelsSmugMan:477783012172365864>")
            await ctx.send(
                "https://tenor.com/view/boom-youre-all-muted-south-park-pandemic-special-s24e1-s24e2-gif-19438992"
            )

        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")
        await member.add_roles(muted_role)
        mute = discord.Embed(title="Muted!", color=ctx.author.color)
        mute.add_field(name="Moderator",
                       value=f"{ctx.author.mention}",
                       inline=True)
        mute.add_field(name="Member", value=f"{member.mention}", inline=True)
        mute.add_field(name="Reason", value=f'{reason}', inline=True)
        mute.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=mute)
        try:
          mod=msg_channel.find_one({"guild id":ctx.guild.id, "name":"Moderation"})
          tempid=mod["channel id"]
          modchannel = await self.client.fetch_channel(tempid)
          await modchannel.send(embed=mute)
        except Exception as e:
          print(e)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(
                "https://tenor.com/view/silent-silence-shh-quiet-loki-gif-5018528"
            )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):

        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        umute = discord.Embed(title="Unmuted!", color=ctx.author.color)
        umute.add_field(name="Moderator",
                        value=f"{ctx.author.mention}",
                        inline=True)
        umute.add_field(name="Member", value=f"{member.mention}", inline=True)
        umute.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=umute)
        try:
          mod=msg_channel.find_one({"guild id":ctx.guild.id, "name":"Moderation"})
          tempid=mod["channel id"]
          modchannel = await self.client.fetch_channel(tempid)
          await modchannel.send(embed=umute)
        except Exception as e:
          print(e)

    @commands.command()
    async def tempmutepass(self, ctx, member: discord.Member,
                       duration: DurationConverter):
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        amount, unit = duration
        if member is None:
            await ctx.send("Time to flex my powers!")
        tm= discord.utils.get(ctx.guild.roles, name="The Mute Pass")
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if tm in ctx.author.roles:
            await member.add_roles(muted_role)
            await ctx.author.remove_roles(tm)
            await ctx.reply(f"{ctx.author.mention} muted {member.mention} using {tm.mention} for {amount}{unit}!")
            await asyncio.sleep(amount * multiplier[unit])
            await member.remove_roles(muted_role)
        else:
            await ctx.reply("Try getting a pass!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def tempmute(self, ctx, member: discord.Member,
                       duration: DurationConverter):
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        amount, unit = duration
        if member is None:
            await ctx.reply(
                "Time for somebody to shut up!<:FeelsSpicyMan:915265533597855834>")        

        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")
        await member.add_roles(muted_role)
        tmute = discord.Embed(title="Temporary Mute!", color=ctx.author.color)
        tmute.add_field(name="Moderator",
                        value=f"{ctx.author.mention}",
                        inline=True)
        tmute.add_field(name="Member", value=f"{member.mention}", inline=True)
        tmute.add_field(name="Duration", value=f'{amount}{unit}', inline=True)
        tmute.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=tmute)
        try:
          mod=msg_channel.find_one({"guild id":ctx.guild.id, "name":"Moderation"})
          tempid=mod["channel id"]
          modchannel = await self.client.fetch_channel(tempid)
          await modchannel.send(embed=tmute)
        except Exception as e:
          print(e)

        await asyncio.sleep(amount * multiplier[unit])
        await member.remove_roles(muted_role)

        utmute = discord.Embed(
            description=f'{member.mention} has been unmuted',
            color=ctx.author.color)
        await ctx.reply(embed=utmute)
        try:
          mod=msg_channel.find_one({"guild id":ctx.guild.id, "name":"Moderation"})
          tempid=mod["channel id"]
          modchannel = await self.client.fetch_channel(tempid)
          await modchannel.send(embed=utmute)
        except Exception as e:
          print(e)

    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                "https://tenor.com/view/zoom-call-wfh-work-from-home-mute-gif-17949615")

    @commands.command()
    @commands.check_any(commands.check(is_it_me), commands.has_permissions(administrator=True))
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
                
                
def setup(client):
    client.add_cog(Moderation(client))