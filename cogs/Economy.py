import discord, os, asyncio, datetime, random, typing
from discord.ext import commands
from pymongo import MongoClient
from resources.Lists import *


cluster = MongoClient(os.environ['MONGO'])

ranking = cluster["discord"]["bounty"]

transport = cluster["discord"]["personalships"]

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._cd = commands.CooldownMapping.from_cooldown(1, 43200.0, commands.BucketType.member)

    def get_ratelimit(self, ctx) -> typing.Optional[int]:
        bucket = self._cd.get_bucket(ctx)
        return bucket.update_rate_limit()        

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
    @commands.cooldown(1, 86400.0, commands.BucketType.member)
    async def daily(self,ctx):
        wage=random.randint(500,1000)
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
    async def give(self,ctx,member:discord.Member,woolong:int):
        if member.id==ctx.author.id:
            await ctx.send("You can't give Woolongs to yourself!")
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
            await message.edit(content=f"Giving {woolong} Woolongs to {member.mention} from {ctx.author.mention}")

            sender=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
            reciever=ranking.find_one({"id":member.id, "guild id":ctx.guild.id})

            send=sender["woolongs"]-woolong
            recieve=reciever["woolongs"]+woolong

            sender=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":send}})
            reciever=ranking.update_one({"id":member.id, "guild id":ctx.guild.id},{"$set":{"woolongs":recieve}})

            async with ctx.typing():
                await asyncio.sleep(0.5)
            await message.edit(content="Transaction successful!")


    @commands.command()
    async def bank(self,ctx):
        id="804347400004173864"
        spike=ranking.find_one({"id":id, "guild id":ctx.guild.id})
        balance=spike["woolongs"]
        bank=int(balance)
        bal=discord.Embed(description=f"**Bank Of Solar System**\n **Woolongs: <:woolongs:952789606762438686> {bank}**", color=discord.Color.red())			
        bal.set_image(url=self.client.user.avatar_url)
        await ctx.reply(embed=bal)

    @commands.command()
    @commands.cooldown(1, 259200.0, commands.BucketType.member)
    async def arrest(self,ctx,member:discord.Member):
        if member == self.client.user:
            await ctx.reply("You can't arrest me!")
            return
        if member.id == ctx.guild.owner.id:
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
            g_arrest = random.randint(0,1)
          
            if g_arrest == 0:
                await ctx.reply("The bounty escaped!")

            else:
                thief=ranking.find_one({"id":member.id, "guild id":ctx.guild.id})
                t_woolongs=thief["woolongs"]

                thiefremove=int(0.05*t_woolongs)
 
                r_woolongs = int(0.025*t_woolongs) #add money to bounty hunter

                s_woolongs = int(0.025*t_woolongs) #add money to spike

                tw = int(t_woolongs - thiefremove)

                sender=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                bh=sender["woolongs"]

                bounty_hunter = int(bh+r_woolongs)

                sender=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":bounty_hunter}})

                thief=ranking.update_one({"id":member.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tw}})

                spike=ranking.find_one({"id":"804347400004173864", "guild id":ctx.guild.id})
                balance=spike["woolongs"]
                bw=int(balance+s_woolongs)

                spike=ranking.update_one({"id": "804347400004173864", "guild id":member.guild.id},{"$set":{"woolongs":bw}})

                arrest = discord.Embed(description= f"{ctx.author.mention} is trying to arrest {member.mention}!\n You got {r_woolongs} for the helping the ISSP!", color=member.top_role.colour) 
                arrest.set_image(url=random.choice(arrest_reply))
                await ctx.reply(embed=arrest)


    @commands.command()
    @commands.cooldown(1, 86400.0, commands.BucketType.member)
    async def steal(self,ctx,member:discord.Member):
        if member.id==self.client.user.id:
            await ctx.send("Stealing from a bank! Calling the ISSP!")
            return

        if member.id == ctx.guild.owner.id:
            await ctx.reply("Stealing from the ISSP Head! Calling Security")
            return

        if member.id==ctx.author.id:
            await ctx.reply("You can't steal yourself!")
            return

        if member.id == 463780399437447200:
            await ctx.send("You can't steal from the bot owner!")
            return

        thief=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
        victim=ranking.find_one({"id":member.id, "guild id":ctx.guild.id})

        vwoolongs=victim["woolongs"]

        remove=random.randint(500,1000)

        if vwoolongs < remove:
            await ctx.send("Stop stealing from a broke person!")
        
        else:

            profit=thief["woolongs"]+remove
            loss=victim["woolongs"]-remove

            thief=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":profit}})
            victim=ranking.update_one({"id":member.id, "guild id":ctx.guild.id},{"$set":{"woolongs":loss}})

            await ctx.send(f"{ctx.author.mention} stole {remove} from {member.mention}<:FeelsSmugMan:477783012172365864>")


    #@commands.command()
    #async def shop(self,ctx):
        #buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.author.guild.id})
        #seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.author.guild.id})

    @commands.command()
    async def brochure(self,ctx):
        the_bebop = discord.Embed(title="The Bebop", description="The primary ship for your Inter-Solar System Travelling!", colour=discord.Colour.red())
        the_bebop.set_image(url="https://i.imgur.com/jhfy7Id.jpg")

        the_swordfish_ii = discord.Embed(title="The Swordfish II", description="A one-man racing spaceship equipped with latest artilleries!", colour=discord.Colour.red())
        the_swordfish_ii.set_image(url="https://i.imgur.com/9plvlUt.jpg")

        the_red_tail = discord.Embed(title="The Red Tail", description="An armed dogfighter with robotic pincers!", colour=discord.Colour.red())
        the_red_tail.set_image(url="https://i.imgur.com/XuPz0dJ.jpg")

        the_hammer_head = discord.Embed(title="The Hammer Head", description="A ship fixed with harpoon to tow or catch other ships!", colour=discord.Colour.red())
        the_hammer_head.set_image(url="https://i.imgur.com/V50qaT8.png")
        
        self.client.help_pages = [the_bebop, the_swordfish_ii, the_red_tail, the_hammer_head]

        buttons = [u"\u2B05", u"\u27A1"]
        current = 0
        msg = await ctx.send(embed=self.client.help_pages[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

                previous_page = current

                if reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                    elif current == 0:
                        current = 3

                    if current != previous_page:
                        await msg.edit(embed=self.client.help_pages[current])
                        await msg.remove_reaction(button, ctx.author)

                elif reaction.emoji == u"\u27A1":
                    if current < len(self.client.help_pages)-1:
                        current += 1
                    elif current == 3:
                        current = 0

                    if current != previous_page:
                        await msg.edit(embed=self.client.help_pages[current])
                        await msg.remove_reaction(button, ctx.author)

            except asyncio.TimeoutError:
                return print("test")
                

    """@commands.command()
    async def buyship(self,ctx, *, args):
        try:
            p_ship=transport.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
            if p_ship is None:
                newowner = {"name":ctx.author.name,"id":ctx.author.id, "guild id":ctx.guild.id, "guild name":ctx.guild.name, "The Bebop": False, "The Swordfish II": False, "The Red Tail": False, "The Hammerhead": False}
                transport.insert_one(newowner)
            else:
                bebop_check=p_ship["The Bebop"]

                if bebop_check == True:
                    await ctx.reply("You already own the ship!")
                else:
                    transport.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"The Bebop":True}})
                    await ctx.reply("Congrats!")

            if "The Swordfish II" in args:
                bebop_check=p_ship["The Bebop"]

                if bebop_check == True:
                    await ctx.reply("You already own the ship!")
                else:
                    b_price=500000
                    w_check=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                    woolongs_check=w_check["woolongs"]
                    if woolongs_check < b_price:
                        await ctx.reply("You are broke!")
                    else:
                        u_woolongs=woolongs_check - b_price
                        transport.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"The Bebop":True}})
                        ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":u_woolongs}})
                        await ctx.reply("Congrats!")

            if "The Red Tail" in args:
                bebop_check=p_ship["The Bebop"]

                if bebop_check == True:
                    await ctx.send("You already own the ship!")
                else:
                    transport.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"The Bebop":True}})
                    await ctx.send("Congrats!")

            if "The Hammer Head" in args:
                bebop_check=p_ship["The Bebop"]

                if bebop_check == True:
                    await ctx.send("You already own the ship!")
                else:
                    transport.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"The Bebop":True}})
                    await ctx.send("Congrats!")
        
        except:
            pass"""




    @commands.command()
    async def sell(self,ctx):

        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣'] # '7⃣', '8⃣', '9⃣']
        
        rembed=discord.Embed(title="Woolong Roles",description="Sell Woolongs for a role",color=discord.Color.red())
        rembed.add_field(name=':one: Komi-sama Cult', value='100000 Woolongs', inline=True)
        rembed.add_field(name=':two: Marin-sama Cult', value='100000 Woolongs', inline=True)
        rembed.add_field(name=':three: Monogatari Circlejerk', value='100000 Woolongs', inline=True)
        rembed.add_field(name=':four: Bot Na Cult', value='100000 Woolongs', inline=True)
        rembed.add_field(name=':five: XKami Cult', value='100000 Woolongs', inline=True)
        rembed.add_field(name=':six: The Mute Pass', value='250000 Woolongs', inline=True)
        rembed.set_thumbnail(url=self.client.user.avatar_url)
        
        msg=await ctx.send(embed=rembed)
        for reaction in reactions:
            await msg.add_reaction(reaction)
        
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in reactions, timeout=20.0)

                ksc = discord.utils.get(ctx.guild.roles, name='Komi-sama Cult')
                msc = discord.utils.get(ctx.guild.roles, name='Marin-sama Cult')
                mc = discord.utils.get(ctx.guild.roles, name='Monogatari Circlejerk')
                bnc = discord.utils.get(ctx.guild.roles, name='Bot Na Cult')
                xc = discord.utils.get(ctx.guild.roles, name='XKami Cult')
                tmp = discord.utils.get(ctx.guild.roles, name='The Mute Pass')

                re=discord.Embed(description=f"Role assigned!",color=discord.Color.red())
                check=discord.Embed(description="Role is already available for the user!",color=discord.Color.red())
                broke=discord.Embed(description="You are broke!",color=discord.Color.red())

                #Komi-san Cult

                if reaction.emoji == '1⃣':
                    if ksc in ctx.author.roles:
                        await msg.edit(embed=check, delete_after=5)

                    else:
                        rksc=100000
                        buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        temprksc=buyer["woolongs"]
                        if rksc>temprksc:
                            await msg.edit(embed=broke, delete_after=5)
                            return
                        else:
                            buying=buyer["woolongs"]-rksc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            selling=seller["woolongs"]+rksc

                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                            await ctx.author.add_roles(ksc)
                            await msg.edit(embed=re, delete_after=5)

                #Marin-sama Cult

                elif reaction.emoji == '2⃣':
                    if msc in ctx.author.roles:
                        await msg.edit(embed=check, delete_after=5)                    
                    else:
                        rmsc=100000
                        buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        temprmsc=buyer["woolongs"]
                        if rmsc>temprmsc:
                            await msg.edit(embed=broke, delete_after=5)
                            return
                        else:
                            buying=buyer["woolongs"]-rmsc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            selling=seller["woolongs"]+rmsc

                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                            await ctx.author.add_roles(msc)
                            await msg.edit(embed=re, delete_after=5)

                #Monogatari Circlejerk

                elif reaction.emoji == '3⃣': 
                    if mc in ctx.author.roles:
                        await msg.edit(embed=check, delete_after=5)
                    else:
                        rmc=100000
                        buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        temprmc=buyer["woolongs"]
                        if rmc>temprmc:
                            await msg.edit(embed=broke, delete_after=5)
                            return           
                        else:             
                            buying=buyer["woolongs"]-rmc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            selling=seller["woolongs"]+rmc

                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                            await ctx.author.add_roles(mc)
                            await msg.edit(embed=re, delete_after=5)

                #Bot Na Cult

                elif reaction.emoji == '4⃣':
                    if bnc in ctx.author.roles:
                        await msg.edit(embed=check, delete_after=5)
                    else:
                        rbnc=100000
                        buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        temprbnc=buyer["woolongs"]
                        if rbnc>temprbnc:
                            await msg.edit(embed=broke, delete_after=5)
                            return      
                        else:                  
                            buying=buyer["woolongs"]-rbnc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            selling=seller["woolongs"]+rbnc

                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                            await ctx.author.add_roles(bnc)
                            await msg.edit(embed=re, delete_after=5)

                #XKami Cult

                elif reaction.emoji == '5⃣':
                    if xc in ctx.author.roles:
                        await msg.edit(embed=check, delete_after=5)
                    else:
                        rxc=100000
                        buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        temprxc=buyer["woolongs"]
                        if rxc>temprxc:
                            await msg.edit(embed=broke, delete_after=5)
                            return
                        else:                        
                            buying=buyer["woolongs"]-rxc

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            selling=seller["woolongs"]+rxc

                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                            await ctx.author.add_roles(xc)
                            await msg.edit(embed=re, delete_after=5)                
                                        
                #The Mute Pass
                
                else:   
                    if tmp in ctx.author.roles:
                        await msg.edit(embed=check, delete_after=5)
                    else:
                        rtmp=250000
                        buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        temprtmp=buyer["woolongs"]
                        if rtmp>temprtmp:
                            await msg.edit(embed=broke, delete_after=5)
                            return       
                        else:                     
                            buying=buyer["woolongs"]-rtmp

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            selling=seller["woolongs"]+rtmp

                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})
                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                            await ctx.author.add_roles(tmp)
                            await msg.edit(embed=re, delete_after=5)

            except asyncio.TimeoutError:
                pass


    @commands.command()
    async def ship(self,ctx):

        if "check ratelimit":
            ratelimit = self.get_ratelimit(ctx)
        if ratelimit is None:        

            reply = random.randint(0,1)
            gacha = random.randint(0,500000)

            print(f'Reply:{reply}')
            print(f'Gacha:{gacha}')

            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣'] #['7⃣', '8⃣', '9⃣', '🔟']

            shipembed = discord.Embed(title="Ship Rent",description="Rent a ship to go to different place",color=discord.Color.red())
            shipembed.add_field(name=':one: Venus', value='25000 Woolongs', inline=True)
            shipembed.add_field(name=':two: Earth', value='15000 Woolongs', inline=True)
            shipembed.add_field(name=':three: Mars', value='150000 Woolongs', inline=True)
            shipembed.add_field(name=':four: Ganymede', value='25000 Woolongs', inline=True)
            shipembed.add_field(name=':five: Jupiter', value='35000 Woolongs', inline=True)
            shipembed.add_field(name=':six: Saturn', value='100000 Woolongs', inline=True)
            shipembed.set_thumbnail(url=self.client.user.avatar_url)

            ship=await ctx.send(embed=shipembed)

            for reaction in reactions:
                await ship.add_reaction(reaction)

        else:
            see_embed = discord.Embed(title="Ship Rent",description="Rent a ship to go to different place",color=discord.Color.red())
            see_embed.add_field(name=':one: Venus', value='25000 Woolongs', inline=True)
            see_embed.add_field(name=':two: Earth', value='15000 Woolongs', inline=True)
            see_embed.add_field(name=':three: Mars', value='150000 Woolongs', inline=True)
            see_embed.add_field(name=':four: Ganymede', value='25000 Woolongs', inline=True)
            see_embed.add_field(name=':five: Jupiter', value='35000 Woolongs', inline=True)
            see_embed.add_field(name=':six: Saturn', value='100000 Woolongs', inline=True)
            see_embed.set_thumbnail(url=self.client.user.avatar_url)            
            await ctx.send(embed=see_embed)

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in reactions, timeout=20.0)
                
                broke=discord.Embed(description="You are broke!",color=discord.Color.red())
                
                hunt=discord.Embed(description="Trying to capturing the bounty",color=discord.Color.red())

                #Venus
                if reaction.emoji == '1⃣':
                    await ship.clear_reaction(reaction.emoji)
                    rvenus=25000
                    buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                    temprvenus=buyer["woolongs"]

                    seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                    tempspike=seller["woolongs"]

                    print(f"Current amount for user:{temprvenus}")
                    print(f"Current amount for Spike:{tempspike}")
                    
                    
                    if rvenus>temprvenus:
                        await ship.edit(embed=broke, delete_after=5)
                        return                        
                    
                    else:
                        buy=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        buying=buy["woolongs"]-rvenus
                        buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})

                        print(f"Amount after buying for user:{buying}")

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                        selling=seller["woolongs"]+rvenus
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                        print(f"Amount after selling for spike:{selling}")

                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await ship.edit(embed=prep)
          
                        for reaction in reactions:
                            await ship.clear_reaction(reaction)                        
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Venus",color=discord.Color.red())
                        await ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await ship.edit(embed=hunt)

                       
                        if reply == 0:
                            failed=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rvenus*0.7)
                            tf=tfailed+ptf

                            print(f"Amount after failed for user:{tf}")
                            
                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            sfailed=seller["woolongs"]
                            
                            stf=sfailed-ptf

                            print(f"Amount after failed for spike:{stf}")

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await ship.edit(embed=fail, delete_after=5)

                
                        if reply == 1:

                            if gacha%5 == 0:
                                
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                print(f"Amount after 2x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
    

                            elif gacha%9 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})                              
                                tsuccess=success["woolongs"]

                                three=int(3*payment)
                                tp=tsuccess+three

                                print(f"Amount after 3x for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {three} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
                                

                            elif gacha%11 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]
                                
                                five=int(5*payment)
                                tp=tsuccess+five

                                print(f"Amount after 5x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {five} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})
                                
                                await ship.edit(embed=paid, delete_after=5)
                                

                            else:
                                payment=random.randint(25000,30000)

                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment

                                print(f"Amount after bounty for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})                            

                                await ship.edit(embed=paid, delete_after=5)
                                                            

                #Earth
                elif reaction.emoji == '2⃣':
                    await ship.clear_reaction(reaction.emoji)
                    rearth=15000
                    buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                    temprearth=buyer["woolongs"]

                    seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                    tempspike=seller["woolongs"]

                    print(f"Current amount for user:{temprearth}")
                    print(f"Current amount for Spike:{tempspike}")
                    
                    
                    if rearth>temprearth:
                        await ship.edit(embed=broke, delete_after=5)
                        return                        
                    
                    else:
                        buy=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        buying=buy["woolongs"]-rearth
                        buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})

                        print(f"Amount after buying for user:{buying}")

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                        selling=seller["woolongs"]+rearth
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                        print(f"Amount after selling for spike:{selling}")

                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await ship.edit(embed=prep)
          
                        for reaction in reactions:
                            await ship.clear_reaction(reaction)                        
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Earth",color=discord.Color.red())
                        await ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await ship.edit(embed=hunt)

                       
                        if reply == 0:
                            failed=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rearth*0.7)
                            tf=tfailed+ptf

                            print(f"Amount after failed for user:{tf}")
                            
                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            sfailed=seller["woolongs"]
                            
                            stf=sfailed-ptf

                            print(f"Amount after failed for spike:{stf}")

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await ship.edit(embed=fail, delete_after=5)

                
                        if reply == 1:

                            if gacha%5 == 0:
                                
                                payment=random.randint(15000,20000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                print(f"Amount after 2x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
    

                            elif gacha%9 == 0:
                                payment=random.randint(15000,20000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})                              
                                tsuccess=success["woolongs"]

                                three=int(3*payment)
                                tp=tsuccess+three

                                print(f"Amount after 3x for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {three} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
                                

                            elif gacha%11 == 0:
                                payment=random.randint(15000,20000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]
                                
                                five=int(5*payment)
                                tp=tsuccess+five

                                print(f"Amount after 5x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {five} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})
                                
                                await ship.edit(embed=paid, delete_after=5)
                                

                            else:
                                payment=random.randint(15000,20000)

                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment

                                print(f"Amount after bounty for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})                            

                                await ship.edit(embed=paid, delete_after=5)

                #Mars
                elif reaction.emoji == '3⃣':
                    await ship.clear_reaction(reaction.emoji)
                    rmars=150000
                    buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                    temprmars=buyer["woolongs"]

                    seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                    tempspike=seller["woolongs"]

                    print(f"Current amount for user:{temprmars}")
                    print(f"Current amount for Spike:{tempspike}")
                    
                    
                    if rmars>temprmars:
                        await ship.edit(embed=broke, delete_after=5)
                        return                        
                    
                    else:
                        buy=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        buying=buy["woolongs"]-rmars
                        buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})

                        print(f"Amount after buying for user:{buying}")

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                        selling=seller["woolongs"]+rmars
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                        print(f"Amount after selling for spike:{selling}")

                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await ship.edit(embed=prep)
          
                        for reaction in reactions:
                            await ship.clear_reaction(reaction)                        
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Mars",color=discord.Color.red())
                        await ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await ship.edit(embed=hunt)

                       
                        if reply == 0:
                            failed=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rmars*0.7)
                            tf=tfailed+ptf

                            print(f"Amount after failed for user:{tf}")
                            
                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            sfailed=seller["woolongs"]
                            
                            stf=sfailed-ptf

                            print(f"Amount after failed for spike:{stf}")

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await ship.edit(embed=fail, delete_after=5)

                
                        if reply == 1:

                            if gacha%5 == 0:
                                
                                payment=random.randint(150000,200000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                print(f"Amount after 2x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
    

                            elif gacha%9 == 0:
                                payment=random.randint(150000,200000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})                              
                                tsuccess=success["woolongs"]

                                three=int(3*payment)
                                tp=tsuccess+three

                                print(f"Amount after 3x for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {three} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
                                

                            elif gacha%11 == 0:
                                payment=random.randint(150000,200000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]
                                
                                five=int(5*payment)
                                tp=tsuccess+five

                                print(f"Amount after 5x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {five} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})
                                
                                await ship.edit(embed=paid, delete_after=5)
                                

                            else:
                                payment=random.randint(150000,200000)

                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment

                                print(f"Amount after bounty for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})                            

                                await ship.edit(embed=paid, delete_after=5)


                #Ganymede
                elif reaction.emoji == '4⃣':
                    await ship.clear_reaction(reaction.emoji)
                    rganymede=25000
                    buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                    temprganymede=buyer["woolongs"]

                    seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                    tempspike=seller["woolongs"]

                    print(f"Current amount for user:{temprganymede}")
                    print(f"Current amount for Spike:{tempspike}")
                    
                    
                    if rganymede>temprganymede:
                        await ship.edit(embed=broke, delete_after=5)
                        return                        
                    
                    else:
                        buy=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        buying=buy["woolongs"]-rganymede
                        buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})

                        print(f"Amount after buying for user:{buying}")

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                        selling=seller["woolongs"]+rganymede
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                        print(f"Amount after selling for spike:{selling}")

                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await ship.edit(embed=prep)
          
                        for reaction in reactions:
                            await ship.clear_reaction(reaction)                        
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Ganymede",color=discord.Color.red())
                        await ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await ship.edit(embed=hunt)

                       
                        if reply == 0:
                            failed=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rganymede*0.7)
                            tf=tfailed+ptf

                            print(f"Amount after failed for user:{tf}")
                            
                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            sfailed=seller["woolongs"]
                            
                            stf=sfailed-ptf

                            print(f"Amount after failed for spike:{stf}")

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await ship.edit(embed=fail, delete_after=5)

                
                        if reply == 1:

                            if gacha%5 == 0:
                                
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                print(f"Amount after 2x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
    

                            elif gacha%9 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})                              
                                tsuccess=success["woolongs"]

                                three=int(3*payment)
                                tp=tsuccess+three

                                print(f"Amount after 3x for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {three} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
                                

                            elif gacha%11 == 0:
                                payment=random.randint(25000,30000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]
                                
                                five=int(5*payment)
                                tp=tsuccess+five

                                print(f"Amount after 5x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {five} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})
                                
                                await ship.edit(embed=paid, delete_after=5)
                                

                            else:
                                payment=random.randint(25000,30000)

                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment

                                print(f"Amount after bounty for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})                            

                                await ship.edit(embed=paid, delete_after=5)
                                    
                #Jupiter
                elif reaction.emoji == '5⃣':
                    await ship.clear_reaction(reaction.emoji)
                    rjupiter=35000
                    buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                    temprjupiter=buyer["woolongs"]

                    seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                    tempspike=seller["woolongs"]

                    print(f"Current amount for user:{temprjupiter}")
                    print(f"Current amount for Spike:{tempspike}")
                    
                    
                    if rjupiter>temprjupiter:
                        await ship.edit(embed=broke, delete_after=5)
                        return                        
                    
                    else:
                        buy=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        buying=buy["woolongs"]-rjupiter
                        buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})

                        print(f"Amount after buying for user:{buying}")

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                        selling=seller["woolongs"]+rjupiter
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                        print(f"Amount after selling for spike:{selling}")

                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await ship.edit(embed=prep)
          
                        for reaction in reactions:
                            await ship.clear_reaction(reaction)                        
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Jupiter",color=discord.Color.red())
                        await ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await ship.edit(embed=hunt)

                       
                        if reply == 0:
                            failed=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rjupiter*0.7)
                            tf=tfailed+ptf

                            print(f"Amount after failed for user:{tf}")
                            
                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            sfailed=seller["woolongs"]
                            
                            stf=sfailed-ptf

                            print(f"Amount after failed for spike:{stf}")

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await ship.edit(embed=fail, delete_after=5)

                
                        if reply == 1:

                            if gacha%5 == 0:
                                
                                payment=random.randint(35000,40000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                print(f"Amount after 2x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
    

                            elif gacha%9 == 0:
                                payment=random.randint(35000,40000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})                              
                                tsuccess=success["woolongs"]

                                three=int(3*payment)
                                tp=tsuccess+three

                                print(f"Amount after 3x for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {three} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
                                

                            elif gacha%11 == 0:
                                payment=random.randint(35000,40000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]
                                
                                five=int(5*payment)
                                tp=tsuccess+five

                                print(f"Amount after 5x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {five} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})
                                
                                await ship.edit(embed=paid, delete_after=5)
                                

                            else:
                                payment=random.randint(35000,40000)

                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment

                                print(f"Amount after bounty for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})                            

                                await ship.edit(embed=paid, delete_after=5)


                #Saturn
                else:
                    await ship.clear_reaction(reaction.emoji)
                    rsaturn=100000
                    buyer=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                    temprsaturn=buyer["woolongs"]

                    seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                    tempspike=seller["woolongs"]

                    print(f"Current amount for user:{temprsaturn}")
                    print(f"Current amount for Spike:{tempspike}")
                    
                    
                    if rsaturn>temprsaturn:
                        await ship.edit(embed=broke, delete_after=5)
                        return                        
                    
                    else:
                        buy=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                        buying=buy["woolongs"]-rsaturn
                        buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":buying}})

                        print(f"Amount after buying for user:{buying}")

                        seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                        selling=seller["woolongs"]+rsaturn
                        seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":selling}})

                        print(f"Amount after selling for spike:{selling}")

                        
                        prep=discord.Embed(description="Prepping the ship for your work!",color=discord.Color.red())
                        
                        await ship.edit(embed=prep)
          
                        for reaction in reactions:
                            await ship.clear_reaction(reaction)                        
                        
                        await asyncio.sleep(0.5)
                        re=discord.Embed(description="Going to Saturn",color=discord.Color.red())
                        await ship.edit(embed=re)
                        await asyncio.sleep(0.5)
                        await ship.edit(embed=hunt)

                       
                        if reply == 0:
                            failed=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                            tfailed=failed["woolongs"]
                            
                            ptf=int(rsaturn*0.7)
                            tf=tfailed+ptf

                            print(f"Amount after failed for user:{tf}")
                            
                            buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tf}})

                            seller=ranking.find_one({"id": "804347400004173864", "guild id":ctx.guild.id})
                            sfailed=seller["woolongs"]
                            
                            stf=sfailed-ptf

                            print(f"Amount after failed for spike:{stf}")

                            seller=ranking.update_one({"id": "804347400004173864", "guild id":ctx.guild.id},{"$set":{"woolongs":stf}})

                            fail=discord.Embed(description=f"Your work has been failed! You have been reimbursed {ptf} Woolongs!",color=discord.Color.red())

                            await ship.edit(embed=fail, delete_after=5)

                
                        if reply == 1:

                            if gacha%5 == 0:
                                
                                payment=random.randint(100000,150000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                two=int(2*payment)
                                tp=tsuccess+two
                                
                                print(f"Amount after 2x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {two} Woolongs for your work!",color=discord.Color.green())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
    

                            elif gacha%9 == 0:
                                payment=random.randint(100000,150000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})                              
                                tsuccess=success["woolongs"]

                                three=int(3*payment)
                                tp=tsuccess+three

                                print(f"Amount after 3x for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {three} Woolongs for your work!",color=discord.Color.orange())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})

                                await ship.edit(embed=paid, delete_after=5)
                                

                            elif gacha%11 == 0:
                                payment=random.randint(100000,150000)
                                
                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]
                                
                                five=int(5*payment)
                                tp=tsuccess+five

                                print(f"Amount after 5x for user:{tp}")

                                paid=discord.Embed(description=f"You have been paid {five} Woolongs for your work!",color=discord.Color.blue())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})
                                
                                await ship.edit(embed=paid, delete_after=5)
                                

                            else:
                                payment=random.randint(100000,150000)

                                success=ranking.find_one({"id":ctx.author.id, "guild id":ctx.guild.id})
                                tsuccess=success["woolongs"]

                                tp=tsuccess+payment

                                print(f"Amount after bounty for user:{tp}")
                                
                                paid=discord.Embed(description=f"You have been paid {payment} Woolongs for your work!",color=discord.Color.red())

                                buyer=ranking.update_one({"id":ctx.author.id, "guild id":ctx.guild.id},{"$set":{"woolongs":tp}})                            

                                await ship.edit(embed=paid, delete_after=5)
                                

            except asyncio.TimeoutError:
                pass


def setup(client):
  client.add_cog(Economy(client))