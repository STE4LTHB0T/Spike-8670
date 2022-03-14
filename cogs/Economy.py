from unittest.mock import NonCallableMagicMock
import discord, os, asyncio
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_it_ON(ctx):
        return ctx.guild.id == 414057277050585088

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy is loaded!')

        for guild in self.client.guilds:
            spike=ranking.find_one({"id": "804347400004173864", "guild id": guild.id})
            if spike is None:
                new_guild={"name":"Spike","id": "804347400004173864", "guild id":guild.id, "guild name":guild.name, "woolongs":0}
                ranking.insert_one(new_guild)
                print("Added {}".format(guild.name))

    @commands.command()
    async def trade(self,ctx,member:discord.Member,woolong:int):
        if member.id==ctx.author.id:
            await ctx.send("You can't trade with yourself!")
            return
        sender=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
        temp=sender["woolongs"]
        if woolong>temp:
            await ctx.send("You are broke!")
            return
        else:
            async with ctx.typing():
                await asyncio.sleep(0.5)
            message=await ctx.send("Beginning Bounty Transaction!")
            async with ctx.typing():
                await asyncio.sleep(0.5)        
            await message.edit(content=f"Transferring {woolong} Woolongs to {member.mention} from {ctx.author.mention}")

            sender=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
            reciever=ranking.find_one({"id":member.id, "guild id":ctx.guild.id})

            send=sender["woolongs"]-woolong
            recieve=reciever["woolongs"]+woolong

            sender=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":send}})
            reciever=ranking.update_one({"id":member.id, "guild id":ctx.guild.id},{"$set":{"woolongs":recieve}})

            async with ctx.typing():
                await asyncio.sleep(0.5)
            await message.edit(content="Bounty Transaction successful!")

    @commands.command()
    @commands.check(is_it_ON)
    async def sell(self,ctx):
        self.client.guildid = ctx.guild.id
        self.client.uid = self.client.user.id 
        self.client.reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣'] #['7⃣', '8⃣', '9⃣', '🔟']
        rembed=discord.Embed(title="Woolong Roles",description="Sell Woolongs for a role",color=discord.Color.red())
        rembed.add_field(name=':one: Komi-sama Cult', value='10000 Woolongs', inline=True)
        rembed.add_field(name=':two: Marin-sama Cult', value='10000 Woolongs', inline=True)
        rembed.add_field(name=':three: Monogatari Circlejerk', value='10000 Woolongs', inline=True)
        rembed.add_field(name=':four: Bot Na Cult', value='10000 Woolongs', inline=True)
        rembed.add_field(name=':five: Xkami Cult', value='10000 Woolongs', inline=True)
        rembed.add_field(name=':six: The Mute Pass', value='50000 Woolongs', inline=True)
        rembed.set_thumbnail(url=self.client.user.avatar_url)
        self.client.msg=await ctx.send(embed=rembed)
        for reaction in self.client.reactions:
            await self.client.msg.add_reaction(reaction)
        self.client.reactid=self.client.msg.id
        print(self.client.reactid)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        reactid = self.client.reactid
        if payload.member.bot:
            return
        else:

            ksc = discord.utils.get(payload.member.guild.roles, name='Komi-sama Cult')
            msc = discord.utils.get(payload.member.guild.roles, name='Marin-sama Cult')
            mc = discord.utils.get(payload.member.guild.roles, name='Monogatari Circlejerk')
            bnc = discord.utils.get(payload.member.guild.roles, name='Bot Na Cult')
            xc = discord.utils.get(payload.member.guild.roles, name='Xkami Cult')
            tmp = discord.utils.get(payload.member.guild.roles, name='The Mute Pass')            
            
            
            if reactid == payload.message_id:
                member=payload.member
                emoji=payload.emoji.name
                re=discord.Embed(description=f"Role assigned!",color=discord.Color.red())
                check=discord.Embed(description="Role is already available for the user!",color=discord.Color.red())
                broke=discord.Embed(description="You are broke!",color=discord.Color.red())
                
                #komi-sama cult
                if emoji == '1⃣':
                    if ksc in member.roles:
                        await self.client.msg.edit(embed=check)
                        for reaction in self.client.reactions:
                            await self.client.msg.clear_reaction(reaction)
                    else:
                        rksc=10000
                        buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                        temprksc=buyer["woolongs"]
                        if rksc>temprksc:
                            await self.client.msg.edit(embed=broke)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                            return
                        else:
                            buying=buyer["woolongs"]-rksc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            selling=seller["woolongs"]+rksc

                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})

                            await member.add_roles(ksc)
                            await self.client.msg.edit(embed=re)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                
                #marin-sama cult
                elif emoji == '2⃣':
                    if msc in member.roles:
                        await self.client.msg.edit(embed=check)
                        for reaction in self.client.reactions:
                            await self.client.msg.clear_reaction(reaction)
                    else:
                        msc=10000
                        buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                        tempmsc=buyer["woolongs"]
                        if msc>tempmsc:
                            await self.client.msg.edit(embed=broke)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                            return
                        else:
                            buying=buyer["woolongs"]-msc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            selling=seller["woolongs"]+msc

                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})

                            await member.add_roles(msc)
                            await self.client.msg.edit(embed=re)
                            await self.client.msg.clear_reaction(emoji)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                
                #monogatari
                elif emoji == '3⃣': #'3⃣', '4⃣', '5⃣'
                    if mc in member.roles:
                        await self.client.msg.edit(embed=check)
                        for reaction in self.client.reactions:
                            await self.client.msg.clear_reaction(reaction)
                    else:
                        rmc=10000
                        buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                        temprmc=buyer["woolongs"]
                        if rmc>temprmc:
                            await self.client.msg.edit(embed=broke)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                            return           
                        else:             
                            buying=buyer["woolongs"]-rmc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            selling=seller["woolongs"]+rmc

                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})

                            await member.add_roles(mc)
                            await self.client.msg.edit(embed=re)
                            await self.client.msg.clear_reaction(emoji)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                
                #bot na cult
                elif emoji == '4⃣':
                    if bnc in member.roles:
                        await self.client.msg.edit(embed=check)
                        for reaction in self.client.reactions:
                            await self.client.msg.clear_reaction(reaction)
                    else:
                        rbnc=10000
                        buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                        temprbnc=buyer["woolongs"]
                        if rbnc>temprbnc:
                            await self.client.msg.edit(embed=broke)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                            return      
                        else:                  
                            buying=buyer["woolongs"]-rbnc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            selling=seller["woolongs"]+rbnc

                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})

                            await member.add_roles(bnc)
                            await self.client.msg.edit(embed=re)
                            await self.client.msg.clear_reaction(emoji)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                
                #xkami cult
                elif emoji == '5⃣':
                    if xc in member.roles:
                        await self.client.msg.edit(embed=check)
                        for reaction in self.client.reactions:
                            await self.client.msg.clear_reaction(reaction)
                    else:
                        rxc=50000
                        buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                        temprxc=buyer["woolongs"]
                        if rxc>temprxc:
                            await self.client.msg.edit(embed=broke)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                            return
                        else:                        
                            buying=buyer["woolongs"]-rxc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            selling=seller["woolongs"]+rxc
    
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})
                            
                            await member.add_roles(xc)
                            await self.client.msg.edit(embed=re)
                            await self.client.msg.clear_reaction(emoji)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)                
                
                #mute pass
                else:   
                    if tmp in member.roles:
                        await self.client.msg.edit(embed=check)
                        for reaction in self.client.reactions:
                            await self.client.msg.clear_reaction(reaction)
                    else:
                        rtmp=50000
                        buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                        temprtmp=buyer["woolongs"]
                        if rtmp>temprtmp:
                            await self.client.msg.edit(embed=broke)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)
                            return       
                        else:                     
                            buying=buyer["woolongs"]-rtmp
    
                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            selling=seller["woolongs"]+rtmp
    
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})
    
                            await member.add_roles(tmp)
                            await self.client.msg.edit(embed=re)
                            await self.client.msg.clear_reaction(emoji)
                            for reaction in self.client.reactions:
                                await self.client.msg.clear_reaction(reaction)


    @commands.command()
    async def bank(self,ctx):
        id="804347400004173864"
        spike=ranking.find_one({"id":id, "guild id":ctx.guild.id})
        balance=spike["woolongs"]
        bal= discord.Embed(description=f"**Bank Of Solar System**\n **Woolongs: <:woolongs:952789606762438686> {balance}**", color=discord.Color.red())			
        bal.set_image(url=self.client.user.avatar_url)
        await ctx.reply(embed=bal)

        
def setup(client):
  client.add_cog(Economy(client))