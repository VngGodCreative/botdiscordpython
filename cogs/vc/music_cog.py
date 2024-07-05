import asyncio
import json
import os
import sqlite3
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist_file = os.path.join('data', "playlists.json")
        self.db_file = os.path.join('data', "playlists.db")
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                songs TEXT
            )
        """)
        self.playlists = self.load_playlists()
        self.sync_playlists()

    def load_playlists(self):
        try:
            with open(self.playlist_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def sync_playlists(self):
        for playlist_name, songs in self.playlists.items():
            songs_json = json.dumps(songs)
            self.cursor.execute("""
                INSERT OR REPLACE INTO playlists (name, songs)
                VALUES (?, ?)
            """, (playlist_name, songs_json))
        self.conn.commit()

    async def delete_audio(self, audio_path, voice_client):
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        await asyncio.sleep(1)
        try:
            os.remove(audio_path)
            print(f"Đã xóa file: {audio_path}")
        except FileNotFoundError:
            print(f"File {audio_path} không tồn tại.")

    def delete_audio_sync(self, audio_path, voice_client):
        asyncio.run_coroutine_threadsafe(self.delete_audio(audio_path, voice_client), self.bot.loop)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user and not after.channel:
            if self.bot.voice_clients:
                voice_client = self.bot.voice_clients[0]
                for filename in os.listdir("."):
                    if filename.endswith(".mp3") or filename.endswith(".wav"):
                        await self.delete_audio(filename, voice_client)

async def setup(bot):
    await bot.add_cog(Music(bot))