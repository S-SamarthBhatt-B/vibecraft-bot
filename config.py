import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --------------------
# Discord OAuth Config (for Flask web panel)
# --------------------
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://db.vibecraft.sbs/callback")
SECRET_KEY = os.getenv("FLASK_SECRET", "your-super-secret-key")
OAUTH_SCOPE = "identify guilds"
DISCORD_API_BASE_URL = "https://discord.com/api"

# --------------------
# Bot Config (for Discord bot)
# --------------------
PREFIXES = ["V!", "v!", "!!"]  # Multiple bot prefixes
DEFAULT_PREFIX = "V!"          # Used in embeds (help, info, etc.)
BOT_NAME = "VibeCraft"         # Display name for embeds
COLOR = 0x8E44AD               # Embed color (Vibrant Purple)

# Optional: Bot owner ID (used for developer-only commands)
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
