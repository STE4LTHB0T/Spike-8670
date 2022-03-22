import discord, os, asyncio, datetime, random
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
    @commands.cooldown(1, 86400.0, commands.BucketType.user)
    async def daily(self,ctx):
        wage=random.randint(0,1000)
        work=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
        wager=work["woolongs"]+wage
        work=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":wager}})
        await ctx.reply(f"Your work has been appreciated! You have been given {wage} Woolongs for your work!")

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
            await ctx.reply(f"Chill out man, Come back a little later or you will be caught lacking! Please come again after "+str(remaining_time))

    @commands.command()
    async def trade(self,ctx,member:discord.Member,woolong:int):
        if member.id==ctx.author.id:
            await ctx.send("You can't trade with yourself!")
            return
        if member==self.client.user:
            await ctx.send("If you are feeling generous, I will take your entire bank balance!")
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
        rembed.add_field(name=':one: Komi-sama Cult', value='50000 Woolongs', inline=True)
        rembed.add_field(name=':two: Marin-sama Cult', value='50000 Woolongs', inline=True)
        rembed.add_field(name=':three: Monogatari Circlejerk', value='50000 Woolongs', inline=True)
        rembed.add_field(name=':four: Bot Na Cult', value='50000 Woolongs', inline=True)
        rembed.add_field(name=':five: XKami Cult', value='50000 Woolongs', inline=True)
        rembed.add_field(name=':six: The Mute Pass', value='100000 Woolongs', inline=True)
        rembed.set_thumbnail(url=self.client.user.avatar_url)
        
        self.client.msg=await ctx.send(embed=rembed)
        for reaction in self.client.reactions:
            await self.client.msg.add_reaction(reaction)
        self.client.reactid=self.client.msg.id
        self.client.sellid=ctx.author.id
        print(self.client.reactid)


    @commands.command()
    @commands.cooldown(1, 10800.0, commands.BucketType.user)
    async def ship(self,ctx):

        self.client.reply = random.randint(0,1)
        self.client.gacha = random.randint(0,500000)

        self.client.numbers = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣']

        shipembed = discord.Embed(title="Ship sale",description="Buy a ship to go to different place",color=discord.Color.red())
        shipembed.add_field(name=':one: Venus', value='25000 Woolongs', inline=True)
        shipembed.add_field(name=':two: Earth', value='15000 Woolongs', inline=True)
        shipembed.add_field(name=':three: Mars', value='150000 Woolongs', inline=True)
        shipembed.add_field(name=':four: Ganymede', value='25000 Woolongs', inline=True)
        shipembed.add_field(name=':five: Jupiter', value='35000 Woolongs', inline=True)
        shipembed.add_field(name=':six: Saturn', value='100000 Woolongs', inline=True)
        shipembed.set_thumbnail(url=self.client.user.avatar_url)
        
        self.client.ship=await ctx.send(embed=shipembed)
        
        for sreaction in self.client.numbers:
            await self.client.ship.add_reaction(sreaction)
        self.client.rid=self.client.ship.id
        self.client.shipid=ctx.author.id
        print(self.client.rid)
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

#sell command

        reactid = self.client.reactid
        raid = self.client.rid
        if payload.message_id == reactid:
            if payload.member.bot:
                return
            if payload.member.id != self.client.sellid:
                return
            else:

                ksc = discord.utils.get(payload.member.guild.roles, name='Komi-sama Cult')
                msc = discord.utils.get(payload.member.guild.roles, name='Marin-sama Cult')
                mc = discord.utils.get(payload.member.guild.roles, name='Monogatari Circlejerk')
                bnc = discord.utils.get(payload.member.guild.roles, name='Bot Na Cult')
                xc = discord.utils.get(payload.member.guild.roles, name='XKami Cult')
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
                            rksc=50000
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
                            rmsc=50000
                            buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                            temprmsc=buyer["woolongs"]
                            if rmsc>temprmsc:
                                await self.client.msg.edit(embed=broke)
                                for reaction in self.client.reactions:
                                    await self.client.msg.clear_reaction(reaction)
                                return
                            else:
                                buying=buyer["woolongs"]-rmsc

                                seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                                selling=seller["woolongs"]+rmsc

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
                            rmc=50000
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
                            rbnc=50000
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
                            rtmp=100000
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

