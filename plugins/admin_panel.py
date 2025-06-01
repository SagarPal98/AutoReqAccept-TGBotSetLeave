import os
import sys
import time
import asyncio
import logging
import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, ChatJoinRequest, ChatMemberUpdated
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

from config import Config
from helper.database import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.OWNER))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))
    start_t = time.time()
    st = await message.reply('**Accessing bot details...**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000

    await st.edit(
        text=f"**--Bot Status--**\n\n"
             f"⏱ Uptime: `{uptime}`\n"
             f"📡 Ping: `{time_taken_s:.3f} ms`\n"
             f"👥 Users: `{total_users}`"
    )


@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.OWNER))
async def restart_bot(bot, message):
    await message.reply_text("🔄 Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("broadcast") & filters.user(Config.OWNER) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} started a broadcast.")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Broadcast started...")

    done = failed = success = 0
    total_users = await db.total_users_count()
    start_time = time.time()

    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(
                f"Broadcast Progress:\n"
                f"Total Users: {total_users}\n"
                f"Completed: {done}/{total_users}\n"
                f"✅ Success: {success}\n"
                f"❌ Failed: {failed}"
            )

    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"✅ Broadcast Completed in `{completed_in}`.\n\n"
        f"👥 Total Users: {total_users}\n"
        f"🎯 Delivered: {success}\n"
        f"❌ Failed: {failed}"
    )


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        return 400
    except Exception as e:
        logger.error(f"Error sending to {user_id}: {e}")
        return 500


@Client.on_chat_join_request()
async def auto_accept(bot: Client, cmd: ChatJoinRequest):
    chat = cmd.chat
    user = cmd.from_user

    try:
        await db.add_user(bot, user)
        await bot.approve_chat_join_request(chat.id, user.id)

        if await db.get_bool_approve_msg(Config.OWNER):
            text = await db.get_approve_msg(Config.OWNER) or Config.APPROVED_WELCOME_TEXT
            await bot.send_message(user.id, text.format(mention=user.mention, title=chat.title))
        else:
            print('Approval message is disabled.')

    except Exception as e:
        print('Error on line {}:'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)



@Client.on_chat_member_updated()
async def on_member_left(bot: Client, event: ChatMemberUpdated):
    try:
        chat = event.chat
        old_status = event.old_chat_member.status
        new_status = event.new_chat_member.status
        user = event.from_user

        # Detect if the user has left or was removed
        if old_status in ["member", "administrator"] and new_status in ["left", "kicked"]:
            # Check if leave message is enabled for the chat
            if await db.get_bool_leave_msg(Config.OWNER):  
                leavemsg = await db.get_leave_msg(Config.OWNER) or Config.LEAVING_BY_TEXT

                # Send the leave message to the chat
                await bot.send_message(
                    chat.id,
                    leavemsg.format(mention=user.mention, title=chat.title)
                )
            else:
                print("Leave message is disabled.")
    except Exception as e:
        import sys
        print('Error on line {}:'.format(sys.ex
