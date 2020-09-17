import os
import youtube
import globals
import discord
import random

from discord.ext import commands
prefix = "!"
# global bot = commands.Bot(command_prefix=prefix)
globals.initialize(commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='TrashBot', case_insensitive=True))
bot = globals.bot
deleteMessage = False


# @bot.event
# async def on_message(message):
#     print("The message's content was", message.content)
#     await bot.process_commands(message)

@bot.command()
async def h(ctx):
    '''
    This text will be shown in the help command
    '''

    message = str("```Availiable commands:\n" +
    "Music: \n" +
    "   !yt <url> play from youtube\n" +
    "   !stream <url> stream from url\n" +
    "   !stop stops playing and disconnects the bot\n" +
    "   !join <channelName> Trashbot joins <channelName>\n"
    "Other:\n" +
    "   !bruh BRUH\n" +
    "   !bruhs a quieter more reserved Bruh (no emoji)\n" +
    "   !roll rolls a d20\n" +
    "   !chooseOne chooses someone from the channel that Trashbot is currently in\n"
    "Trash Related:\n" +
    "   !whoIsTheTraitor who can it be?\n" +
    "   !whoStaysCool there is only one person we can count on to stay cool" +
    "```")
    
    # style = discord.Embed(name="responding quote", description="- "+message)
    # await bot.send(embed=style)
    await ctx.send(message)

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)
    emoji = discord.utils.get(bot.emojis, name='tiltproof')
    print(emoji)

@bot.command()
async def whoIsTheTraitor(ctx):
    await ctx.send("Its Logan... maybe Emily")

@bot.command()
async def fuckYouMatt(ctx):
    await ctx.send("Yes Fuck you Matt")

@bot.command()
async def whoStaysCool(ctx):
    await ctx.send("<:tiltproof:741028686651719691> Its Logan <:tiltproof:741028686651719691> <@174733787182137345>")
    # for member in ctx.message.guild.members:
    #     print(member)
    #     print(member.id)

@bot.command()
async def roll(ctx):
    randomnumber = random.randint(1, 20)
    await ctx.send(":game_die: " + str(randomnumber) + " :game_die: ")

@bot.command()
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

youtube.bot = bot
youtube.bot.add_cog(youtube.Music(bot))

youtube.bot.run('<>')  # Where 'TOKEN' is your bot token