#ship command

        if payload.message_id == raid:
            if payload.member.bot:
                return
            if payload.member.id != self.client.shipid:
                return
            else:           
                member=payload.member
                emoji=payload.emoji.name
                broke=discord.Embed(description="You are broke!",color=discord.Color.red())
                hunt=discord.Embed(description="Trying to capturing the bounty",color=discord.Color.red())                

                #Venus
                if emoji == '1⃣':
                    rv=25000
                    buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                    temprv=buyer["woolongs"]
                    if rv>temprv:
                        await self.client.ship.edit(embed=broke)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)
                        return                        
                    else:
                        buying=buyer["woolongs"]-rv

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                        selling=seller["woolongs"]+rv

                        buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})
                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await self.client.ship.edit(embed=prep)

                        await self.client.ship.clear_reaction(emoji)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)                        
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Venus",color=discord.Color.red())
                        await self.client.ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await self.client.ship.edit(embed=hunt)

                       
                        if self.client.reply == 0:
                            failed=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rv*0.7)
                            tf=tfailed+ptf
                            
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            sfailed=seller["woolongs"]
                            
                            sf=int(rv*0.3)
                            stf=sfailed+sf

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await self.client.ship.edit(embed=fail)

                
                        if self.client.reply == 1:

                            if self.client.gacha%2 == 0:
                                
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
    

                            elif self.client.gacha%10 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})                              
                                tsuccess=success["woolongs"]

                                ten=int(10*payment)
                                tp=tsuccess+ten
                                
                                paid=discord.Embed(description=f"You have been paid {ten} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
                                

                            elif self.client.gacha%15 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]
                                
                                fifteen=int(15*payment)
                                tp=tsuccess+fifteen

                                paid=discord.Embed(description=f"You have been paid {fifteen} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})
                                
                                await self.client.ship.edit(embed=paid)
                                

                            else:
                                payment=random.randint(25000,30000)

                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})                            

                                await self.client.ship.edit(embed=paid)
                                                            

                #Earth
                elif emoji == '2⃣':
                    rearth=15000
                    buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                    temprearth=buyer["woolongs"]
                    if rearth>temprearth:
                        await self.client.ship.edit(embed=broke)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)
                        return                        
                    else:
                        buying=buyer["woolongs"]-rearth

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                        selling=seller["woolongs"]+rearth

                        buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})   
                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await self.client.ship.edit(embed=prep)   
                        await self.client.ship.clear_reaction(emoji)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)                  
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Earth",color=discord.Color.red())
                        await self.client.ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await self.client.ship.edit(embed=hunt)

                        if self.client.reply == 0:
                            failed=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rearth*0.7)
                            tf=tfailed+ptf
                            
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            sfailed=seller["woolongs"]
                            
                            sf=int(rearth*0.3)
                            stf=sfailed+sf

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await self.client.ship.edit(embed=fail)


                        if self.client.reply == 1:

                            if self.client.gacha%2 == 0:
                                
                                payment=random.randint(15000,20000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
    

                            elif self.client.gacha%10 == 0:
                                payment=random.randint(15000,20000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})                              
                                tsuccess=success["woolongs"]

                                ten=int(10*payment)
                                tp=tsuccess+ten
                                
                                paid=discord.Embed(description=f"You have been paid {ten} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
                                

                            elif self.client.gacha%15 == 0:
                                payment=random.randint(15000,20000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]
                                
                                fifteen=int(15*payment)
                                tp=tsuccess+fifteen

                                paid=discord.Embed(description=f"You have been paid {fifteen} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})
                                
                                await self.client.ship.edit(embed=paid)
                                

                            else:
                                payment=random.randint(15000,20000)

                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})                            

                                await self.client.ship.edit(embed=paid)


                #Mars
                elif emoji == '3⃣':
                    rm=150000
                    buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                    temprm=buyer["woolongs"]
                    if rm>temprm:
                        await self.client.ship.edit(embed=broke)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)
                        return                        
                    else:
                        buying=buyer["woolongs"]-rm

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                        selling=seller["woolongs"]+rm

                        buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})      

                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await self.client.ship.edit(embed=prep)

                        await self.client.ship.clear_reaction(emoji)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)                  
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Mars",color=discord.Color.red())
                        await self.client.ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await self.client.ship.edit(embed=hunt)

                        if self.client.reply == 0:
                            failed=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rm*0.7)
                            tf=tfailed+ptf
                            
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            sfailed=seller["woolongs"]
                            
                            sf=int(rm*0.3)
                            stf=sfailed+sf

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await self.client.ship.edit(embed=fail)


                        if self.client.reply == 1:

                            if self.client.gacha%2 == 0:
                                
                                payment=random.randint(150000,200000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
    

                            elif self.client.gacha%10 == 0:
                                payment=random.randint(150000,200000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})                              
                                tsuccess=success["woolongs"]

                                ten=int(10*payment)
                                tp=tsuccess+ten
                                
                                paid=discord.Embed(description=f"You have been paid {ten} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
                                

                            elif self.client.gacha%15 == 0:
                                payment=random.randint(150000,200000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]
                                
                                fifteen=int(15*payment)
                                tp=tsuccess+fifteen

                                paid=discord.Embed(description=f"You have been paid {fifteen} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})
                                
                                await self.client.ship.edit(embed=paid)
                                

                            else:
                                payment=random.randint(150000,200000)

                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})                            

                                await self.client.ship.edit(embed=paid)

                #Ganymede
                elif emoji == '4⃣':
                    rg=25000
                    buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                    temprg=buyer["woolongs"]
                    if rg>temprg:
                        await self.client.ship.edit(embed=broke)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)
                        return                        
                    else:
                        buying=buyer["woolongs"]-rg

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                        selling=seller["woolongs"]+rg

                        buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})      
                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await self.client.ship.edit(embed=prep)                        
                        
                        await self.client.ship.clear_reaction(emoji)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)                  
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Ganymede",color=discord.Color.red())
                        await self.client.ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await self.client.ship.edit(embed=hunt)

                        if self.client.reply == 0:
                            failed=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rg*0.7)
                            tf=tfailed+ptf
                            
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            sfailed=seller["woolongs"]
                            
                            sf=int(rg*0.3)
                            stf=sfailed+sf

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await self.client.ship.edit(embed=fail)


                        if self.client.reply == 1:

                            if self.client.gacha%2 == 0:
                                
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
    

                            elif self.client.gacha%10 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})                              
                                tsuccess=success["woolongs"]

                                ten=int(10*payment)
                                tp=tsuccess+ten
                                
                                paid=discord.Embed(description=f"You have been paid {ten} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
                                

                            elif self.client.gacha%15 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]
                                
                                fifteen=int(15*payment)
                                tp=tsuccess+fifteen

                                paid=discord.Embed(description=f"Woah! You have been paid {fifteen} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})
                                
                                await self.client.ship.edit(embed=paid)
                                

                            else:
                                payment=random.randint(25000,30000)

                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})                            

                                await self.client.ship.edit(embed=paid)
                                    
                #Jupiter
                elif emoji == '5⃣':
                    rj=35000
                    buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                    temprj=buyer["woolongs"]
                    if rj>temprj:
                        await self.client.ship.edit(embed=broke)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)
                        return                        
                    else:
                        buying=buyer["woolongs"]-rj

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                        selling=seller["woolongs"]+rj

                        buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})      
                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await self.client.ship.edit(embed=prep)                        
                        
                        await self.client.ship.clear_reaction(emoji)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)                  
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Jupiter",color=discord.Color.red())
                        await self.client.ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await self.client.ship.edit(embed=hunt)
                    
                        if self.client.reply == 0:
                            failed=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rj*0.7)
                            tf=tfailed+ptf
                            
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            sfailed=seller["woolongs"]
                            
                            sf=int(rj*0.3)
                            stf=sfailed+sf

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await self.client.ship.edit(embed=fail)


                        if self.client.reply == 1:

                            if self.client.gacha%2 == 0:
                                
                                payment=random.randint(35000,40000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
    

                            elif self.client.gacha%10 == 0:
                                payment=random.randint(35000,40000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})                              
                                tsuccess=success["woolongs"]

                                ten=int(10*payment)
                                tp=tsuccess+ten
                                
                                paid=discord.Embed(description=f"You have been paid {ten} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
                                

                            elif self.client.gacha%15 == 0:
                                payment=random.randint(35000,40000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]
                                
                                fifteen=int(15*payment)
                                tp=tsuccess+fifteen

                                paid=discord.Embed(description=f"Woah! You have been paid {fifteen} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})
                                
                                await self.client.ship.edit(embed=paid)
                                

                            else:
                                payment=random.randint(35000,40000)

                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})                            

                                await self.client.ship.edit(embed=paid)


                #Saturn
                else:
                    rs=100000
                    buyer=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                    temprs=buyer["woolongs"]
                    if rs>temprs:
                        await self.client.ship.edit(embed=broke)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)
                        return                        
                    else:
                        buying=buyer["woolongs"]-rs

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                        selling=seller["woolongs"]+rs

                        buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":buying}})
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":selling}})      
                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await self.client.ship.edit(embed=prep)                        
                        
                        await self.client.ship.clear_reaction(emoji)
                        for sreaction in self.client.numbers:
                            await self.client.ship.clear_reaction(sreaction)                  
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Saturn",color=discord.Color.red())
                        await self.client.ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await self.client.ship.edit(embed=hunt)
                        
                        if self.client.reply == 0:
                            failed=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rs*0.7)
                            tf=tfailed+ptf
                            
                            buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":member.guild.id})
                            sfailed=seller["woolongs"]
                            
                            sf=int(rs*0.3)
                            stf=sfailed+sf

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await self.client.ship.edit(embed=fail)

                       
                        if self.client.reply == 1:

                            if self.client.gacha%2 == 0:
                                
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
    

                            elif self.client.gacha%10 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})                              
                                tsuccess=success["woolongs"]

                                ten=int(5*payment)
                                tp=tsuccess+ten
                                
                                paid=discord.Embed(description=f"You have been paid {ten} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})

                                await self.client.ship.edit(embed=paid)
                                

                            elif self.client.gacha%15 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]
                                
                                fifteen=int(15*payment)
                                tp=tsuccess+fifteen

                                paid=discord.Embed(description=f"You have been paid {fifteen} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})
                                
                                await self.client.ship.edit(embed=paid)
                                

                            else:
                                payment=random.randint(25000,30000)

                                success=ranking.find_one({"id":member.id, "guild id":member.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":member.id, "guild id":member.guild.id},{"$set":{"woolongs":tp}})                            

                                await self.client.ship.edit(embed=paid)


    @commands.command()
    async def bank(self,ctx):
        id="804347400004173864"
        spike=ranking.find_one({"id":id, "guild id":ctx.guild.id})
        balance=spike["woolongs"]
        bal=discord.Embed(description=f"**Bank Of Solar System**\n **Woolongs: <:woolongs:952789606762438686> {balance}**", color=discord.Color.red())			
        bal.set_image(url=self.client.user.avatar_url)
        await ctx.reply(embed=bal)


    @commands.command()
    @commands.cooldown(1, 86400.0, commands.BucketType.user)
    async def steal(self,ctx,member:discord.Member):
        if member.id==self.client.user.id:
            await ctx.send("Stealing from a bank! Calling the ISSP!")
            return

        if member.id==ctx.author.id:
            await ctx.send("You can't trade with yourself!")
            return

        thief=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
        victim=ranking.find_one({"id":member.id, "guild id":ctx.guild.id})

        remove=random.randint(0,1000)

        profit=thief["woolongs"]+remove
        loss=victim["woolongs"]-remove

        thief=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":profit}})
        victim=ranking.update_one({"id":member.id, "guild id":ctx.guild.id},{"$set":{"woolongs":loss}})

        await ctx.send(f"{ctx.author.mention} stole {remove} from {member.mention}<:FeelsSmugMan:477783012172365864>")


    @commands.command()
    async def shop(self,ctx):
        buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.author.guild.id})
        seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.author.guild.id})


def setup(client):
  client.add_cog(Economy(client))