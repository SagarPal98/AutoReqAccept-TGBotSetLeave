from datetime import datetime
from pytz import timezone
from config import Config
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def send_log(bot, user):
    if Config.LOG_CHANNEL:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')

        try:
            await bot.send_message(
                chat_id=Config.LOG_CHANNEL,
                text=(
                    f"**-- New User Started the Bot --**\n\n"
                    f"👤 **User**: {user.mention}\n"
                    f"🆔 **ID**: `{user.id}`\n"
                    f"🔗 **Username**: @{user.username if user.username else 'N/A'}\n"
                    f"🗓 **Date**: `{date}`\n"
                    f"⏰ **Time**: `{time}`"
                )
            )
        except Exception as e:
            logger.error(f"Error sending log message for user {user.id}: {e}")
