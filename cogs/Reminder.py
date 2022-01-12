import discord, os, random, datetime
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime, timedelta

cluster = MongoClient(os.environ['MONGO'])

reminder = cluster["discord"]["reminder"]  


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd', 'w']:
            return (int(amount), unit)

        raise commands.BadArgument(message="Not a valid duration!")


class Reminder(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.reminder_task.start()

  @tasks.loop(minutes=1.0)
  async def reminder_task(self):
    reminds = reminder.find()
    for remind in reminds:
        now = datetime.now()
        temprt= remind["rt"]
        tempmem=remind["uid"]
        tempmsg=remind["message"]

        if now >= temprt:
          target = await self.client.fetch_user(tempmem)
          await target.send(f"This is a reminder for **{tempmsg}**")
          reminder.delete_one(remind)

  @commands.Cog.listener()
  async def on_ready(self):
    print('Reminder is loaded!')

  @commands.command()
  async def remind(self,ctx,time: DurationConverter,*,msg):
      number=random.randint(0, 50000)

      multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}
      amount, unit = time
      
      timer=amount * multiplier[unit]

      remindertime = datetime.now() + timedelta(seconds=timer)
      
      newremind={"_id":number, "name":ctx.author.name, "uid":ctx.author.id, "rt":remindertime, "message":msg}
      reminder.insert_one(newremind)
      
      await ctx.send(f"I'll remind you when the time comes!")


def setup(client):
  client.add_cog(Reminder(client))