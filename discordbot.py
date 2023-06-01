import discord
from discord.ext import commands
from pytube import YouTube

#FİRST ENTER YOUR DİSCORD TOKEN
TOKEN = 'TOKEN'

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} entered the chat.')

@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send('First you need to join a voice channel.')
        return

    voice_channel = ctx.author.voice.channel
    voice_client = ctx.voice_client

    if voice_client and voice_client.is_connected():
        await voice_client.move_to(voice_channel)
    else:
        voice_client = await voice_channel.connect()

    try:
        youtube = YouTube(url)
        video = youtube.streams.get_audio_only()
        source = await discord.FFmpegOpusAudio.from_probe(video.url)
        voice_client.play(source)
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send('Leaving voice channel.')

bot.run(TOKEN)
