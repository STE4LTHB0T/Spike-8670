import discord
from discord.ext import commands
from pytz import timezone


class Embeds(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Embeds is loaded!')

  @commands.command()
  async def invite(self,ctx):
    invite=discord.Embed(title="Invite!",description="Owner: **[STE4LTH_B0T#3622](https://discordapp.com/users/463780399437447200)**",color=discord.Color.red())
    invite.add_field(name="Invite Link",value="Click [here](https://discord.com/api/oauth2/authorize?client_id=804347400004173864&permissions=2352147526&scope=bot) to invite the bot to your server!",inline=False)
    invite.add_field(name="Github Repo",value="Click [here](https://github.com/STE4LTHB0T/Spike-8670) to visit the bot's repo!",inline=False)
    invite.set_thumbnail(url=self.client.user.avatar_url)
    await ctx.reply(embed=invite)

  @commands.command()
  async def id(self, ctx, member : discord.Member=None):
    if member is None:
      member=ctx.author
      
    join_time = member.joined_at
    joined_time = join_time.astimezone(timezone('Asia/Kolkata'))

    create_time = member.created_at
    created_time= create_time.astimezone(timezone('Asia/Kolkata'))
    
    data = discord.Embed(title = f"{member.name}#{member.discriminator}", description = f"Info about {member.mention}", color=member.top_role.colour)
    data.add_field(name = "User ID", value = member.id, inline = False)
    data.add_field(name="Top Role", value=member.top_role.mention, inline=False)
    data.add_field(name= "Created at", value=created_time.strftime("%d/%m/%Y %H:%M IST"), inline= False)
    data.add_field(name="Joined at", value= joined_time.strftime("%d/%m/%Y %H:%M IST"), inline=False)
    data.add_field(name="Nickname", value=member.nick, inline=False)
    data.set_thumbnail(url = member.avatar_url)
    data.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.reply(embed=data)

  @commands.command()
  async def records(self,ctx):
    guild_time = ctx.message.guild.created_at
    guild_created_time= guild_time.astimezone(timezone('Asia/Kolkata'))

    records= discord.Embed(title=f"{ctx.guild.name} Server Information", colour=ctx.guild.owner.colour)
    records.set_thumbnail(url=ctx.guild.icon_url)
    records.add_field(name="Inter-Solar System Police Head", value=ctx.guild.owner.mention, inline=False)
    records.add_field(name="Planet ID", value=ctx.guild.id, inline=False)
    records.add_field(name="Created at", value=guild_created_time.strftime("%d/%m/%Y %H:%M Post Gateway Accident"), inline=False)
    records.add_field(name="Bounty Roles", value=len(ctx.guild.roles), inline=False)
    records.add_field(name="Available Bounties", value=len(list(filter(lambda m: not m.bot, ctx.guild.members))), inline=False)
    records.add_field(name="Bounty News Announcers", value=len(list(filter(lambda m: m.bot, ctx.guild.members))), inline=False)
    records.add_field(name="Bounty News Information", value=len(ctx.guild.text_channels), inline=False)
    records.add_field(name="Bounty News Help", value=len(ctx.guild.voice_channels), inline=False)
    records.set_footer(icon_url = ctx.author.avatar_url, text = f"Informations for {ctx.author.name}#{ctx.author.discriminator}")
    await ctx.reply(embed=records)


def setup(client):
  client.add_cog(Embeds(client))