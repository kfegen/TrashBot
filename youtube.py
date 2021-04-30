import asyncio
import discord
import youtube_dl
import ffmpeg
import globals
import threading

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @classmethod
    async def leavetimer(self, ctx):
        self.ctx = ctx
        await asyncio.sleep(1200)
        await self.ctx.voice_client.disconnect()

    async def joinDefault(self, ctx):
        """Joins a voice channel"""
        if ctx.voice_client is None:
            channel = discord.utils.get(ctx.message.guild.channels, name="Test", type="ChannelType.voice")
            print(channel)
            if channel is None:
                for ch in ctx.message.guild.channels:
                    if(ch.id == 420394425014026255):
                        channel = ch
                # channel = discord.utils.get(ctx.message.guild.channels, name="*teleports behind you*", type="ChannelType.voice")
                # channel = discord.utils.get(ctx.message.guild.channels, id=420394425014026254)
            print(channel)
            if channel is not None: 
                print("connecting")
                await channel.connect()
                await self.leavetimer(ctx)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(help="<channelName> Trashbot joins <channelName>")
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)

        await channel.connect()
        await self.hi(ctx)
        await self.leavetimer(ctx)

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command(help="<url> play from youtube")
    async def yt(self, ctx, *, url):
        try:
            """Plays from a url (almost anything youtube_dl supports)"""

            await self.joinDefault(ctx)

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.message.delete()
                await ctx.send('Now playing: {}'.format(player.title))
        except:
            print("An exception occurred")

    @commands.command(help="<url> play from youtube")
    async def stop(self, ctx, *, url):
        try:
            """Plays from a url (almost anything youtube_dl supports)"""

            await self.joinDefault(ctx)

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.message.delete()
                await ctx.send('Now playing: {}'.format(player.title))
        except:
            print("An exception occurred")

    @commands.command(help="<url> stream from url")
    async def stream(self, ctx, *, url):
        try:
            """Streams from a url (same as yt, but doesn't predownload)"""
            await self.joinDefault(ctx)

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.message.delete()

            await ctx.send('Now playing: {}'.format(player.title))
        except:
            print("An exception occurred")
        

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(help="stops playing and disconnects the bot")
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        try:
            async with ctx.typing():
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("bye.webm"))
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

        await ctx.message.delete()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def bruh(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=2ZIpFytCSVc", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.message.delete()

                await ctx.send("<:bruh:596482799280848896>")
        except:
            print("An exception occurred")
        
    
    @commands.command(help="a quieter more reserved Bruh (no emoji)")
    async def bruhs(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=2ZIpFytCSVc", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.message.delete()
        except:
            print("An exception occurred")

    @commands.command(pass_context=True, help="hello... trash!")
    async def hi(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://sound.peal.io/ps/audios/000/007/769/original/youtube_7769.mp3?1517524109", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")
        
    @commands.command(pass_context=True)
    async def bye(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("bye.webm"))
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command()
    async def whoisit(self, ctx):
        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("C:\\Users\\keval\\OneDrive\\Desktop\\DiscBot\\Hello who is it.mp3"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")
        await ctx.message.delete()

    @commands.command()
    async def owie(self, ctx):
        try:
            await self.joinDefault(ctx)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("C:\\Users\\keval\\OneDrive\\Desktop\\DiscBot\\owie.mp3"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command()
    async def beanswtf(self, ctx):
        try:
            await self.joinDefault(ctx)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("C:\\Users\\keval\\OneDrive\\Desktop\\DiscBot\\beanswtf.mp3"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")
        
    @commands.command(help="owie full version")
    async def owiel(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=e1pYQQKY6Gs", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command()
    async def no(self, ctx):
        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("C:\\Users\\keval\\OneDrive\\Desktop\\DiscBot\\no.m4a"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")
        await ctx.message.delete()
    
    @commands.command(pass_context=True)
    async def playingFactorio(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=b6SODkIzbn0", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command(pass_context=True)
    async def loveJesus(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=Vl6L8BDC_eg", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command(pass_context=True)
    async def baba(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=n7uc6W9qqVs", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command(pass_context=True, help="why thou?")
    async def spicy(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=VOHx7FdHE_0", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command(pass_context=True)
    async def war(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=5Ysj0wyTtsc", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")
    
    @commands.command(pass_context=True)
    async def openTheCountry(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=Cj1Tex6NfWQ", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")
    
    @commands.command(pass_context=True)
    async def gimmie(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=cfiPB8omuQQ", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @commands.command(pass_context=True, help="how bout you do it, anyway")
    async def doitanyway(self, ctx):
        try:
            await self.joinDefault(ctx)
            async with ctx.typing():
                player = await YTDLSource.from_url("https://www.youtube.com/watch?v=yWULCfJ2PGA", loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        except:
            print("An exception occurred")

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

# globals.initialize()
# bot = globals.bot

