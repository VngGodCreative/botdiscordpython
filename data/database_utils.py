import sqlite3
from discord.ext import commands
import os

class DatabaseUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join('data', 'playlist.db')  # Đường dẫn đến tệp cơ sở dữ liệu
        self.conn = None
        self.create_tables()

    def create_connection(self):
        """Kết nối đến cơ sở dữ liệu SQLite."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            print(f"Kết nối đến cơ sở dữ liệu tại {self.db_path}")
        except sqlite3.Error as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return self.conn

    def create_tables(self):
        """Tạo các bảng trong cơ sở dữ liệu nếu chưa tồn tại."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    join_date TEXT NOT NULL
                                  );''')
                conn.commit()
                print("Bảng users đã được tạo hoặc đã tồn tại.")
            except sqlite3.Error as e:
                print(f"Lỗi khi tạo bảng: {e}")
            finally:
                conn.close()

    @commands.command(name='add_user')
    async def add_user(self, ctx, user_id: int, name: str, join_date: str):
        """Thêm một người dùng vào cơ sở dữ liệu."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (id, name, join_date) VALUES (?, ?, ?)', (user_id, name, join_date))
                conn.commit()
                await ctx.send(f"Đã thêm người dùng {name} vào cơ sở dữ liệu.")
            except sqlite3.Error as e:
                await ctx.send(f"Lỗi khi thêm người dùng: {e}")
            finally:
                conn.close()

    @commands.command(name='get_user')
    async def get_user(self, ctx, user_id: int):
        """Lấy thông tin người dùng từ cơ sở dữ liệu."""
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                user = cursor.fetchone()
                if user:
                    await ctx.send(f"ID: {user[0]}, Name: {user[1]}, Join Date: {user[2]}")
                else:
                    await ctx.send("Không tìm thấy người dùng.")
            except sqlite3.Error as e:
                await ctx.send(f"Lỗi khi lấy thông tin người dùng: {e}")
            finally:
                conn.close()

async def setup(bot):
    await bot.add_cog(DatabaseUtils(bot))