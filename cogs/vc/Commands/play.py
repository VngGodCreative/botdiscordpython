import discord
from discord.ext import commands
from pytube import YouTube, Playlist
import subprocess
import os
import asyncio
import json
import requests
from bs4 import BeautifulSoup

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist_file = os.path.join('data', "playlists.json")
        self.playlists = self.load_playlists()
        self.current_song = None
        self.queue = asyncio.Queue()
        self.loop = False
        self.loop_mode = None
        self.loop_playlist = None
        self.loop_song_index = None
        
        # Xác định đường dẫn tương đối đến thư mục chứa ffmpeg
        self.ffmpeg_executable = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin', 'ffmpeg.exe')

    def load_playlists(self):
        try:
            with open(self.playlist_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    async def play_music(self, ctx, url):
        try:
            audio_path = None
            if 'youtube.com/playlist' in url:
                # Đây là danh sách phát YouTube
                playlist = Playlist(url)
                for video_url in playlist.video_urls:
                    await self.queue.put((ctx, video_url))
                if not ctx.voice_client.is_playing():
                    next_ctx, next_url = await self.queue.get()
                    await self.play_music(next_ctx, next_url)
                return
            elif 'youtube.com' in url:
                yt = YouTube(url)
                stream = yt.streams.filter(only_audio=True).first()
                if not stream:
                    embed = discord.Embed(title="Lỗi", description="Không tìm thấy luồng âm thanh.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                audio_path = stream.download()
                self.current_song = {
                    "title": yt.title,
                    "artist": yt.author,
                    "thumbnail": yt.thumbnail_url
                }
            elif 'soundcloud.com' in url:
                audio_path = 'SoundCloud_Audio.mp3'
                subprocess.run(['youtube-dl', '-x', '--audio-format', 'mp3', '-o', audio_path, url])
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                title_tag = soup.find('h1', class_='sc-ellipsis-1-1')
                title = title_tag.text.strip() if title_tag else "Unknown Title"

                artist_tag = soup.find('a', class_='sc-link-1-1')
                artist = artist_tag.text.strip() if artist_tag else "Unknown Artist"

                thumbnail_tag = soup.find('img', class_='sc-image-1-1')
                thumbnail = thumbnail_tag['src'] if thumbnail_tag else None

                self.current_song = {
                    "title": title,
                    "artist": artist,
                    "thumbnail": thumbnail
                }
            elif 'cdn.discordapp.com' in url:
                audio_path = 'Discord_Audio.mp3'
                response = requests.get(url)
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                self.current_song = {
                    "title": "Discord Audio",
                    "artist": "Libraries Audio From Creative",
                    "thumbnail": ""
                }
            else:
                embed = discord.Embed(title="Lỗi", description="URL không hợp lệ.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            if not os.path.exists(audio_path):
                embed = discord.Embed(title="Lỗi", description="Tệp âm thanh không tồn tại.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            voice_client = ctx.voice_client
            if not voice_client or not voice_client.is_connected():
                embed = discord.Embed(title="Lỗi", description="Bot chưa tham gia vào voice channel.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            if not voice_client.is_playing():
                source = discord.FFmpegPCMAudio(audio_path, executable=self.ffmpeg_executable)
                voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.on_music_end(ctx, audio_path)))
                embed = discord.Embed(title=self.current_song["title"], description=f"Nghệ sĩ: {self.current_song['artist']}", color=0x00ff00)
                if self.current_song["thumbnail"]:
                    embed.set_thumbnail(url=self.current_song["thumbnail"])
                await ctx.send(embed=embed)
            else:
                await self.queue.put((ctx, url))

        except Exception as e:
            embed = discord.Embed(title="Lỗi", description=f"Lỗi tải thông tin track nhạc: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)

    async def on_music_end(self, ctx, audio_path):
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                print(f"Đã xóa file: {audio_path}")
            except FileNotFoundError:
                print(f"File {audio_path} không tồn tại.")
        
        if not self.queue.empty():
            next_ctx, next_url = await self.queue.get()
            await self.play_music(next_ctx, next_url)

    @commands.command(help="Chơi nhạc từ liên kết YouTube, SoundCloud, Discord hoặc từ playlist đã tạo trước đó")
    async def play(self, ctx, *, input: str):
        if ctx.author.voice is None:
            embed = discord.Embed(title="Lỗi", description="Bạn cần tham gia vào một voice channel trước.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)

        if any(substring in input for substring in ["youtube.com", "soundcloud.com", "cdn.discordapp.com"]):
            await self.play_music(ctx, input)
        else:
            if input not in self.playlists:
                embed = discord.Embed(title="Lỗi", description=f"Danh sách phát {input} không tồn tại.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            playlist = self.playlists[input]
            if not playlist:
                embed = discord.Embed(title="Lỗi", description=f"Danh sách phát {input} trống.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            for track in playlist:
                await self.queue.put((ctx, track))
            if not ctx.voice_client.is_playing():
                next_ctx, next_url = await self.queue.get()
                await self.play_music(next_ctx, next_url)

async def setup(bot):
    await bot.add_cog(PlayCommand(bot))