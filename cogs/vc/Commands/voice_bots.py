import discord
from discord.ext import commands

class VoiceBots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Tham gia vào kênh voice hiện tại")
    async def join(self, ctx):
        if ctx.author.voice is None:
            embed = discord.Embed(title="Lỗi", description="Bạn cần tham gia vào một voice channel trước.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        voice_channel = ctx.author.voice.channel
        if voice_channel:
            if ctx.voice_client is None:
                await voice_channel.connect()
                embed = discord.Embed(title="Thành công", description=f"Đã tham gia vào {voice_channel.name}", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Thông báo", description="Bot đã tham gia vào voice channel.", color=discord.Color.blue())
                await ctx.send(embed=embed)

    @commands.command(help="Thoát khỏi kênh voice hiện tại và xóa tin nhắn liên quan")
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_connected():
            # Xóa tin nhắn lệnh gọi play và tin nhắn bot gửi tên music
            async for message in ctx.channel.history(limit=100):
                if message.author == ctx.author and message.content.startswith(ctx.prefix + 'play'):
                    await message.delete()
                elif message.author == self.bot.user and 'Nghệ sĩ' in message.content:
                    await message.delete()
            await voice_client.disconnect()
            embed = discord.Embed(title="Thành công", description="Đã rời khỏi voice channel.", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Lỗi", description="Bot chưa tham gia vào voice channel.", color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VoiceBots(bot))