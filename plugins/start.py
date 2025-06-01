import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import Txt, Config
from helper.database import db

# 🌐 Global Buttons
btn1 = InlineKeyboardButton('✅ Approval Message On', callback_data='approvalmsg_on')
btn2 = InlineKeyboardButton('❌ Approval Message Off', callback_data='approvalmsg_off')
btn4 = InlineKeyboardButton('✅ Leaving Message On', callback_data='leavingmsg_on')
btn3 = InlineKeyboardButton('❌ Leaving Message Off', callback_data='leavingmsg_off')


@Client.on_message(filters.private & filters.command('start'))
async def start_message(bot: Client, msg: Message):
    user = msg.from_user
    await db.add_user(bot, user)

    bot_username = (await bot.get_me()).username  # Get bot username dynamically

    await msg.reply_text(
        text=Txt.START_MSG.format(user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('👨‍💻 Developer', url='https://t.me/TgMaster_Bots')],
            [
                InlineKeyboardButton(
                    '➕ 𝖠𝖽𝖽 𝖳𝗈 𝖢𝗁𝖺𝗇𝗇𝖾𝗅',
                    url=f'https://t.me/{bot_username}?startchannel=true&admin=invite_users+manage_chat+delete_messages+restrict_members'
                ),
                InlineKeyboardButton(
                    '👥 𝖠𝖽𝖽 𝖳𝗈 𝖦𝗋𝗈𝗎𝗉',
                    url=f'https://t.me/{bot_username}?startgroup=true&admin=invite_users+manage_chat+delete_messages+restrict_members'
                )
            ]
        ])
    )



@Client.on_message(filters.private & filters.command(['setting', 'config']) & filters.user(Config.OWNER))
async def settings(bot: Client, msg: Message):
    SnowDev = await msg.reply_text('Please Wait ⏳')
    bool_approve = await db.get_bool_approve_msg(msg.from_user.id)
    bool_leave = await db.get_bool_leave_msg(msg.from_user.id)

    markup = [
        [btn1 if bool_approve else btn2],
        [btn4 if bool_leave else btn3]
    ]

    await SnowDev.edit(
        text="**Your Approval and Leaving Message Settings ⚙️**",
        reply_markup=InlineKeyboardMarkup(markup)
    )


@Client.on_callback_query()
async def query(bot: Client, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id

    if data.startswith('approvalmsg'):
        value = data.split('_')[1] == 'off'
        await db.set_bool_approve_msg(chat_id, value)

    elif data.startswith('leavingmsg'):
        value = data.split('_')[1] == 'off'
        await db.set_bool_leave_msg(chat_id, value)

    # Refresh settings after update
    bool_approve = await db.get_bool_approve_msg(chat_id)
    bool_leave = await db.get_bool_leave_msg(chat_id)
    markup = [
        [btn1 if bool_approve else btn2],
        [btn4 if bool_leave else btn3]
    ]

    await query.message.edit(
        text="**Your Approval and Leaving Message Settings ⚙️**",
        reply_markup=InlineKeyboardMarkup(markup)
    )


@Client.on_message(filters.private & filters.command('set_approvemsg') & filters.user(Config.OWNER))
async def set_approve_msg(bot: Client, msg: Message):
    if msg.reply_to_message:
        ms = await msg.reply_text("Please Wait...")
        await db.set_approve_msg(msg.from_user.id, msg.reply_to_message.text)
        await ms.edit("**Successfully Added ✅**")
        await asyncio.sleep(3)
        await ms.delete()
    else:
        await msg.reply_text("Reply to a message.\nSupports only text and HTML format.\n\nExample:\n`Hi {mention}, your request for {title} has been approved!`")


@Client.on_message(filters.private & filters.command('set_leavemsg') & filters.user(Config.OWNER))
async def set_leave_msg(bot: Client, msg: Message):
    if msg.reply_to_message:
        ms = await msg.reply_text("Please Wait...")
        await db.set_leave_msg(msg.from_user.id, msg.reply_to_message.text)
        await ms.edit("**Successfully Added ✅**")
        await asyncio.sleep(3)
        await ms.delete()
    else:
        await msg.reply_text(
            "Reply to a message.\nSupports only text and HTML format.\n\n"
            "Example:\n`Goodbye {mention}, we will miss you at {title}!`"
        )
