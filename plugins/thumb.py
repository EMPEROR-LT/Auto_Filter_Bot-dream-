import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS
from database.users_chats_db import db
from plugins.monkey_patch import clear_thumb_cache

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("set_thumb") & filters.user(ADMINS))
async def set_thumb(client, message: Message):
    """Set global thumbnail for the bot"""
    reply = message.reply_to_message
    if reply and reply.photo:
        thumb_id = reply.photo.file_id
    elif message.photo:
        thumb_id = message.photo.file_id
    else:
        return await message.reply_text("<b>ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ sᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ ᴡɪᴛʜ /set_thumb ᴛᴏ sᴇᴛ ᴀ ᴛʜᴜᴍʙɴᴀɪʟ.</b>")

    await db.update_bot_setting(client.me.id, "BOT_THUMB", thumb_id)
    clear_thumb_cache()
    await message.reply_text("<b>✅ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ!</b>")

@Client.on_message(filters.command("view_thumb") & filters.user(ADMINS))
async def view_thumb(client, message: Message):
    """View current global thumbnail"""
    thumb = await db.get_bot_setting(client.me.id, "BOT_THUMB", None)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb, caption="<b>ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴀᴠᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ.</b>")
    else:
        await message.reply_text("<b>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ.</b>")

@Client.on_message(filters.command("del_thumb") & filters.user(ADMINS))
async def del_thumb(client, message: Message):
    """Delete global thumbnail"""
    thumb = await db.get_bot_setting(client.me.id, "BOT_THUMB", None)
    if not thumb:
        return await message.reply_text("<b>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ.</b>")

    await db.delete_bot_setting(client.me.id, "BOT_THUMB")
    clear_thumb_cache()
    await message.reply_text("<b>✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ!</b>")
