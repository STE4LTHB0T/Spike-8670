import discord, time, datetime, asyncio, random, os
from datetime import datetime
from discord.ext import commands
from googlesearch import search
from pymongo import MongoClient
from resources.Lists import *

cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]

class Replies(commands.Cog):

  def __init__(self, client):
    self.client = client	

  @commands.Cog.listener()
  async def on_ready(self):
    print('Replies is loaded!')
   
  @commands.command()
  async def ping(self, ctx):
    time_1 = time.perf_counter()
    await ctx.trigger_typing()
    time_2 = time.perf_counter()
    ping = round((time_2-time_1)*1000)
    await ctx.reply(f"Your ping is **{ping}ms**.")

  @commands.command()
  async def botping(self, ctx):
    await ctx.reply(f'{round(self.client.latency*1000)}ms')

  @commands.command()
  async def spotify(self, ctx, user: discord.Member = None):
    user = user or ctx.author  
    spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if spot is None:
        await ctx.send(f"{user.name} is not listening to Spotify")
        return
    embed = discord.Embed(title=f"{user.name}'s Current Spotify Track", color=spot.color)
    embed.add_field(name="Song", value=spot.title,inline=True)
    embed.add_field(name="Artist", value=spot.artist,inline=True)
    embed.add_field(name="Album", value=spot.album,inline=True)
    m1, s1 = divmod(int(spot.duration.seconds), 60)
    spot_duration = f'{m1}:{s1}'
    embed.add_field(name="Duration",value=spot_duration,inline=True)
    embed.add_field(name="Track Link", value=f"[{spot.title}](https://open.spotify.com/track/{spot.track_id})",inline=True)
    embed.set_thumbnail(url=spot.album_cover_url)
    await ctx.reply(embed=embed)

  @commands.command()
  async def echo(self, ctx, *, content:str):
    await ctx.message.delete()
    async with ctx.typing():
      await asyncio.sleep(0.5)
    await ctx.send(content)  
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.client.user:
      return

    if 'fml' in message.content:
      await message.channel.send('https://tenor.com/X57z.gif')
    
    if 'wait what?' in message.content:
      await message.channel.send('you got confused, eh?')

    if 'sentient' in message.content:
      await message.channel.send("**Bot Instrumentality Project Undergoing!**")
      await message.channel.send("https://tenor.com/bh980.gif")
      

  @commands.command()
  async def google(self, ctx,*, query):
    if query not in bannedwords:
      searchContent = query
      for i in search(searchContent,tld="com", num=1, stop=1, pause=2):
        await ctx.reply(i)
    else: 
      await ctx.reply("Fuck You!")			
			

  @commands.command()
  async def wanted(self,ctx,member:discord.Member=None):
    if member is None:
      member=ctx.author
    try:
      bounty = ranking.find_one({"id":member.id, "guild id":member.guild.id})
      bounty_value = bounty["xp"]
      woolongs= bounty["woolongs"]
      woolong=int(woolongs)
      wanted=discord.Embed(description=f"**WANTED** {member.mention}**!**\n **Bounty Value: <:woolongs:952789606762438686> {bounty_value}**\n **Woolongs: <:woolongs:952789606762438686> {woolong}**", color=member.top_role.colour)			
      wanted.set_image(url=member.avatar_url)
      await ctx.reply(embed=wanted)
    except:
      avatar=discord.Embed(description=f"**WANTED** {member.mention}!", color=member.top_role.colour)
      avatar.set_image(url=member.avatar_url)
      await ctx.reply(embed=avatar)
    

def setup(client):
  client.add_cog(Replies(client))