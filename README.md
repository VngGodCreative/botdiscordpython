# DCS Creative BOT

DCS Creative BOT is a powerful Discord bot with multiple features for server management, user engagement, and entertainment. The bot is organized into several modules, each handling different aspects of functionality.

## Project Structure

```
project_root/
│
├── cogs/
│   ├── commands/
│   │   ├── __pycache__/
│   │   ├── admin/
│   │   │   ├── __pycache__/
│   │   │   ├── ban_unban.py
│   │   │   ├── clear.py
│   │   │   ├── mute_unmute.py
│   │   │   ├── reaction_role.py
│   │   │   ├── setup.py
│   │   │   ├── status.py
│   │   │   ├── cuop_emoji.py
│   │   │   ├── get_avatar.py
│   │   │   ├── help_command.py
│   │   │   ├── info_server.py
│   │   │   ├── info_user.py
│   │   │   ├── list_emoji.py
│   │   │   ├── ping.py
│   │   ├── events/
│   │   │   ├── __pycache__/
│   │   │   ├── ban.py
│   │   │   ├── booster_update.py
│   │   │   ├── bye.py
│   │   │   ├── counting.py
│   │   │   ├── member_update.py
│   │   │   ├── message_update.py
│   │   │   ├── server_update.py
│   │   │   ├── unban.py
│   │   │   ├── welcome.py
│   │   ├── utils/
│   │   │   ├── __pycache__/
│   │   │   ├── database_utils.py
│   │   ├── vc/
│   │       ├── music/
│   │       │   ├── __pycache__/
│   │       │   ├── Commands/
│   │       │   │   ├── __pycache__/
│   │       │   │   ├── control_music.py
│   │       │   │   ├── play.py
│   │       │   │   ├── playlist_management.py
│   │       │   │   ├── voice_bots.py
│   │       │   ├── music_cog.py
│   │   ├── voice/
│   │       ├── __pycache__/
│   │       ├── voice.py
│   ├── data/
│   │   ├── channel_ids.json
│   │   ├── database_utils.py
│   │   ├── playlists.db
│   │   ├── playlists.json
│   ├── utils/
│       ├── __pycache__/
│       ├── __init__.py
│       ├── common.py
│       ├── db.py
├── venv/
├── .env
├── main.py
├── readme.md
├── requirements.txt
├── Start.bat
```

## Features

### Admin Commands
- `ban_unban.py`: Commands to ban and unban users.
- `clear.py`: Command to clear messages.
- `mute_unmute.py`: Commands to mute and unmute users.
- `reaction_role.py`: Command to manage reaction roles.
- `setup.py`: Initial setup commands for the bot.
- `status.py`: Command to check the bot's status.
- `cuop_emoji.py`: Command related to emoji theft.
- `get_avatar.py`: Command to get user's avatar.
- `help_command.py`: Custom help command.
- `info_server.py`: Command to get server information.
- `info_user.py`: Command to get user information.
- `list_emoji.py`: Command to list all server emojis.
- `ping.py`: Command to check bot's latency.

### Event Listeners
- `ban.py`: Event listener for user bans.
- `booster_update.py`: Event listener for server boosts.
- `bye.py`: Event listener for user goodbyes.
- `counting.py`: Event listener for counting game.
- `member_update.py`: Event listener for member updates.
- `message_update.py`: Event listener for message updates.
- `server_update.py`: Event listener for server updates.
- `unban.py`: Event listener for user unbans.
- `welcome.py`: Event listener for welcoming new users.

### Music Commands
- `control_music.py`: Commands to control music playback.
- `play.py`: Command to play music.
- `playlist_management.py`: Commands to manage playlists.
- `voice_bots.py`: Commands for voice channel bots.
- `music_cog.py`: Main music cog handling music-related commands.

### Utility Commands
- `common.py`: Common utilities used across the bot.
- `db.py`: Database utilities.

## Setup and Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/vnggodcreative/botdiscordpython.git
   cd botdiscordpython
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Create a `.env` file in the project root and add your configuration variables (e.g., bot token, database credentials).

6. **Run the bot:**
   ```sh
   python main.py
   ```

## Permissions and Role Checks

The bot uses several decorators to check for permissions and roles. Ensure you have the necessary roles and permissions set up in your Discord server.

### Decorators
- `@commands.is_owner()`
- `@is_admin()`
- `@has_any_role(yeu_cau_roles)`
- `@has_any_role_or_owner(yeu_cau_roles)`
- `@has_permissions_or_owner(administrator=True)`
- `@commands.has_permissions(administrator=True)`
- `@commands.has_permissions(moderate_members=True)`
- `@commands.has_permissions(ban_members=True)`
- `@commands.has_permissions(kick_members=True)`
- `@commands.has_permissions(manage_emojis=True)`

### Permission Check Functions
Ensure the following functions are defined in your bot to handle custom permission checks:

```python
def has_any_role_or_owner(role_ids):
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True
        for role_id in role_ids:
            role = discord.utils.get(ctx.author.roles, id=role_id)
            if role is not None:
                return True
        raise commands.MissingRole(role_ids)
    return commands.check(predicate)

def has_permissions_or_owner(**perms):
    async def predicate(ctx):
        if ctx.author.id == ctx.bot.owner_id:
            return True
        resolved = ctx.channel.permissions_for(ctx.author)
        return all(getattr(resolved, name, None) == value for name, value in perms.items())
    return commands.check(predicate)

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check

(predicate)
```

## Contributing

Feel free to fork this repository, make changes, and submit pull requests. All contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Thank you for using DCS Creative BOT! If you have any questions or need assistance, please reach out to [vnggodcreative@gmail.com](mailto:vnggodcreative@gmail.com).
