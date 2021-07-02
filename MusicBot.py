import discord
from discord.channel import VoiceChannel
from discord.client import Client
import youtube_dl
from discord.ext import commands, tasks
from random import choice
import os

client=commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print("I am ready Shriya")

@client.command(name='hello', help='this command says hello')
async def hello(ctx):
    responses=["why did you wake me up!! 😴", "talk to my hand ✋", "Hii, how are you? 👼 "]
    await ctx.send(choice(responses))

@client.command(name='bye', help='this command says bye')
async def bye(ctx):
    responses=["bye, come back soon!! ❤️", "bye, i miss youu 😢", "get lost 😠"]
    await ctx.send(choice(responses))

@client.command(name='wassup', help='this command says wassup')
async def wassup(ctx):
    responses=["singing m hoon jiyaan 🎤 ", "about to sleep, wbu? 😪 ", "thinking of what to eat 🍕 "]
    await ctx.send(choice(responses))

@client.command(name="play", help="play music")
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    VoiceChannel = discord.utils.get(ctx.guild.voice_channels, name="Music")
    await VoiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command(name='leave', help='this command leaves')
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    
@client.command(name='pause', help='this command pause music')
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.pause()

@client.command(name='resume', help='this command resume music')
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()

@client.command(name='stop', help='this command stop music')
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voice.stop()
   
client.run('token') 




