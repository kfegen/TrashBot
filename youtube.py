import asyncio

import discord
import youtube_dl
import ffmpeg
import globals

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

    async def joinDefault(self, ctx):
        """Joins a voice channel"""
        if ctx.voice_client is None:
            print(1)
            channel = discord.utils.get(ctx.message.guild.channels, name="Test", type="ChannelType.voice")
            print(channel)
            if channel is None:
                channel = discord.utils.get(ctx.message.guild.channels, name="*teleports behind you*", type="ChannelType.voice")
            print(channel)
            if channel is not None: 
                print("connecting")
                await channel.connect()

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await ctx.message.delete()
        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        self.joinDefault(ctx)

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.message.delete()

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def whosplayingbot(self, ctx):
        await ctx.send("Logan")

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        self.joinDefault(ctx)

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.message.delete()

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.message.delete()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def bruh(self, ctx):
        isalreadyConnected = True
        if ctx.voice_client is None: 
            isalreadyConnected = False
        self.joinDefault(ctx)

        async with ctx.typing():
            player = await YTDLSource.from_url("https://www.youtube.com/watch?v=2ZIpFytCSVc", loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.message.delete()

        await ctx.send("<:bruh:596482799280848896>")
        if isalreadyConnected == False:
            await ctx.voice_client.disconnect()
    
    @commands.command()
    async def bruhs(self, ctx):
        self.joinDefault(ctx)

        async with ctx.typing():
            player = await YTDLSource.from_url("https://www.youtube.com/watch?v=2ZIpFytCSVc", loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.message.delete()

        await ctx.voice_client.disconnect()

    @commands.command(pass_context=True)
    async def queue(self, ctx, *, url):
        self.joinDefault(ctx)

        async with ctx.typing():
            globals.streamQ.append(url)
            player = ctx.voice_client.create_ytdl_player(str(await globals.streamQ.get()), before_options=options)
            await ctx.message.delete()

            player.start()
            while not player.is_done():
                await asyncio.sleep(1)

        await ctx.send('Now playing: {}'.format(player.title))

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

