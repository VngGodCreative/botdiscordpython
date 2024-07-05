import discord
from discord.ext import commands
import asyncio

class ControlCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []
        self.loop = False  # Trạng thái lặp lại
        self.loop_mode = None  # Kiểu lặp lại (bài hát, danh sách nhạc)
        self.loop_playlist = None  # Danh sách nhạc để lặp lại
        self.loop_song_index = None  # Chỉ số bài hát trong danh sách nhạc để lặp lại

    @commands.command(help="Tạm dừng nhạc đang nghe")
    async def pause(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            embed = discord.Embed(title="Tạm dừng", description="Đã tạm dừng nhạc.", color=discord.Color.orange())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Lỗi", description="Không có nhạc đang phát.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(help="Tiếp tục nhạc đã tạm dừng trước đó")
    async def resume(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            embed = discord.Embed(title="Tiếp tục", description="Đã tiếp tục phát nhạc.", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Lỗi", description="Nhạc không bị tạm dừng.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(help="Chuyển sang bài tiếp theo")
    async def skip(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            embed = discord.Embed(title="Chuyển bài", description="Đã chuyển sang bài tiếp theo.", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Lỗi", description="Không có nhạc đang phát để chuyển.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(help="Phát lại bài trước đó")
    async def previous(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_connected():
            if self.song_queue:
                # Phát lại bài trước đó
                previous_song = self.song_queue.pop(-2)  # Lấy bài trước đó từ danh sách hàng đợi
                self.song_queue.append(previous_song)  # Đẩy bài hát lên đầu hàng đợi
                voice_client.stop()
                await ctx.send(f"Đang phát lại bài trước đó: {previous_song}")
                # Phát bài hát trước đó (cần chức năng phát nhạc của bạn để thực hiện việc này)
                await self.play_song(ctx, previous_song)
            else:
                embed = discord.Embed(title="Lỗi", description="Không có bài trước đó để phát lại.", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Lỗi", description="Bot chưa tham gia vào voice channel.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(help="Lặp lại nhạc")
    async def loop(self, ctx, *args):
        if len(args) == 0:
            self.loop = True
            self.loop_mode = "song"
            embed = discord.Embed(title="Lặp lại Bài Hát", description="Lặp lại bài hát hiện tại đã được bật.", color=discord.Color.green())
        elif len(args) == 1:
            playlist_name = args[0]
            self.loop = True
            self.loop_mode = "playlist"
            self.loop_playlist = playlist_name
            embed = discord.Embed(title="Lặp lại Danh Sách Nhạc", description=f"Lặp lại danh sách nhạc '{playlist_name}' đã được bật.", color=discord.Color.green())
        elif len(args) == 2:
            playlist_name = args[0]
            try:
                song_index = int(args[1])
                self.loop = True
                self.loop_mode = "playlist_song"
                self.loop_playlist = playlist_name
                self.loop_song_index = song_index
                embed = discord.Embed(title="Lặp lại Bài Hát Trong Danh Sách Nhạc", description=f"Lặp lại bài hát số {song_index} trong danh sách nhạc '{playlist_name}' đã được bật.", color=discord.Color.green())
            except ValueError:
                embed = discord.Embed(title="Lỗi", description="Số thứ tự bài hát không hợp lệ.", color=discord.Color.red())
        else:
            embed = discord.Embed(title="Lỗi", description="Cú pháp không hợp lệ.", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(help="Hủy lặp lại nhạc")
    async def unloop(self, ctx):
        self.loop = False
        self.loop_mode = None
        self.loop_playlist = None
        self.loop_song_index = None
        embed = discord.Embed(title="Hủy Lặp Lại", description="Chế độ lặp lại nhạc đã được hủy.", color=discord.Color.red())
        await ctx.send(embed=embed)

    async def play_song(self, ctx, song):
        # Hàm phát nhạc tùy theo cách triển khai của bạn
        # Giả sử sử dụng một hàm play với callback `after_song`
        voice_client = ctx.voice_client
        if not voice_client:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(song), after=lambda e: asyncio.run_coroutine_threadsafe(self.after_song(ctx), self.bot.loop))

    async def after_song(self, ctx):
        await self.play_next_song(ctx)

    async def play_next_song(self, ctx):
        if self.loop:
            if self.loop_mode == "song":
                # Lặp lại bài hát hiện tại
                await self.play_song(ctx, self.song_queue[-1])
            elif self.loop_mode == "playlist":
                # Lặp lại toàn bộ danh sách nhạc
                for song in self.song_queue:
                    await self.play_song(ctx, song)
            elif self.loop_mode == "playlist_song" and self.loop_playlist and self.loop_song_index is not None:
                # Lặp lại bài hát cụ thể trong danh sách nhạc
                if 0 <= self.loop_song_index < len(self.song_queue):
                    await self.play_song(ctx, self.song_queue[self.loop_song_index])
                else:
                    embed = discord.Embed(title="Lỗi", description="Chỉ số bài hát không hợp lệ.", color=discord.Color.red())
                    await ctx.send(embed=embed)
        else:
            # Phát bài hát tiếp theo trong hàng đợi nếu không lặp lại
            if self.song_queue:
                next_song = self.song_queue.pop(0)
                await self.play_song(ctx, next_song)

async def setup(bot):
    await bot.add_cog(ControlCommands(bot))