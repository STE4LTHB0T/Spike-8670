import discord
from discord.ext import commands


class Help(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('Help is loaded!')

  @commands.group(invoke_without_command=True)
  async def help(self,ctx):
    helper = discord.Embed(title="Help",description="Oh well. Whatever happens, happens.\n\nUse `spike help command` to know more about a command.", color=discord.Color.red())
    helper.set_thumbnail(url=self.client.user.avatar_url)
    helper.add_field(name="Bot Owner",value="**STE4LTH_B0T#3622**",inline=False)
    helper.add_field(name="Bounty (Otaku Nadu Exclusive)",value="`board`,`bounty`",inline=False)
    helper.add_field(name="Moderation",value="`setup`, `ban`, `caseregister`, `cases`, `clear`, `deletecase`, `kick`, `mute`, `nickname`, `tempmute`",inline=False)
    helper.add_field(name="Music and Radio",value="`music`, `radio`",inline=False)
    helper.add_field(name="General Commands",value="`echo`, `google`, `invite`, `ping`, `poll`, `remind`",inline=False)
    helper.add_field(name="User-related Commands",value="`id`, `profiles`, `records`, `wanted`",inline=False)
    helper.add_field(name="Roleplay Commands",value="`arrest`",inline=False)
    await ctx.reply(embed=helper)
  
  @help.command(aliases=["board!"])
  async def board(self,ctx):
    board= discord.Embed(title="Help - Board", description="`spike board` shows you who is the top dawg...\n\nI mean the Leaderboard of the Planet!",color=discord.Color.red())
    board.set_thumbnail(url=self.client.user.avatar_url)
    await ctx.reply(embed=board)

  @help.command(aliases=["bounty!"])
  async def bounty(self,ctx):
    bounty= discord.Embed(title="Help - Bounty", description="`spike bounty` tells you about your place in the Planet's Bounty heirarchy and how much you're prioritized!\n\nMake sure to rise up the ranks to unlock more perks.",color=discord.Color.red())
    bounty.set_thumbnail(url=self.client.user.avatar_url)
    await ctx.reply(embed=bounty)
  
  @help.command(aliases=["setup!"])
  async def setup(self, ctx):
      mod = discord.Embed(title="Help - Setup",description="The command gives Pre-requisites to set up the bot for Moderators and Planet Maintainers.\n\nThe command can only be invoked by people who have the necessary permissions",color=discord.Color.red())
      mod.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=mod)

  @help.command(aliases=["ban!"])
  async def ban(self, ctx):
      ban = discord.Embed(title="Help - Ban",description="`spike ban [@User]` strikes the hammer on anyone the Mods deem exilable from the Planet.\n\nWith great power comes great responsibility. Refrain from using it in uncalled for situations!",color=discord.Color.red())
      ban.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=ban)

  @help.command(aliases=["caseregister!"])
  async def caseregister(self,ctx):
      cr = discord.Embed(title="Help - Case Registration", description ="`spike caseregister [@User]/spike cr [@User]` registers a case on any Citizen and places a bounty on them", color=discord.Color.red())
      cr.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=cr)

  @help.command(aliases=["cases!"])
  async def cases(self,ctx):
      case = discord.Embed(title="Help - Cases", description ="`spike cases [@User]` pulls out the deck of cases on the Citizen", color=discord.Color.red())
      case.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=case)

  @help.command(aliases=["deletecase!"])
  async def deletecase(self,ctx):
      dc = discord.Embed(title="Help - Case Closing", description ="`spike deletecase [ID]/spike dc [@User]` closes the case on the Citizen when the Bounty is claimed.", color=discord.Color.red())
      dc.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=dc)

  @help.command(aliases=["clear!"])
  async def clear(self, ctx):
      clear = discord.Embed(title="Help - Clear",description="`spike clear [Amount]` clears a number of messages in the Channel as asked for.\n\nWith great power comes great responsibility. Refrain from using it in uncalled for situations!",color=discord.Color.red())
      clear.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=clear)

  @help.command(aliases=["kick!"])
  async def kick(self, ctx):
      kick = discord.Embed(title="Help - Kick",description="`spike kick [@User]` yeets the Citizen deemed unworthy of staying in the Planet.\n\nWith great power comes great responsibility. Refrain from using it in uncalled for situations!",color=discord.Color.red())
      kick.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=kick)

  @help.command(aliases=["mute!"])
  async def mute(self, ctx):
      mute = discord.Embed(title="Help - Mute",description="`spike mute [@User]` strips the right to speech of a Citizen in the Planet until further notice.\n\nWith great power comes great responsibility. Refrain from using it in uncalled for situations!",color=discord.Color.red())
      mute.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=mute)
  
  @help.command(aliases=["nickname!"])
  async def nickname(self, ctx):
      nickname = discord.Embed(title="Help - Nickname",description="`spike nickname [@User]` changes the nickname of a Citizen in the Planet.\n\nCitizens are warned that people up the heirarchy might play around with it, as long as shits and giggles, It will be tolerated. Citizens are asked to keep people who missuse the power maliciously in check!",color=discord.Color.red())
      nickname.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=nickname)

  @help.command(aliases=["tempmute!"])
  async def tempmute(self, ctx):
      tempmute = discord.Embed(title="Help - Temporary Mute",description="`spike tempmute [@User] [Time]` strips the right to speech of a Citizen in the Planet until the stipulated time mentioned strikes.\n\nWith great power comes great responsibility. Refrain from using it in uncalled for situations!",color=discord.Color.red())
      tempmute.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=tempmute)

  @help.command(aliases=["music!"])
  async def music(self, ctx):
      music = discord.Embed(title="Help - Music 🎵", description="Music commands (YouTube searches only)", color=discord.Color.red())
      music.add_field(name="🔗Join",value="Joins the user's voice channel",inline=True)
      music.add_field(name="👋Leave",value="Leaves the voice channel",inline=True)
      music.add_field(name="🔁Loop",value="Loops the current song",inline=True)
      music.add_field(name="🎤NP - Now Playing",value="Shows the current song that is playing",inline=True)
      music.add_field(name="⏸️Pause", value="Pauses the player", inline=True)
      music.add_field(name="⏯️Play",value="Plays the searched song",inline=True)
      music.add_field(name="⏯️Resume",value="Resumes the player",inline=True)
      music.add_field(name="🔀Shuffle",value="Shuffles the queue",inline=True)
      music.add_field(name="⏭️Skip",value="Skips the current song. Three votes required or song requester has to skip",inline=True)
      music.add_field(name="🎧Spotify",value="Shows the current song playing in Spotify in PC",inline=True)
      music.add_field(name="⏹️Stop", value="Stops the player", inline=True)
      music.add_field(name="🧞Summon",value="Joins the mentioned voice channel. Requires administrator permission",inline=True)
      music.add_field(name="❎Remove (song number)",value="Removes the song from the queue",inline=True)
      music.add_field(name="🗒️Queue", value="Shows the queue", inline=True)
      music.add_field(name="🔊Volume", value="Sets the volume", inline=True)
      music.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=music)

  @help.command(aliases=["radio!"])
  async def radio(self, ctx):
      radio = discord.Embed(title="Help - Radio",description="Below are a list of all available commands pretaining to Radio",color=discord.Color.red())
      radio.add_field(name="rstart",value="Starts the radio",inline=False)
      radio.add_field(name="rstop",value="Stops the radio",inline=False)
      radio.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=radio)

  @help.command(aliases=["echo!"])
  async def echo(self, ctx):
      echo = discord.Embed(title="Help - Echo",description="`spike echo [Message]` makes the Announcer to repeat what the Citizen said.\n\nRefrain from misusing it malicioulsy!",color=discord.Color.red())
      echo.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=echo)

  @help.command(aliases=["google!"])
  async def google(self, ctx):
      google = discord.Embed(title="Help - Google",description="`spike google [Topic]` makes the Announcer to assist the Citizen in searching across the Solar System about Information. \n\nRefrain from misusing it malicioulsy!",color=discord.Color.red())
      google.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=google)

  @help.command(aliases=["invite!"])
  async def invite(self, ctx):
      invite = discord.Embed(title="Help - Invite",description="`spike invite` makes the Announcer to provide the Citizen a summoner if the Citizen wishes the Announcer to be on another Planet. \n\nRefrain from misusing it malicioulsy!",color=discord.Color.red())
      invite.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=invite)

  @help.command(aliases=["ping!"])
  async def ping(self, ctx):
      ping = discord.Embed(title="Help - Ping",description="`spike ping` makes the Announcer to provide the Summoning Citizen an estimated time it took for the Citizen's call to reach the Announcer.",color=discord.Color.red())
      ping.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=ping)

  @help.command(aliases=["poll!"])
  async def poll(self, ctx):
      poll = discord.Embed(title="Help - Poll",description="`spike poll 'question' option1 option2` makes the Announcer to provide the Summoning Citizen a way to ask other Planetary Citizens to vote on a discourse.\n\nRefrain from using it maliciously!",color=discord.Color.red())
      poll.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=poll)

  @help.command(aliases=["id!"])
  async def id(self, ctx):
      data = discord.Embed(title="Help - ID",description="`spike id` provides the Citizen's Citizenship status in the Planet and their details on when they joined the Solar System.",color=discord.Color.red())
      data.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=data)

  @help.command(aliases=["profiles!","profile!"])
  async def profiles(self, ctx):
      profiles = discord.Embed(title="Help - Profiles",description="`spike profiles [@User]` provides the mentioned Citizens' means of contacting them in other Solar Systems and Galaxies in the Universe. ",color=discord.Color.red())
      profiles.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=profiles)

  @help.command(aliases=["remind!"])
  async def remind(self, ctx):
      remind = discord.Embed(title="Help - Remind",description="`spike remind [Time] [Reminder]` helps you to not forget your schedule in this busy Planet.",color=discord.Color.red())
      remind.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=remind)

  @help.command(aliases=["records!"])
  async def records(self, ctx):
      records = discord.Embed(title="Help - Record",description="`spike records` provides the key information pretaining to the Current Planet that the Citizens are living in. ",color=discord.Color.red())
      records.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=records)

  @help.command(aliases=["wanted!"])
  async def wanted(self, ctx):
      wanted = discord.Embed(title="Help - Wanted",description="`spike wanted [@User]` provides the mentioned Citizens' facial features as perceived.",color=discord.Color.red())
      wanted.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=wanted)

  @help.command(aliases=["arrest!"])
  async def arrest(self, ctx):
      arrest = discord.Embed(title="Help - Arrest",description="`spike arrest [@User]` arrests the Citizen for all their bounties /jk",color=discord.Color.red())
      arrest.set_thumbnail(url=self.client.user.avatar_url)
      await ctx.reply(embed=arrest)

def setup(client):
	client.add_cog(Help(client))