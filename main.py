import discord
from discord.ext import commands
import yt_dlp
import os # Ortam değişkenleri için

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}

ffmpeg_options = {
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'🚀 Bot Yayında: {bot.user.name}')

@bot.command(name='çal')
async def play(ctx, url: str):
    if ctx.author.voice is None:
        await ctx.send("Kanka önce bir ses kanalına gir!")
        return
    
    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            title = info.get('title', 'Müzik')

        vc = ctx.voice_client
        if vc.is_playing():
            vc.stop()
            
        # Bulut sunucularda 'executable' kısmına gerek kalmaz, ffmpeg yüklü gelir
        vc.play(discord.FFmpegPCMAudio(source=url2, **ffmpeg_options))
        await ctx.send(f"🎶 Çalıyor: **{title}**")
        
    except Exception as e:
        await ctx.send("❌ Bir hata oluştu!")
        print(f"Hata: {e}")

# Token'ı sistem değişkeninden çekiyoruz (Güvenlik için)
token = os.getenv('DISCORD_TOKEN')
bot.run(token)