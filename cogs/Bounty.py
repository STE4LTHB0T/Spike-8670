import discord, typing, random, os, logging
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ["MONGO"])

ranking = cluster["discord"]["bounty"]

statuses = cluster["discord"]["statuses"]

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class Bounty(commands.Cog):

    def __init__(self,client):
        self.client = client
        self._cd = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.member)

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bounty is loaded!")

    @commands.hybrid_command(name = "ranks", with_app_command = True, description = "Toggles the ranking system of the server")
    @commands.has_permissions(administrator = True)
    async def ranks(self, ctx):
        guild = statuses.find_one({"id" : ctx.guild.id})
        status = guild["rank_system"]
        if status is True:
            statuses.update_one({"id" : ctx.guild.id}, {"$set" : {"rank_system" : False}})
            await ctx.reply("Ranking system has been disabled!", ephemeral = False)
        else:
            statuses.update_one({"id" : ctx.guild.id}, {"$set" : {"rank_system" : True}})
            await ctx.reply("Ranking system has been enabled!", ephemeral = False)

    @commands.Cog.listener()
    async def on_message(self,message):
        try:
            stats = ranking.find_one({"id" : message.author.id, "guild id" : message.author.guild.id})
            guild_status = statuses.find_one({"id" : message.guild.id})
            if not message.author.bot:
                if not message.guild:
                    return
                disabled = guild_status["rank_system"]
                if disabled is False:
                    return
                else:
                    if "check ratelimit":
                        ratelimit = self.get_ratelimit(message)
                    if ratelimit is None:
                        if stats is None:
                            newuser = {"name" : message.author.display_name, "id" : message.author.id, "guild id" : message.author.guild.id, "guild name" : message.author.guild.name, "xp" : 0, "woolongs" : 0}
                            ranking.insert_one(newuser)
                        else:
                            xp = stats["xp"]+100
                            woolongs = stats["woolongs"]+100	
                            ranking.update_one({"id" : message.author.id, "guild id" : message.author.guild.id}, {"$set" : {"xp" : xp}})
                            ranking.update_one({"id" : message.author.id, "guild id" : message.author.guild.id}, {"$set" : {"woolongs" : woolongs}})
                            lvl = 0
                            while True:
                                if xp<((50*(lvl**2))+(50*lvl)):
                                    break
                                lvl+=1
                            xp-=((50*((lvl-1)**2))+(50*(lvl-1)))
                            if xp == 0:
                                try:
                                    guild = message.author.guild
                                    rank = msg_channel.find_one({"guild id" : guild.id, "name" : "rank"})
                                    tempid = rank["channel id"]
                                    rankchannel = await self.client.fetch_channel(tempid)
                                    await rankchannel.send(f'**Attention! The level of {message.author.name} has been raised to Level {lvl}!**')
                                except: 
                                    await message.channel.send(f"**Attention! The level of {message.author.name} has been raised to Level {lvl}!**")
                                if message.guild.id == 414057277050585088:
                                    for i in range(len(level)):
                                        if lvl == levelnum[i]:
                                            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                            bounty_level=discord.Embed(title="Announcement!",description=f"Attention! {message.author.mention} is now declared as **{level[i]}**!", color=discord.Color.red())
                                            bounty_level.set_thumbnail(url=message.author.avatar_url)
                                            await message.channel.send(embed=bounty_level)
        except:
        	pass

    @commands.hybrid_command(name = "bounty", with_app_command = True, description = "Shows the bounty of a member")
    async def bounty(self, ctx, member : discord.Member = None):
    	if member is None:
    		member = ctx.author
    	stats = ranking.find_one({"id" : member.id, "guild id" : member.guild.id})
    	if stats is None:
    		pathetic = discord.Embed(description = "You have no bounty!")
    		await ctx.channel.reply(embed = pathetic, ephemeral = False)
    	else:
    		xp = stats["xp"]
    		lvl = 0
    		rank = 0
    		while True:
    			if xp<((50*(lvl**2))+(50*lvl)):
    				break
    			lvl+=1
    		xp-=((50*((lvl-1)**2))+(50*(lvl-1)))
    		mark=int((xp/(200*((1/2)* lvl)))*5)
    		rankings = ranking.find({"guild id" : ctx.guild.id}).sort("xp", -1)
    		for x in rankings:
    			rank+=1
    			if stats["id"] == x ["id"]:
    				break
    		bounty = discord.Embed(title = "Bounty Info", color = member.top_role.colour)
    		bounty.add_field(name = "Name", value = member.mention, inline = True)
    		bounty.add_field(name = "Bounty XP", value = f"{xp}/{int(200*((1/2)*lvl))}", inline = True)
    		bounty.add_field(name = "Bounty Rank", value = f"{rank}/{ctx.guild.member_count}", inline = True)
    		bounty.add_field(name = "Bounty Level", value = f"{lvl}", inline = True)
    		if member.guild.id ==  414057277050585088:
    			bounty.add_field(name="Bounty Level Priority", value=member.top_role.mention, inline = True)
    		else:
    			pass
    		bounty.add_field(name = "Bounty Level Progress", value = mark*":x:" + (5-mark)*":heavy_multiplication_x:", inline = False)
    		bounty.set_thumbnail(url = member.avatar.url)
    		await ctx.reply(embed = bounty, ephemeral = False)

    @commands.hybrid_command(name = "board", with_app_command = True, description = "Shows the leaderboard of the top bounties of the server")
    async def board(self, ctx):
    	rankings = ranking.find({"guild id" : ctx.guild.id}).sort("xp", -1)
    	i = 1
    	board = discord.Embed(title = f"{ctx.guild.name} Leaderboard", color = 0xff0000)
    	for x in rankings:
    		try:
    			temp = ctx.guild.get_member(x["id"])
    			tempxp = x["xp"]
    			board.add_field(name = f"{i} : {temp.name}", value = f"Bounty XP : {tempxp}", inline = False)
    			i+=1
    		except:
    			pass
    		if i==11:
    			break
    	board.set_thumbnail(url = ctx.guild.icon.url)
    	await ctx.reply(embed = board, ephemeral = False)

async def setup(client):
    await client.add_cog(Bounty(client))					  