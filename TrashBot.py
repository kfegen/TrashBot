import os
import youtube
import globals
import discord
import random
import re
import uwuify


from discord.ext import commands
prefix = "!"
# global bot = commands.Bot(command_prefix=prefix)
globals.initialize(commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='TrashBot', case_insensitive=True))
bot = globals.bot
deleteMessage = False

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)
    emoji = discord.utils.get(bot.emojis, name='tiltproof')
    print(emoji)

@bot.command(help="who can it be?")
async def whoIsTheTraitor(ctx):
    await ctx.send("Its Logan... maybe Emily")

@bot.command()
async def fuckYouMatt(ctx):
    await ctx.send("Yes Fuck you Matt")

@bot.command(help="there is only one person we can count on to stay cool")
async def whoStaysCool(ctx):
    await ctx.send("<:tiltproof:741028686651719691> Its Logan <:tiltproof:741028686651719691> <@174733787182137345>")
    # for member in ctx.message.guild.members:
    #     print(member)
    #     print(member.id)

@bot.command(help="rolls a d20")
async def roll(ctx):
    randomnumber = random.randint(1, 20)
    await ctx.send(":game_die: " + str(randomnumber) + " :game_die: ")

@bot.command(help="im sorry for this abomination of a command")
async def uwu(ctx, content:str):
    await ctx.send(uwuify.uwu(content))

@bot.command()
async def noAnime(ctx):
    await ctx.send('https://media.tenor.com/images/5fd4212ffb6b24df9c186be39719223e/tenor.gif')
    ctx.message.delete()

@bot.command(help="chooses someone from the channel that Trashbot is currently in")
async def chooseOne(ctx):
    print(ctx.voice_client)
    # if ctx.voice_client is None:
    #     youtube.Music.joinDefault(self, ctx)
    if ctx.voice_client is not None:
        found = False
        while found == False and len(ctx.voice_client.channel.members) > 1:
            rand = random.randint(0, len(ctx.voice_client.channel.members) -1)
            user = ctx.voice_client.channel.members[rand]
            if user != bot.user: 
                found = True
                await ctx.send(":point_right: **" + user.name + " has been chosen**")

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

@bot.event
async def on_message(message):
    # print(message)
    if (message.author.bot == False):
        if(message.author.id == 174733787182137345):
            emoji = '\N{THUMBS UP SIGN}'
            await message.add_reaction(emoji)
            emoji = '\N{THUMBS DOWN SIGN}'
            await message.add_reaction(emoji)
        if(message.author.id == 174731616801914880): 
            #harass matt
            randomnumber = random.randint(1, 10)
            if randomnumber == 1:
                emoji = bot.get_emoji(583877834552901632)
                await message.add_reaction(emoji)
            if re.search('trashbot', message.content, re.IGNORECASE):
                emoji = bot.get_emoji(583877834552901632)
                await message.add_reaction(emoji)
            if re.search('trash', message.content, re.IGNORECASE) and re.search('bot', message.content, re.IGNORECASE):
                emoji = bot.get_emoji(583877834552901632)
                await message.add_reaction(emoji)
        if re.search('owie', message.content, re.IGNORECASE):
            emoji = bot.get_emoji(813783762017583139)
            await message.add_reaction(emoji)
    await bot.process_commands(message)
    

youtube.bot = bot
youtube.bot.add_cog(youtube.Music(bot))

youtube.bot.run('')  # Where 'TOKEN' is your bot token