import discord, os, datetime, dateutil.parser, aiofiles, asyncio, logging
from discord.ext import commands
from pymongo import MongoClient
from googlesearch import search
from resources.Lists import *

cluster = MongoClient(os.environ["MONGO"])

ranking = cluster["discord"]["bounty"]

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class Replies(commands.Cog):

    def __init__(self, client):
        self.client = client	

    @commands.Cog.listener()
    async def on_ready(self):
        print("Replies is loaded!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if "fml" in message.content:
          await message.channel.send("https://tenor.com/X57z.gif")
    
        if "sentient" in message.content:
          await message.channel.send("**Bot Instrumentality Project Undergoing!**")
          await message.channel.send("https://tenor.com/bh980.gif")

    @commands.Cog.listener()
    async def on_message(self, message):    
        for x in message.mentions:
            if (x == self.client.user):
                if message.author == self.client.user:
                    return

                if message.author.id == 463780399437447200:
                    await message.channel.send(f"Hisashiburi {message.author.mention}!", delete_after = 5)
                    await message.channel.send("https://media.giphy.com/media/5gK1hvwoutPnG/giphy.gif", delete_after = 5)
                    return

                elif message.author.id == message.guild.owner.id:
                    await message.channel.send("Hello, Chief!<:FeelsFedoraMan:477838638185578496>", delete_after = 5)

                else:
                    await message.channel.send(random.choice(mentions_reply), delete_after = 15)

    @commands.hybrid_command(name = "google", with_app_command = True, description = "Gives you a search result")
    async def google(self, ctx, * , query):
        try:
            for i in search(query, num_results = 1):
                await ctx.reply(i, ephemeral = False)
                break
        except Exception as e:
            await ctx.reply("An error occurred! Please try again!")

    @commands.hybrid_command(name = "dm", with_app_command = True, description = "Sends a personalized DM to a user")
    async def dm(self, ctx, user_id = None, *, args = None):
        if user_id != None and args != None:
            try:
                target = await self.client.fetch_user(user_id)
                await ctx.message.delete()
                await target.send(args)
                await ctx.send("Delivered!", delete_after=2)
            except:
                await ctx.channel.send("Please try again!")
        else:
            await ctx.channel.send("Please mention a user ID to DM to!")

    @commands.hybrid_command(name = "ping", with_app_command = True, description = "Tells you the bot's ping")
    async def ping(self, ctx):
        await ctx.reply(f'{round(self.client.latency*1000)}ms', ephemeral = False)

    @commands.hybrid_command(name = "spotify", with_app_command = True, description = "Tells you the detail about the user's current Spotify track")
    async def spotify(self, ctx, user: discord.Member = None):
        user = user or ctx.author  
        spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
        if spot is None:
            await ctx.send(f"{user.name} is not listening to Spotify")
            return
        embed = discord.Embed(title = f"{user.name}'s Current Spotify Track", color = spot.color)
        embed.add_field(name = "Song", value = spot.title, inline = True)
        embed.add_field(name = "Artist", value = spot.artist, inline = True)
        embed.add_field(name = "Album", value = spot.album, inline = True)
        m1, s1 = divmod(int(spot.duration.seconds), 60)
        spot_duration = f"{m1}:{s1}"
        embed.add_field(name = "Duration",value = f"{dateutil.parser.parse(str(spot.duration)).strftime('%M:%S')}", inline = True)
        embed.add_field(name = "Track Link", value = f"[{spot.title}](https://open.spotify.com/track/{spot.track_id})", inline = True)
        embed.set_thumbnail(url = spot.album_cover_url)
        await ctx.reply(embed = embed, ephemeral = False)

    @commands.hybrid_command(name = "wanted", with_app_command = True, description = "Shows the avatar of the user")
    async def wanted(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        try:
            bounty = ranking.find_one({"id" : member.id, "guild id" : member.guild.id})
            bounty_value = bounty["xp"]
            woolongs = bounty["woolongs"]
            wanted = discord.Embed(description = f"**WANTED** {member.mention}**!**\n **Bounty Value : <:woolongs:952789606762438686> {bounty_value}**\n **Woolongs : <:woolongs:952789606762438686> {woolongs}**", color = member.top_role.colour)			
            wanted.set_image(url = member.avatar.url)
            await ctx.reply(embed = wanted, ephemeral = False)
        except Exception as e:
            avatar = discord.Embed(description = f"**WANTED** {member.mention}!", color = member.top_role.colour)
            avatar.set_image(url = member.avatar.url)
            await ctx.reply(embed = avatar, ephemeral = False)

    @commands.hybrid_command(name = "thinkingbee", with_app_command = True, description = "According to all known laws of aviation, there is no way a bee should be able to fly.")
    async def thinkingbee(self, ctx):
        user = self.client.get_user(463780399437447200)
        await ctx.send(f"Please wait for a minute for confirmation!\nTo shutdown the bot, please message [STE4LTH_B0T](https://discord.com/users/463780399437447200).")
        await user.send("**THINKINGBEE** command is about to be used. Be ready!")
        await asyncio.sleep(15)
        async with aiofiles.open(f"./resources/BEE.txt", mode = "r") as file:
            lines = await file.readlines()
            for line in lines:
                await ctx.send(line)

async def setup(client):
    await client.add_cog(Replies(client))