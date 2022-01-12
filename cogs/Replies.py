import discord, time, datetime, asyncio, random, giphy_client, os
from datetime import datetime
from discord.ext import commands
from googlesearch import search
from pymongo import MongoClient
from resources.Lists import *
from giphy_client.rest import ApiException 

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
  async def aping(self, ctx):
    await ctx.reply(f'{round(self.client.latency*1000)}ms')

  @commands.command()
  async def date(self,ctx):
    await ctx.reply(f"{datetime.now().strftime('%B %d %Y - %H:%M:%S')}")

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
  async def pain(self,ctx):
    await ctx.message.delete()
    async with ctx.typing():
      await asyncio.sleep(0.5)
    await ctx.send("sed laif")

  @commands.command()
  async def echo(self, ctx, *, content:str):
    await ctx.message.delete()
    async with ctx.typing():
      await asyncio.sleep(0.5)
    await ctx.send(content)  
  
  @commands.command()
  async def arrest(self,ctx,member:discord.Member):
    if member == self.client.user:
      await ctx.reply("You can't arrest me!")
      return
    if member.id == 261143180387287040:
      await ctx.reply("https://cdn.discordapp.com/attachments/849338245354749973/852853543606026290/6b5.jpg")
      return
    if member.id == ctx.author.id:
      await ctx.reply("https://media.giphy.com/media/4MxLhxhOqCqYw/giphy.gif")
      return
    if member.id == 463780399437447200:
      await ctx.reply("You can't arrest the bot owner, you idiot!")
      await ctx.send("https://media.giphy.com/media/USNlL9p2fxY6Q/giphy.gif")
      return
    else:
      gifs=["https://media.giphy.com/media/LowuSEmgBGEso/giphy.gif",
      
      "https://media.giphy.com/media/p7QJSVvU4bMWc/giphy.gif",
      
      "https://media.giphy.com/media/cjvFRb8DyAk0g/giphy.gif",
      
      "https://media.giphy.com/media/MCpVd5NJhNXJRkXV60/giphy.gif",
      
      "https://media.giphy.com/media/NQ43L8yLRg3iE/giphy.gif",
      
      "https://media.giphy.com/media/12mQQxo2lHcyhG/giphy.gif",
      
      "https://media.giphy.com/media/ovrcwymJaF9f2/giphy.gif",
      
      "https://media.giphy.com/media/v87ycxiegXFF6/giphy.gif",
      
      "https://media.giphy.com/media/10ZuedtImbopos/giphy.gif",
      
      "https://media.giphy.com/media/gQbVzXQQbGO7C/giphy.gif",
      
      "https://media.giphy.com/media/gQbVzXQQbGO7C/giphy.gif",
      
      "https://media.giphy.com/media/b1dXky39p5Zcs/giphy.gif",
      
      "https://media.giphy.com/media/14kYBP3sOq3ubm/giphy.gif",
      
      "https://media.giphy.com/media/irWbG2YwTDXR6/giphy.gif",
      
      "https://media.giphy.com/media/eR7OEDQDyA7Cg/giphy.gif",
      
      "https://media.giphy.com/media/KmG26GNmdWOUE/giphy.gif",
      
      "https://media.giphy.com/media/NNmJyVWriRDlS/giphy.gif"]
      arrest = discord.Embed(description= f"{ctx.author.mention} is trying to arrest {member.mention}!", color=member.top_role.colour) 
      arrest.set_image(url=random.choice(gifs))
      await ctx.reply(embed=arrest)
  
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

    """if message.content.lower().startswith('spike google'):
      if message.content.lower() in bannedwords:
        await message.channel.send("Fuck You!")
        return
      else:      
        searchContent = ""
        text = str(message.content).split(' ')
        for i in range(2, len(text)):
          searchContent = searchContent + text[i]
        for j in search(searchContent, tld="com", num=1, stop=1, pause=2):
          await message.channel.send(j)"""  

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
    bounty = ranking.find_one({"id":member.id})
    bounty_value = bounty["xp"]
    number = random.randint(0, 10000)
    if ctx.guild.id == 414057277050585088:
      wanted= discord.Embed(description=f"**WANTED** {member.mention}**!**\n **Bounty Value: ${bounty_value}**",color=member.top_role.colour)
    else:
      wanted= discord.Embed(description=f"**WANTED** {member.mention}**!**\n **Bounty Value: ${number}**",color=member.top_role.colour)			
    wanted.set_image(url=member.avatar_url)
    await ctx.reply(embed=wanted)

  @commands.command()
  async def gif(self,ctx,*,search):

    api_key="hiw1KTLvX47dVLiJGHZrInUk1HILL7a9"
    api_instance = giphy_client.DefaultApi()

    try: 
        
        api_response = api_instance.gifs_search_get(api_key, search, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=search)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.message.delete()
        await ctx.channel.reply(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)


def setup(client):
  client.add_cog(Replies(client))