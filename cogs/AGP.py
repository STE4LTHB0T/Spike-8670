import discord, json, os, datetime, logging
from discord.ext import commands
from pytz import timezone

class AGP(commands.Cog):

  def __init__(self, client):
    self.client = client
    with open(os.path.join('./resources/ghost_ping.txt')) as file:
      self.data = json.load(file)

  @commands.Cog.listener()
  async def on_ready(self):
    print('Anti Ghost Ping is loaded!')

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    logging.info("Message Delete: %s", message)
    await self.parse(message)

  async def parse(self, message):
    pinged = []
    fields = {"User": message.author.mention, "Channel": message.channel.mention,"Message": message.content}
    if self.data["everyone"]:
      if message.mention_everyone:
        fields["Message @everyone"] = "Yes"
      pinged.append(bool(message.mention_everyone))
    if self.data["roles"]:
      if message.raw_role_mentions:
        fields["Role Mentions"] = ', '.join([discord.utils.get(message.guild.roles, id=i).name\
        for i in message.raw_role_mentions])
        pinged.append(bool(message.raw_role_mentions))
    if self.data["members"]:
      if message.raw_mentions:
        fields["Member Mentions"] = ', '.join([discord.utils.get(message.guild.members, id=i).name\
        for i in message.raw_mentions])
        pinged.append(bool(message.raw_mentions))
    if not any(pinged):
      return False
    embed = discord.Embed(title="Ghost Ping Detected:ghost:",color=0xff0000)
    for field in fields:
        embed.add_field(name=field, value=fields[field])
    embed.set_footer(text=f"Detected At: {datetime.datetime.now().astimezone(timezone('Asia/Kolkata')).strftime('%d/%m/%Y %H:%M:%S IST')}")
    embed.set_thumbnail(url=message.author.avatar_url)
    guild = message.guild
    log_channel = discord.utils.get(guild.text_channels, name="ghost-ping")
    await log_channel.send(embed=embed)
    return True
      
def setup(client):
  client.add_cog(AGP(client))