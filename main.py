import discord, os, platform, time, logging, asyncio
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv('./*.env')

client = commands.AutoShardedBot(command_prefix = ["spike ", "Spike "], intents = discord.Intents.all())

start_time = time.time()

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")
discord.utils.setup_logging(handler = handler)

cluster = MongoClient(os.environ["MONGO"])

statuses = cluster["discord"]["statuses"]

@client.event
async def on_ready():
    print("We have logged in as {0.user}!".format(client))
    await client.change_presence(activity=discord.Game(name="as an old-fashioned cowboy🚬"))

    for guild in client.guilds:
        print("Joined {}".format(guild.name))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("I cannot do that without the requirements!", ephemeral = False)

@client.event
async def on_guild_join(guild):
    new_server = {"Server Name" : guild.name, "id" : guild.id, "rank_system" : False}
    statuses.insert_one(new_server)

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Hello! My prefix is `spike <command>`. For help, check `spike help`!")
        break

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.reply("Shutting down the bot!")
    await client.close()

@client.hybrid_command(name = "data", with_app_command = True, description = "Tells you about the bot's data")
async def data(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))

    current_time = time.time()
    difference = int(round(current_time - start_time))
    ut = difference
    hours, remainder = divmod(ut, 3600)
    minutes, seconds = divmod(remainder, 60)

    data = discord.Embed(title = "Spike#8670's Data", color = 0xff0000)
    data.add_field(name = "Bot Version :", value = "v3.0", inline = True)
    data.add_field(name = "Python Version :", value = pythonVersion, inline = True)
    data.add_field(name = "Discord.Py Version :", value = dpyVersion, inline = True)
    data.add_field(name = "Total Guilds :", value = serverCount, inline = True)
    data.add_field(name = "Total Users :", value = memberCount, inline = True)
    data.add_field(name = "Uptime :", value = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)), inline = True)
    data.set_thumbnail(url = client.user.avatar.url)

    await ctx.reply(embed = data, ephemeral = False)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await client.start(os.getenv('TOKEN'))

asyncio.run(main())