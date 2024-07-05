import discord
from discord.ext import commands
import json
import os

class PlaylistManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist_file = os.path.join('data', "playlists.json")
        self.playlists = self.load_playlists()

    def load_playlists(self):
        try:
            with open(self.playlist_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_playlists(self):
        with open(self.playlist_file, "w") as f:
            json.dump(self.playlists, f)

    @commands.command(help="Tạo Playlist nhạc")
    async def createpl(self, ctx, playlist_name):
        try:
            if playlist_name in self.playlists:
                embed = discord.Embed(title="Lỗi", description=f"Danh sách phát {playlist_name} đã tồn tại.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            self.playlists[playlist_name] = []
            embed = discord.Embed(title="Thành công", description=f"Danh sách phát {playlist_name} đã được tạo.", color=discord.Color.green())
            await ctx.send(embed=embed)
            self.save_playlists()
        except Exception as e:
            embed = discord.Embed(title="Lỗi", description=f"Lỗi tạo danh sách phát: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(help="Thêm nhạc vào danh sách phát\nCú pháp: ?addpl (tên Playlist) (tên nhạc hoặc URL)")
    async def addpl(self, ctx, playlist_name, *song_names):
        try:
            if playlist_name not in self.playlists:
                embed = discord.Embed(title="Lỗi", description=f"Danh sách phát {playlist_name} không tồn tại.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            self.playlists[playlist_name].extend(song_names)
            embed = discord.Embed(title="Thành công", description=f"Bài hát đã được thêm vào danh sách phát {playlist_name}.", color=discord.Color.green())
            await ctx.send(embed=embed)
            self.save_playlists()
        except Exception as e:
            embed = discord.Embed(title="Lỗi", description=f"Lỗi thêm bài hát: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(help="Lấy danh sách phát đã có hoặc danh sách bài hát trong một danh sách phát\nCú pháp: ?getpl (tùy chọn: tên Playlist)")
    async def getpl(self, ctx, playlist_name=None):
        try:
            if playlist_name is None:
                if not self.playlists:
                    embed = discord.Embed(title="Thông báo", description="Hiện không có danh sách phát nào.", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    return
                
                embed = discord.Embed(title="Danh sách các Playlist", color=discord.Color.blue())
                for name in self.playlists:
                    embed.add_field(name=name, value="Danh sách bài hát có sẵn", inline=False)
                await ctx.send(embed=embed)
            else:
                if playlist_name not in self.playlists:
                    embed = discord.Embed(title="Lỗi", description=f"Danh sách phát {playlist_name} không tồn tại.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                songs = self.playlists[playlist_name]
                if not songs:
                    embed = discord.Embed(title="Thông báo", description=f"Danh sách phát {playlist_name} trống.", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    return
                embed = discord.Embed(title=f"Danh sách bài hát trong {playlist_name}", color=discord.Color.green())
                for i, song in enumerate(songs, 1):
                    embed.add_field(name=f"Bài hát {i}", value=song, inline=False)
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Lỗi", description=f"Lỗi lấy danh sách phát: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(help="Xóa một danh sách phát hoặc bài hát trong danh sách phát\nCú pháp: ?deletepl (tên Playlist) (bài hát số thứ tự)")
    async def deletepl(self, ctx, playlist_name, song_index=None):
        try:
            if playlist_name not in self.playlists:
                embed = discord.Embed(title="Lỗi", description=f"Danh sách phát {playlist_name} không tồn tại.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            if song_index is None:
                del self.playlists[playlist_name]
                embed = discord.Embed(title="Thành công", description=f"Danh sách phát {playlist_name} đã được xóa.", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                try:
                    song_index = int(song_index)
                    del self.playlists[playlist_name][song_index - 1]
                    embed = discord.Embed(title="Thành công", description=f"Bài hát số {song_index} trong danh sách phát {playlist_name} đã được xóa.", color=discord.Color.green())
                    await ctx.send(embed=embed)
                except (ValueError, IndexError):
                    embed = discord.Embed(title="Lỗi", description=f"Số thứ tự bài hát không hợp lệ.", color=discord.Color.red())
                    await ctx.send(embed=embed)
            self.save_playlists()
        except Exception as e:
            embed = discord.Embed(title="Lỗi", description=f"Lỗi xóa danh sách phát: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PlaylistManagement(bot))