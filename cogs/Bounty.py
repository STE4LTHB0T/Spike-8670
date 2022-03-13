import discord,typing, random, os
from discord.ext import commands
from pymongo import MongoClient

level = ["Shinobi", "Aku", "Avengers", "Espada", "Super Saiyajin", "Kaizoku"]
levelnum = [2,10,15,25,35,50]

cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]
spam_channels = [461661510520012800,435765743766863882,478568350080040970,479645984658292737,546632755476300045,775031354374225930,785081153949663242,479139129230360576,791954505678979072,773266465678950520,792260571130626058,802877502661197874]

class Bounty(commands.Cog):
	def __init__(self,client):
		self.client = client
		self._cd = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.member)

	def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
		bucket = self._cd.get_bucket(message)
		return bucket.update_rate_limit()

	def is_it_ON(ctx):
		return ctx.guild.id == 414057277050585088

	@commands.Cog.listener()
	async def on_ready(self):
		print("Bounty is loaded!")
	
	@commands.Cog.listener()
	async def on_message(self,message):
		stats = ranking.find_one({"id":message.author.id, "guild id":message.author.guild.id})
		if not message.author.bot:
			if not message.guild:
				return
			if message.channel.id in spam_channels:
				return
			if "check ratelimit":
				ratelimit = self.get_ratelimit(message)
			if ratelimit is None:
				if stats is None:
					newuser = {"name":message.author.name,"id":message.author.id, "guild id":message.author.guild.id, "guild name":message.author.guild.name, "xp": 0, "woolongs":0}
					ranking.insert_one(newuser)
				else:
					xp=stats["xp"]+10
					woolongs=stats["woolongs"]+10
					ranking.update_one({"id":message.author.id, "guild id":message.author.guild.id},{"$set":{"xp":xp}})
					ranking.update_one({"id":message.author.id, "guild id":message.author.guild.id},{"$set":{"woolongs":woolongs}})
					lvl = 0
					while True:
						if xp < ((50*(lvl**2))+(50*lvl)):
							break
						lvl +=1
					xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
					if xp == 0:
						await message.channel.send(f"**Attention! The level of {message.author.mention} has been raised to Level {lvl}!**")
						if message.guild.id == 414057277050585088:
							for i in range(len(level)):
								if lvl == levelnum[i]:
									await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
									bounty_level=discord.Embed(title="Announcement!",description=f"Attention! {message.author.mention} is now declared as **{level[i]}**!", color=discord.Color.red())
									bounty_level.set_thumbnail(url=message.author.avatar_url)
									await message.channel.send(embed=bounty_level)

	@commands.command()
	async def bounty(self,ctx,member:discord.Member=None):
		if member is None:
			member=ctx.author
		stats=ranking.find_one({"guild id":ctx.guild.id})
		if stats is None:
			pathetic=discord.Embed(description="You have no bounty!")
			await ctx.channel.send(embed=pathetic)
		else:
			xp= stats["xp"]
			lvl = 0
			rank = 0
			while True:
				if xp < ((50*(lvl**2))+(50*lvl)):
					break
				lvl +=1
			xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
			mark = int((xp/(200*((1/2)* lvl)))*5)
			rankings = ranking.find({"guild id":ctx.guild.id}).sort("xp",-1)
			for x in rankings:
				rank +=1
				if stats["id"] == x ["id"]:
					break
			bounty = discord.Embed(title="Bounty Info", color=member.top_role.colour)
			bounty.add_field(name="Name", value=member.mention, inline=True)
			bounty.add_field(name="Bounty XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
			bounty.add_field(name="Bounty Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
			bounty.add_field(name="Bounty Level", value=f"{lvl}", inline = True)
			if member.guild.id ==  414057277050585088:
				bounty.add_field(name="Bounty Level Priority", value=member.top_role.mention, inline = True)
			else:
				pass
			bounty.add_field(name="Bounty Level Progress", value=mark* ":x:" + (5-mark)*":heavy_multiplication_x:", inline=False)
			bounty.set_thumbnail(url=member.avatar_url)
			await ctx.reply(embed=bounty)

	@commands.command(aliases=["top bounties", "top"])
	async def board(self,ctx):
		rankings = ranking.find({"guild id":ctx.guild.id}).sort("xp",-1)
		i = 1
		board = discord.Embed(title=f"{ctx.guild.name} Leaderboard",color=discord.Color.red())
		for x in rankings:
			try:
				temp=ctx.guild.get_member(x["id"])
				tempxp= x["xp"]
				board.add_field(name=f"{i}: {temp.name}", value=f"Bounty XP: {tempxp}", inline= False)
				i+=1
			except:
				pass
			if i==11:
				break
		board.set_thumbnail(url=ctx.guild.icon_url)
		await ctx.reply(embed=board)


def setup(client):
  client.add_cog(Bounty(client))					  