import discord
from discord.ext import commands
import os
import sys
from Constants import *

#ffmpeg
FFMPEG_PATH = "\\".join(sys.argv[0].split("\\")[:-1]) + "\\ffmpeg\\ffmpeg.exe"
print(f"FFMPEG at {FFMPEG_PATH}")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Folder to store temporary audio files
AUDIO_DIR = "audio_uploads"
os.makedirs(AUDIO_DIR, exist_ok=True)

def end_playback(path):
    os.remove(path)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    """Joins the user's voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"נכנס ל{channel}🌚, היכון לבואי חבוב")
    else:
        await ctx.send("גבר voice channel אתה לא בשום💔")

@bot.command()
async def leave(ctx):
    """Leaves the current voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ביי פוקי בר")
    else:
        await ctx.send("😘 אני צריך להיכנס קודם גבר")

@bot.command()
async def play(ctx):
    """Plays an audio file — either default or from an uploaded MP3."""
    voice_client = ctx.voice_client

    # Ensure bot is in the voice channel
    if not voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("גבר voice channel אתה לא בשום💔")
            return

    # Stop any current playback
    if voice_client.is_playing():
        voice_client.stop()

    # Check for attachment
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if not attachment.filename.lower().endswith(".mp3"):
            await ctx.send("⚠️ תביא לי קובץ אודיו נורמלי גבר")
            return

        file_path = os.path.join(AUDIO_DIR, attachment.filename)
        await attachment.save(file_path)
        await ctx.send(f"🎵 קיבלתי את `{attachment.filename}`, מנגן...")
    else:
        # Default fallback file
        file_path = "song.mp3"
        if not os.path.exists(file_path):
            await ctx.send("⚠️ No default song found! Upload an MP3 instead.")
            return
        await ctx.send(f"🎶 Playing default file `{file_path}`")

    # Play the chosen file
    source = discord.FFmpegPCMAudio(file_path, executable=FFMPEG_PATH)
    voice_client.play(source, after=end_playback(path=file_path))

@bot.command()
async def stop(ctx):
    """Stops playback."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped playback.")
    else:
        await ctx.send("Nothing is playing right now.")

bot.run(BOT_TOKEN)
