import discord, asyncio, random
from cogs.Bounty import spam_channels
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from main import is_it_trustees
from resources.Lists import *


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
        guild = message.guild
        chat_logchannel= discord.utils.get(guild.text_channels, name="chat-logs")
        chatlog=discord.Embed(title="Chat Log")
        chatlog.add_field(name="User:", value=f"{message.author.mention}")
        chatlog.add_field(name="Channel", value=f"{message.channel.mention}")
        chatlog.add_field(name="Message",value=f"{message.content}")
        chatlog.set_thumbnail(url=message.author.avatar_url)
        await chat_logchannel.send(embed=chatlog)

      except:
        pass
    
    @commands.command()
    @commands.check(is_it_trustees)
    async def setup(self, ctx):
      mod = discord.Embed(title="Prepping the server for the bot.",color=discord.Color.red())
      mod.add_field(name="Welcome",value="To welcome new members, create a channel named `👋🏽︱welcome`",inline=False)
      mod.add_field(name="Goodbye",value="To send off leaving members, create a channel named `goodbye-👋🏽`",inline=False)
      mod.add_field(name="Log Channel",value="To log moderation, create a channel named `log-channel`",inline=False)
      mod.add_field(name="Chat Logs", value="To log chats, create a channel named `chat-logs`")
      mod.add_field(name="Ghost Pings",value="To detect and log ghost-pings, create a channel named `ghost-ping`",inline=False)
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
                "Time to yeet somebody!<:evilpepe:477783012428349441>")
        if member is ctx.author:
            return await ctx.reply("You can't kick yourself!")
        guild = ctx.guild
        log_channel = discord.utils.get(guild.text_channels,
                                        name="log-channel")
        await member.send(
            f"You've been kicked from the {guild.name} for the following reason: {reason}."
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
        await log_channel.send(embed=kick)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                'Ever heard of admin powers?<:PepoThink:477783009651851284>')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            return await ctx.reply(
                "Time to put the ban hammer on somebody!<:vadistyle:794639310062092308>"
            )
        if member is ctx.author:
            return await ctx.reply("You can't ban yourself!")
        guild = ctx.guild
        log_channel = discord.utils.get(guild.text_channels,
                                        name="log-channel")
        await member.send(
            f"You've been banned from the {guild.name} for the following reason: {reason}."
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
        await log_channel.send(embed=ban)

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
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await ctx.reply(
                "Time to mute somebody!<:MingoPepe:502444849442586644>")
            await ctx.send(
                "https://tenor.com/view/boom-youre-all-muted-south-park-pandemic-special-s24e1-s24e2-gif-19438992"
            )

        guild = ctx.guild
        log_channel = discord.utils.get(guild.text_channels,
                                        name="log-channel")
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
        await log_channel.send(embed=mute)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(
                "https://tenor.com/view/silent-silence-shh-quiet-loki-gif-5018528"
            )

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):

        guild = ctx.guild
        log_channel = discord.utils.get(guild.text_channels,
                                        name="log-channel")
        muted_role = discord.utils.get(guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        umute = discord.Embed(title="Unmuted!", color=ctx.author.color)
        umute.add_field(name="Moderator",
                        value=f"{ctx.author.mention}",
                        inline=True)
        umute.add_field(name="Member", value=f"{member.mention}", inline=True)
        umute.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=umute)
        await log_channel.send(embed=umute)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def tempmute(self, ctx, member: discord.Member,
                       duration: DurationConverter):
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        amount, unit = duration
        if member is None:
            await ctx.reply(
                "Time for somebody to shut up!<:vadishhhh:794639608071585802>")        

        guild = ctx.guild
        log_channel = discord.utils.get(guild.text_channels,
                                        name="log-channel")
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
        await log_channel.send(embed=tmute)

        await asyncio.sleep(amount * multiplier[unit])
        await member.remove_roles(muted_role)

        utmute = discord.Embed(
            description=f'{member.mention} has been unmuted',
            color=ctx.author.color)
        await ctx.reply(embed=utmute)
        await log_channel.send(embed=utmute)

    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(
                "https://tenor.com/view/zoom-call-wfh-work-from-home-mute-gif-17949615"
            )


def setup(client):
    client.add_cog(Moderation(client))