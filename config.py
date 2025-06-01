import os, time, re

id_pattern = re.compile(r'^.\d+$') 

# Get FORCE_SUB first
FORCE_SUB = os.environ.get('FORCE_SUB', '')

# Decide AUTH_CHANNEL
if FORCE_SUB:
    if FORCE_SUB.startswith("-100") and FORCE_SUB[1:].isdigit():
        AUTH_CHANNEL = int(FORCE_SUB)
    elif FORCE_SUB.startswith("@"):
        AUTH_CHANNEL = FORCE_SUB
    else:
        AUTH_CHANNEL = None
else:
    AUTH_CHANNEL = None


class Config(object):
    # Client Config 
    API_ID = int(os.environ.get('API_ID', ''))  # ⚠️ Required
    API_HASH = os.environ.get('API_HASH', '')   # ⚠️ Required
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '') # ⚠️ Required

    # Database Config
    DB_URL = os.environ.get("DB_URL", "")  # ⚠️ Required

    # Other Config 
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")  # ⚠️ Required
    BOT_UPTIME = time.time()
    OWNER = int(os.environ.get('OWNER', ''))  # ⚠️ Required
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))  # ⚠️ Required
    APPROVED_WELCOME_TEXT = os.environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYou're Auto Approved. ✅")
    LEAVING_BY_TEXT = os.environ.get("APPROVED_WELCOME_TEXT", "👋 Bye {mention} !\nSee You Soon by {title}\n\nYou Left. ⛔")

    FORCE_SUB = FORCE_SUB
    AUTH_CHANNEL = AUTH_CHANNEL

    # Web response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


class Txt(object):
    START_MSG = """
🦁 Hᴇʟʟᴏ {} !,
I'ᴍ ᴀɴ ᴀᴜᴛᴏ Aᴘᴘʀᴏᴠᴀʟ Bᴏᴛ (Aᴅᴍɪɴ Jᴏɪɴ Rᴇǫᴜᴇsᴛ)

I ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴜsᴇʀs ɪɴ Gʀᴏᴜᴘ ᴏʀ Cʜᴀɴɴᴇʟs. Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ 💬
"""
