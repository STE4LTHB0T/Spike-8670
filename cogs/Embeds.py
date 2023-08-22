import discord, datetime, logging
from discord.ext import commands

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

class Embeds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Embeds is loaded!")

    @commands.hybrid_command(name = "invite", with_app_command = True, description = "Invite the bot to your server")
    async def invite(self,ctx):
        invite = discord.Embed(title = "Invite!", description = "Owner: **[STE4LTH_B0T](https://discordapp.com/users/463780399437447200)**", color = 0xff0000)
        invite.add_field(name = "Invite Link", value = "Click [here](https://discord.com/api/oauth2/authorize?client_id=804347400004173864&permissions=19235484462199&scope=bot%20applications.commands) to invite the bot to your server!", inline = False)
        invite.add_field(name = "Github Repo",value = "Click [here](https://github.com/STE4LTHB0T/Spike-8670) to visit the bot's repo!", inline = False)
        invite.set_thumbnail(url = self.client.user.avatar.url)
        await ctx.reply(embed = invite, ephemeral = False)

    @commands.hybrid_command(name = "id", with_app_command = True, description = "Shows the details of the user")
    async def id(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        created_time = member.created_at.timestamp()
        joined_time = member.joined_at.timestamp()
               
        data = discord.Embed(title = f"{member.name}", description = f"Info about {member.mention}", color = member.top_role.colour)
        data.add_field(name = "User ID", value = member.id, inline = False)
        data.add_field(name = "Top Role", value = member.top_role.mention, inline = False)
        data.add_field(name = "Created at", value =  f"<t:{int(created_time)}:F>", inline = False)
        data.add_field(name = "Joined at", value =  f"<t:{int(joined_time)}:F>", inline = False)
        data.add_field(name = "Nickname", value = member.nick, inline = False)
        data.set_thumbnail(url = member.display_avatar.url)
        data.set_footer(icon_url = ctx.author.avatar.url, text = f"Requested by {ctx.author.display_name}")
        await ctx.reply(embed = data, ephemeral = False)

    @commands.hybrid_command(name =  "records", with_app_command = True, description = "Pulls out the records of the server")
    async def records(self, ctx):

        guild_time = ctx.guild.created_at.timestamp()

        records = discord.Embed(title = f"{ctx.guild.name} Server Information", colour = ctx.guild.owner.colour)
        records.set_thumbnail(url = ctx.guild.icon.url)
        records.add_field(name = "Inter-Solar System Police Head", value = ctx.guild.owner.mention, inline = False)
        records.add_field(name = "Planet ID", value = ctx.guild.id, inline = False)
        records.add_field(name = "Created at", value = f"<t:{int(guild_time)}:F>", inline = False)
        records.add_field(name = "Bounty Roles", value = len(ctx.guild.roles), inline = False)
        records.add_field(name = "Available Bounties", value = len(list(filter(lambda m : not m.bot, ctx.guild.members))), inline = False)
        records.add_field(name = "Bounty News Announcers", value = len(list(filter(lambda m : m.bot, ctx.guild.members))), inline = False)
        records.add_field(name = "Bounty News Information", value = len(ctx.guild.text_channels), inline = False)
        records.add_field(name = "Bounty News Help", value = len(ctx.guild.voice_channels), inline = False)
        records.set_footer(icon_url = ctx.author.avatar.url, text = f"Informations for {ctx.author.display_name}")
        await ctx.reply(embed = records, ephemeral = False)

async def setup(client):
    await client.add_cog(Embeds(client))