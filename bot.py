#!/usr/bin/env python3
"""
Auto Rename Bot - Complete Version
Users set media format first, then all files are processed accordingly
"""

import os
import re
import sys
import time
import json
import math
import asyncio
import logging
import datetime
import shutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageOps
import motor.motor_asyncio
from pyrogram import Client, filters, __version__
from pyrogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, 
    CallbackQuery
)
from pyrogram.errors import (
    FloodWait, InputUserDeactivated, UserIsBlocked, 
    PeerIdInvalid
)

# Load environment variables
load_dotenv()

# ==================== CONFIGURATION ====================
class Config:
    API_ID = int(os.getenv("API_ID", "25775944"))
    API_HASH = os.getenv("API_HASH", "217e861ebca9da0dd4c17b1abf92636c")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8527439347:AAFE-qK2yTYU-90D30eTLF-wyiaHfYyTOZ4")
    ADMIN = [int(admin) for admin in os.getenv("ADMIN", "1869817167").split()]
    DB_URL = os.getenv("DB_URL", "mongodb+srv://Filex:Guddu8972771037@cluster0.er3kfsr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DB_NAME = os.getenv("DB_NAME", "Filex")
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002795055491"))
    START_PIC = os.getenv("START_PIC", "https://graph.org/file/29a3acbbab9de5f45a5fe.jpg")
    WEBHOOK = os.getenv("WEBHOOK", "False").lower() == "true"
    PORT = int(os.getenv("PORT", "8080"))
    BOT_UPTIME = time.time()
    
    # Media conversion settings
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
    SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    SUPPORTED_AUDIO_FORMATS = ['.mp3', '.m4a', '.wav', '.flac', '.ogg']
    SUPPORTED_DOCUMENT_FORMATS = ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']

class Txt:
    START_TXT = """<b>ʜᴇʏ! {}  

» ɪ ᴀᴍ ᴀᴅᴠᴀɴᴄᴇᴅ ʀᴇɴᴀᴍᴇ ʙᴏᴛ! ᴡʜɪᴄʜ ᴄᴀɴ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ғɪʟᴇs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴀɴᴅ ᴀʟsᴏ sᴇǫᴜᴇɴᴄᴇ ᴛʜᴇᴍ ᴘᴇʀғᴇᴄᴛʟʏ</b>"""
    
    FILE_NAME_TXT = """<b>» <u>sᴇᴛᴜᴘ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ</u></b>

<b>ᴠᴀʀɪᴀʙʟᴇs :</b>
➲ ᴇᴘɪsᴏᴅᴇ - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ᴇᴘɪsᴏᴅᴇ ɴᴜᴍʙᴇʀ  
➲ sᴇᴀsᴏɴ - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ sᴇᴀsᴏɴ ɴᴜᴍʙᴇʀ  
➲ ǫᴜᴀʟɪᴛʏ - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ǫᴜᴀʟɪᴛʏ  

<b>‣ ꜰᴏʀ ᴇx:- </b> `/autorename Oᴠᴇʀғʟᴏᴡ [Sseason Eepisode] - [Dual] quality`

<b>‣ /Autorename: ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ꜰɪʟᴇs ʙʏ ɪɴᴄʟᴜᴅɪɴɢ 'ᴇᴘɪsᴏᴅᴇ' ᴀɴᴅ 'ǫᴜᴀʟɪᴛʏ' ᴠᴀʀɪᴀʙʟᴇs ɪɴ ʏᴏᴜʀ ᴛᴇxᴛ, ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴇᴘɪsᴏᴅᴇ ᴀɴᴅ ǫᴜᴀʟɪᴛʏ ᴘʀᴇsᴇɴᴛ ɪɴ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ꜰɪʟᴇɴᴀᴍᴇ.</b>"""
    
    CAPTION_TXT = """<b><u>» ᴛᴏ ꜱᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ</u></b>
    
<b>ᴠᴀʀɪᴀʙʟᴇs :</b>         
sɪᴢᴇ: {filesize}
ᴅᴜʀᴀᴛɪᴏɴ: {duration}
ꜰɪʟᴇɴᴀᴍᴇ: {filename}

➲ /set_caption: ᴛᴏ ꜱᴇᴛ ᴀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.
➲ /see_caption: ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.
➲ /del_caption: ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.

» ꜰᴏʀ ᴇx:- /set_caption ꜰɪʟᴇ ɴᴀᴍᴇ: {filename}"""

    THUMBNAIL_TXT = """<b><u>» ᴛᴏ ꜱᴇᴛ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ</u></b>
    
➲ /start: ꜱᴇɴᴅ ᴀɴʏ ᴘʜᴏᴛᴏ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ꜱᴇᴛ ɪᴛ ᴀs ᴀ ᴛʜᴜᴍʙɴᴀɪʟ..
➲ /del_thumb: ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴏʟᴅ ᴛʜᴜᴍʙɴᴀɪʟ.
➲ /view_thumb: ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ.

ɴᴏᴛᴇ: ɪꜰ ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴀᴠᴇᴅ ɪɴ ʙᴏᴛ ᴛʜᴇɴ, ɪᴛ ᴡɪʟʟ ᴜsᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴏꜰ ᴛʜᴇ ᴏʀɪɢɪɴɪᴀʟ ꜰɪʟᴇ ᴛᴏ ꜱᴇᴛ ɪɴ ʀᴇɴᴀᴍᴇᴅ ꜰɪʟᴇ"""

    MEDIA_FORMAT_TXT = """<b><u>» ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ ꜰɪʀꜱᴛ</u></b>

<b>ɪᴍᴘᴏʀᴛᴀɴᴛ:</b> ʏᴏᴜ ᴍᴜꜱᴛ ꜱᴇᴛ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ ʙᴇꜰᴏʀᴇ ꜱᴇɴᴅɪɴɢ ꜰɪʟᴇꜱ!

<b>📁 File Format:</b>
• ꜰɪʟᴇs ᴡɪʟʟ ʙᴇ sᴇɴᴛ ᴀs ᴅᴏᴄᴜᴍᴇɴᴛs
• ᴘʀᴇsᴇʀᴠᴇs ᴏʀɪɢɪɴᴀʟ ꜰɪʟᴇ ᴛʏᴘᴇ
• ꜰᴀsᴛᴇʀ ᴘʀᴏᴄᴇssɪɴɢ

<b>🎬 Video Format:</b>
• ᴀʟʟ ꜰɪʟᴇs ᴡɪʟʟ ʙᴇ ᴄᴏɴᴠᴇʀᴛᴇᴅ ᴛᴏ ᴍᴘ4 ᴠɪᴅᴇᴏ
• ᴠɪᴅᴇᴏ ꜰʀᴀᴍᴇ ᴍᴀᴛᴄʜᴇs ᴛʜᴜᴍʙɴᴀɪʟ ꜱɪᴢᴇ & ʀᴀᴛɪᴏ
• ᴘᴇʀꜰᴇᴄᴛ ꜰᴏʀ ᴠɪᴅᴇᴏ ᴘʟᴀᴛꜰᴏʀᴍs

<b>ʜᴏᴡ ᴛᴏ ᴜsᴇ:</b>
1. /setmedia - ꜱᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ
2. /autorename - ꜱᴇᴛ ʀᴇɴᴀᴍᴇ ꜰᴏʀᴍᴀᴛ
3. ꜱᴇɴᴅ ᴘʜᴏᴛᴏ - ꜱᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ (ᴏᴘᴛɪᴏɴᴀʟ)
4. ꜱᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ - ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴘʀᴏᴄᴇssɪɴɢ"""

    PROGRESS_BAR = """\n
<b>» Size</b> : {1} | {2}
<b>» Done</b> : {0}%
<b>» Speed</b> : {3}/s
<b>» ETA</b> : {4} """

    HELP_TXT = """<b>ʜᴇʀᴇ ɪs ʜᴇʟᴘ ᴍᴇɴᴜ ɪᴍᴘᴏʀᴛᴀɴᴔ ᴄᴏᴍᴍᴀɴᴅs:

ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs🫧

ʀᴇɴᴀᴍᴇ ʙᴏᴛ ɪs ᴀ ʜᴀɴᴅʏ ᴛᴏᴏʟ ᴛʜᴀᴛ ʜᴇʟᴘs ʏᴏᴜ ʀᴇɴᴀᴍᴇ ᴀɴᴅ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ꜰɪʟᴇs ᴇꜰꜰᴏʀᴛʟᴇssʟʏ.

<b>ꜱᴇᴛᴜᴘ ꜱᴛᴇᴘs:</b>
1. /setmedia - ꜱᴇᴛ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ ꜰɪʀꜱᴛ
2. /autorename - ꜱᴇᴛ ʀᴇɴᴀᴍᴇ ꜰᴏʀᴍᴀᴛ
3. ꜱᴇɴᴅ ᴘʜᴏᴛᴏ - ꜱᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ
4. ꜱᴇɴᴅ ꜰɪʟᴇs - ᴀᴜᴛᴏ ᴘʀᴏᴄᴇssɪɴɢ

<b>ᴏᴛʜᴇʀ ᴄᴏᴍᴍᴀɴᴅs:</b>
➲ /set_caption: ꜱᴇᴛ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ
➲ /metadata: ᴛᴜʀɴ ᴏɴ/ᴏꜰꜰ ᴍᴇᴛᴀᴅᴀᴛᴀ
➲ /help: ɢᴇᴛ ᴍᴏʀᴇ ʜᴇʟᴘ</b>"""
    
    META_TXT = """<b><u>» How to Set Metadata</u></b>

<b>Available metadata commands:</b>
➲ /settitle - Set the title metadata
➲ /setauthor - Set the author metadata
➲ /setartist - Set the artist metadata  
➲ /setaudio - Set the audio track title
➲ /setsubtitle - Set the subtitle track title
➲ /setvideo - Set the video track title

<b>Example:</b>
<code>/settitle Encoded by @Codeflix_Bots</code>
<code>/setauthor @Codeflix_Bots</code>

<b>Note:</b> Some metadata fields may not be supported by all video formats."""

# ==================== DATABASE ====================
class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.DB_URL)
        self.db = self.client[Config.DB_NAME]
        self.col = self.db.users
    
    def new_user(self, user_id):
        return {
            "_id": int(user_id),
            "join_date": datetime.now().isoformat(),
            "file_id": None,
            "caption": None,
            "metadata": True,
            "title": "Encoded by @Codeflix_Bots",
            "author": "@Codeflix_Bots",
            "artist": "@Codeflix_Bots",
            "audio": "By @Codeflix_Bots",
            "subtitle": "By @Codeflix_Bots",
            "video": "Encoded By @Codeflix_Bots",
            "format_template": None,
            "media_format": None,  # User must set this first: "file" or "video"
            "media_format_set": False,  # Track if user has set media format
            "ban_status": {
                "is_banned": False,
                "ban_duration": 0,
                "banned_on": datetime.max.isoformat(),
                "ban_reason": ''
            }
        }
    
    async def add_user(self, user_id):
        if not await self.is_user_exist(user_id):
            user = self.new_user(user_id)
            await self.col.insert_one(user)
    
    async def is_user_exist(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return bool(user)
    
    async def total_users_count(self):
        return await self.col.count_documents({})
    
    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({"_id": int(user_id)})
    
    async def set_thumbnail(self, user_id, file_id):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"file_id": file_id}})
    
    async def get_thumbnail(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("file_id", None) if user else None
    
    async def set_caption(self, user_id, caption):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"caption": caption}})
    
    async def get_caption(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("caption", None) if user else None
    
    async def set_format_template(self, user_id, format_template):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"format_template": format_template}})
    
    async def get_format_template(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("format_template", None) if user else None
    
    async def set_media_format(self, user_id, media_format):
        await self.col.update_one({"_id": int(user_id)}, {
            "$set": {
                "media_format": media_format,
                "media_format_set": True
            }
        })
    
    async def get_media_format(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("media_format", None) if user else None
    
    async def is_media_format_set(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("media_format_set", False) if user else False
    
    async def get_metadata(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("metadata", True) if user else True
    
    async def set_metadata(self, user_id, metadata):
        if isinstance(metadata, str):
            metadata = metadata.lower() == "on"
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"metadata": metadata}})
    
    async def get_title(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("title", "Encoded by @Codeflix_Bots") if user else "Encoded by @Codeflix_Bots"
    
    async def set_title(self, user_id, title):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"title": title}})
    
    async def get_author(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("author", "@Codeflix_Bots") if user else "@Codeflix_Bots"
    
    async def set_author(self, user_id, author):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"author": author}})
    
    async def get_artist(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("artist", "@Codeflix_Bots") if user else "@Codeflix_Bots"
    
    async def set_artist(self, user_id, artist):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"artist": artist}})
    
    async def get_audio(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("audio", "By @Codeflix_Bots") if user else "By @Codeflix_Bots"
    
    async def set_audio(self, user_id, audio):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"audio": audio}})
    
    async def get_subtitle(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("subtitle", "By @Codeflix_Bots") if user else "By @Codeflix_Bots"
    
    async def set_subtitle(self, user_id, subtitle):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"subtitle": subtitle}})
    
    async def get_video(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("video", "Encoded By @Codeflix_Bots") if user else "Encoded By @Codeflix_Bots"
    
    async def set_video(self, user_id, video):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"video": video}})

# Initialize database
db = Database()

# ==================== UTILITY FUNCTIONS ====================
def humanbytes(size):
    """Convert bytes to human readable format"""
    if not size:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
          ((str(hours) + "ʜ, ") if hours else "") + \
          ((str(minutes) + "ᴍ, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2] or "0 s"

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}".format(
            ''.join(["█" for _ in range(math.floor(percentage / 5))]),
            ''.join(["░" for _ in range(20 - math.floor(percentage / 5))])
        )
        
        tmp = progress + Txt.PROGRESS_BAR.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time else "0 s"
        )
        
        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• ᴄᴀɴᴄᴇʟ •", callback_data="close")]
                ])
            )
        except:
            pass

# ==================== NSFW CHECK ====================
nsfw_keywords = [
    "porn", "sex", "nude", "naked", "boobs", "tits", "pussy", "dick", "cock", "ass",
    "fuck", "blowjob", "cum", "orgasm", "shemale", "erotic", "masturbate", "anal",
    "hardcore", "bdsm", "fetish", "lingerie", "xxx", "milf", "gay", "lesbian",
    "threesome", "hentai", "doujin", "ecchi", "yaoi", "shota", "loli", "tentacle"
]

async def check_anti_nsfw(filename, message):
    lower_name = filename.lower()
    for keyword in nsfw_keywords:
        if keyword in lower_name:
            await message.reply_text("❌ NSFW content detected. File not processed.")
            return True
    return False

# ==================== MEDIA CONVERSION FUNCTIONS ====================
def get_media_info(file_path):
    """Get media information using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    except:
        return None

def get_video_resolution(file_path):
    """Get video resolution"""
    info = get_media_info(file_path)
    if info and 'streams' in info:
        for stream in info['streams']:
            if stream.get('codec_type') == 'video':
                width = stream.get('width', 0)
                height = stream.get('height', 0)
                return width, height
    return 0, 0

def get_thumbnail_dimensions(thumb_path):
    """Get thumbnail dimensions"""
    if not thumb_path or not os.path.exists(thumb_path):
        return 1280, 720  # Default HD dimensions
    
    try:
        with Image.open(thumb_path) as img:
            width, height = img.size
            # Ensure even dimensions for video encoding
            width = width - (width % 2)
            height = height - (height % 2)
            return width, height
    except:
        return 1280, 720

def get_aspect_ratio(width, height):
    """Calculate aspect ratio"""
    if width == 0 or height == 0:
        return "16:9"
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    g = gcd(width, height)
    return f"{width//g}:{height//g}"

def convert_to_video_format(input_path, output_path, thumb_path=None):
    """Convert any file to MP4 video format with thumbnail dimensions"""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Get thumbnail dimensions
    if thumb_path and os.path.exists(thumb_path):
        thumb_width, thumb_height = get_thumbnail_dimensions(thumb_path)
        # Ensure minimum dimensions
        if thumb_width < 640:
            thumb_width = 640
        if thumb_height < 360:
            thumb_height = 360
    else:
        thumb_width, thumb_height = 1280, 720
    
    # Get file extension
    input_ext = os.path.splitext(input_path)[1].lower()
    
    # Build FFmpeg command based on input type
    cmd = ['ffmpeg']
    
    # Check if input is video
    if input_ext in Config.SUPPORTED_VIDEO_FORMATS:
        # Video to video conversion - resize to thumbnail dimensions
        cmd.extend([
            '-i', input_path,
            '-vf', f'scale={thumb_width}:{thumb_height}:force_original_aspect_ratio=decrease,pad={thumb_width}:{thumb_height}:(ow-iw)/2:(oh-ih)/2,setsar=1',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-pix_fmt', 'yuv420p',
            '-y', output_path
        ])
    
    # Check if input is image
    elif input_ext in Config.SUPPORTED_IMAGE_FORMATS:
        # Image to video conversion
        cmd.extend([
            '-loop', '1',
            '-i', input_path,
            '-vf', f'scale={thumb_width}:{thumb_height},setsar=1',
            '-c:v', 'libx264',
            '-t', '10',  # 10 second video
            '-pix_fmt', 'yuv420p',
            '-y', output_path
        ])
    
    # Check if input is audio
    elif input_ext in Config.SUPPORTED_AUDIO_FORMATS:
        # Audio to video conversion
        if thumb_path and os.path.exists(thumb_path):
            cmd.extend([
                '-loop', '1',
                '-i', thumb_path,
                '-i', input_path,
                '-vf', f'scale={thumb_width}:{thumb_height},setsar=1',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-pix_fmt', 'yuv420p',
                '-y', output_path
            ])
        else:
            cmd.extend([
                '-f', 'lavfi',
                '-i', f'color=c=black:s={thumb_width}x{thumb_height}:r=25',
                '-i', input_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                '-pix_fmt', 'yuv420p',
                '-y', output_path
            ])
    
    # For other files (documents, etc.)
    else:
        if thumb_path and os.path.exists(thumb_path):
            cmd.extend([
                '-loop', '1',
                '-i', thumb_path,
                '-vf', f'scale={thumb_width}:{thumb_height},setsar=1',
                '-c:v', 'libx264',
                '-t', '5',  # 5 second video
                '-pix_fmt', 'yuv420p',
                '-y', output_path
            ])
        else:
            cmd.extend([
                '-f', 'lavfi',
                '-i', f'color=c=white:s={thumb_width}x{thumb_height}:r=25',
                '-c:v', 'libx264',
                '-t', '5',
                '-pix_fmt', 'yuv420p',
                '-y', output_path
            ])
    
    # Run conversion
    try:
        process = subprocess.run(cmd, capture_output=True, text=True)
        if process.returncode != 0:
            error_msg = process.stderr if process.stderr else "Unknown error"
            raise RuntimeError(f"FFmpeg error: {error_msg}")
        
        # Verify output file was created
        if not os.path.exists(output_path):
            raise RuntimeError("Output file was not created")
        
        return output_path
    except Exception as e:
        print(f"Conversion error: {e}")
        print(f"FFmpeg command: {' '.join(cmd)}")
        raise

async def convert_to_video_async(input_path, output_path, thumb_path):
    """Async wrapper for video conversion"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, convert_to_video_format, input_path, output_path, thumb_path
    )

async def add_metadata(input_path, output_path, user_id):
    """Add metadata to media file using ffmpeg"""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Get metadata values from database
    title = await db.get_title(user_id)
    artist = await db.get_artist(user_id)
    author = await db.get_author(user_id)
    video_title = await db.get_video(user_id)
    audio_title = await db.get_audio(user_id)
    subtitle_title = await db.get_subtitle(user_id)
    
    # Determine file extension
    file_ext = os.path.splitext(output_path)[1].lower()
    
    # Prepare metadata arguments
    metadata_args = []
    
    # Add standard metadata fields
    if title:
        metadata_args.extend(['-metadata', f'title={title}'])
    if artist:
        metadata_args.extend(['-metadata', f'artist={artist}'])
    if author:
        metadata_args.extend(['-metadata', f'author={author}'])
    
    # Add stream-specific metadata
    if video_title:
        metadata_args.extend(['-metadata:s:v', f'title={video_title}'])
    if audio_title:
        metadata_args.extend(['-metadata:s:a', f'title={audio_title}'])
    if subtitle_title:
        metadata_args.extend(['-metadata:s:s', f'title={subtitle_title}'])
    
    # Build FFmpeg command
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-map_metadata', '0',
        '-c', 'copy',
    ]
    
    # Add format-specific flags
    if file_ext in ['.mp4', '.m4v', '.mov']:
        cmd.extend(['-movflags', 'use_metadata_tags'])
    elif file_ext in ['.mkv', '.webm']:
        cmd.extend(['-map_metadata', '0', '-c', 'copy'])
    
    # Add metadata arguments
    cmd.extend(metadata_args)
    
    # Add output file
    cmd.extend(['-y', output_path])
    
    # Execute FFmpeg command
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            print(f"Metadata warning: {error_msg}")
            # Copy file without metadata as fallback
            shutil.copy2(input_path, output_path)
            return output_path
        
        return output_path
        
    except Exception as e:
        print(f"Metadata processing error: {e}")
        # Fallback: copy file without metadata
        shutil.copy2(input_path, output_path)
        return output_path

# ==================== FILE PROCESSING FUNCTIONS ====================
def extract_season_episode(filename):
    """Extract season and episode numbers from filename"""
    patterns = [
        (r'S(\d+)(?:E|EP)(\d+)', ('season', 'episode')),
        (r'S(\d+)[\s-]*(?:E|EP)(\d+)', ('season', 'episode')),
        (r'Season\s*(\d+)\s*Episode\s*(\d+)', ('season', 'episode')),
        (r'\[S(\d+)\]\[E(\d+)\]', ('season', 'episode')),
        (r'S(\d+)[^\d]*(\d+)', ('season', 'episode')),
        (r'(?:E|EP|Episode)\s*(\d+)', (None, 'episode')),
        (r'\b(\d+)\b', (None, 'episode'))
    ]
    
    for pattern, (season_group, episode_group) in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            season = match.group(1) if season_group else None
            episode = match.group(2) if episode_group else match.group(1)
            return season, episode
    return None, None

def extract_quality(filename):
    """Extract quality information from filename"""
    quality_patterns = [
        (r'\b(\d{3,4}[pi])\b', lambda m: m.group(1)),  # 1080p, 720p
        (r'\b(4k|2160p)\b', lambda m: "4K"),
        (r'\b(2k|1440p)\b', lambda m: "2K"),
        (r'\b(HDRip|HDTV|WEB-DL|WEBRip|BluRay)\b', lambda m: m.group(1)),
        (r'\[(\d{3,4}[pi])\]', lambda m: m.group(1))
    ]
    
    for pattern, extractor in quality_patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            return extractor(match)
    return "Unknown"

async def cleanup_files(*paths):
    """Safely remove files if they exist"""
    for path in paths:
        try:
            if path and os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
        except Exception as e:
            print(f"Error removing {path}: {e}")

async def process_thumbnail(thumb_path):
    """Process and resize thumbnail image"""
    if not thumb_path or not os.path.exists(thumb_path):
        return None
    
    try:
        with Image.open(thumb_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize to reasonable size for Telegram
            img.thumbnail((320, 320), Image.Resampling.LANCZOS)
            img.save(thumb_path, "JPEG", quality=90)
        return thumb_path
    except Exception as e:
        print(f"Thumbnail processing error: {e}")
        await cleanup_files(thumb_path)
        return None

def generate_new_filename(format_template, original_name, file_size, duration):
    """Generate new filename based on template"""
    base_name = os.path.splitext(original_name)[0]
    ext = os.path.splitext(original_name)[1] or '.mp4'
    
    season, episode = extract_season_episode(base_name)
    quality = extract_quality(base_name)
    
    # Replace variables in template
    new_filename = format_template
    replacements = {
        '{filename}': base_name,
        '{season}': season or '01',
        '{episode}': episode or '01',
        '{quality}': quality,
        '{filesize}': humanbytes(file_size),
        '{duration}': str(timedelta(seconds=duration)) if duration else '00:00:00',
        'Season': season or '01',
        'Episode': episode or '01',
        'QUALITY': quality.upper() if quality != "Unknown" else "HD"
    }
    
    for key, value in replacements.items():
        new_filename = new_filename.replace(key, value)
    
    return new_filename, ext

# ==================== BOT CLIENT ====================
# Create necessary directories
os.makedirs("downloads", exist_ok=True)
os.makedirs("temp", exist_ok=True)
os.makedirs("converted", exist_ok=True)

# Initialize bot
app = Client(
    "auto_rename_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=200,
    sleep_threshold=15,
)

# ==================== HANDLERS ====================
# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user
    await db.add_user(user.id)
    
    # Check if media format is set
    media_format_set = await db.is_media_format_set(user.id)
    
    # Send welcome message with appropriate buttons
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
        [
            InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇs', url='https://t.me/Codeflix_Bots'),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/CodeflixSupport')
        ]
    ])
    
    if not media_format_set:
        # Add media format button if not set
        buttons.inline_keyboard.insert(0, [
            InlineKeyboardButton("⚙️ ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ", callback_data='set_media_first')
        ])
    
    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Txt.START_TXT.format(user.mention),
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            Txt.START_TXT.format(user.mention),
            reply_markup=buttons
        )

# Set media format command - MUST BE SET FIRST
@app.on_message(filters.command("setmedia") & filters.private)
async def setmedia_handler(client, message):
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📁 File Format", callback_data="media_file"),
            InlineKeyboardButton("🎬 Video Format", callback_data="media_video")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="help")]
    ])
    
    current_format = await db.get_media_format(message.from_user.id)
    format_status = f"`{current_format.capitalize()}`" if current_format else "❌ **Not Set!**"
    
    await message.reply_text(
        f"**⚙️ ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ ꜰɪʀꜱᴛ**\n\n"
        f"**Current Format:** {format_status}\n\n"
        "**📁 File Format:** Files will be sent as documents\n"
        "**🎬 Video Format:** All files converted to MP4 video\n\n"
        "⚠️ **You must set media format before sending files!**",
        reply_markup=buttons
    )

# Help command
@app.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    user_id = message.from_user.id
    media_format_set = await db.is_media_format_set(user_id)
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
        [
            InlineKeyboardButton('• ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
            InlineKeyboardButton('ᴄᴀᴘᴛɪᴏɴ •', callback_data='caption')
        ],
        [
            InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'),
            InlineKeyboardButton('ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ •', callback_data='media_format')
        ],
        [InlineKeyboardButton('• ʜᴏᴍᴇ', callback_data='home')]
    ])
    
    # Add warning if media format not set
    if not media_format_set:
        buttons.inline_keyboard.insert(0, [
            InlineKeyboardButton("⚠️ ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ ꜰɪʀꜱᴛ", callback_data='set_media_first')
        ])
    
    await message.reply_text(
        Txt.HELP_TXT,
        reply_markup=buttons,
        disable_web_page_preview=True
    )

# Autorename command
@app.on_message(filters.command("autorename") & filters.private)
async def autorename_handler(client, message):
    user_id = message.from_user.id
    
    # Check if media format is set
    if not await db.is_media_format_set(user_id):
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ", callback_data='set_media_first')],
            [InlineKeyboardButton("🔙 Back", callback_data='help')]
        ])
        
        await message.reply_text(
            "❌ **Please set media format first!**\n\n"
            "You must set your media format before using the rename feature.\n"
            "Use /setmedia or click the button below.",
            reply_markup=buttons
        )
        return
    
    if len(message.command) < 2:
        await message.reply_text(
            "**Please provide a rename format!**\n\n"
            "**Example:** `/autorename {filename} [S{season}E{episode}] - {quality}`\n\n"
            "**Available variables:**\n"
            "- `{filename}`: Original filename\n"
            "- `{season}`: Season number\n"
            "- `{episode}`: Episode number\n"
            "- `{quality}`: Video quality\n"
            "- `{filesize}`: File size\n"
            "- `{duration}`: Duration (for videos)"
        )
        return
    
    format_template = message.text.split(" ", 1)[1]
    await db.set_format_template(user_id, format_template)
    
    await message.reply_text(
        f"**✅ Rename format set successfully!**\n\n"
        f"**Your format:** `{format_template}`\n\n"
        "Now you can send me any file to rename it automatically."
    )

# Set caption command
@app.on_message(filters.command("set_caption") & filters.private)
async def set_caption_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "**Please provide a caption!**\n\n"
            "**Example:** `/set_caption File: {filename}\nSize: {filesize}\nDuration: {duration}`\n\n"
            "**Available variables:**\n"
            "- `{filename}`: File name\n"
            "- `{filesize}`: File size\n"
            "- `{duration}`: Duration"
        )
        return
    
    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.from_user.id, caption)
    await message.reply_text("✅ Caption set successfully!")

# View caption command
@app.on_message(filters.command(["see_caption", "view_caption"]) & filters.private)
async def see_caption_handler(client, message):
    caption = await db.get_caption(message.from_user.id)
    if caption:
        await message.reply_text(f"**Your caption:**\n\n`{caption}`")
    else:
        await message.reply_text("❌ No caption set. Use /set_caption to set one.")

# Delete caption command
@app.on_message(filters.command("del_caption") & filters.private)
async def del_caption_handler(client, message):
    await db.set_caption(message.from_user.id, None)
    await message.reply_text("✅ Caption deleted successfully!")

# View thumbnail command
@app.on_message(filters.command(["view_thumb", "viewthumb"]) & filters.private)
async def view_thumb_handler(client, message):
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(message.chat.id, thumb)
    else:
        await message.reply_text("❌ No thumbnail set. Send a photo to set as thumbnail.")

# Delete thumbnail command
@app.on_message(filters.command(["del_thumb", "delthumb"]) & filters.private)
async def del_thumb_handler(client, message):
    await db.set_thumbnail(message.from_user.id, None)
    await message.reply_text("✅ Thumbnail deleted successfully!")

# Set thumbnail from photo
@app.on_message(filters.private & filters.photo)
async def set_thumb_handler(client, message):
    await db.set_thumbnail(message.from_user.id, message.photo.file_id)
    await message.reply_text("✅ Thumbnail saved successfully!")

# Metadata command
@app.on_message(filters.command("metadata") & filters.private)
async def metadata_handler(client, message):
    metadata_status = await db.get_metadata(message.from_user.id)
    status_text = "ON ✅" if metadata_status else "OFF ❌"
    
    # Get current metadata values for display
    title = await db.get_title(message.from_user.id)
    author = await db.get_author(message.from_user.id)
    artist = await db.get_artist(message.from_user.id)
    video = await db.get_video(message.from_user.id)
    audio = await db.get_audio(message.from_user.id)
    subtitle = await db.get_subtitle(message.from_user.id)
    
    text = f"""
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪs ᴄᴜʀʀᴇɴᴛʟʏ: {status_text}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪsᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴅᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
    """
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Turn ON", callback_data="metadata_on"),
            InlineKeyboardButton("Turn OFF", callback_data="metadata_off")
        ],
        [
            InlineKeyboardButton("How to Set Metadata", callback_data="metainfo")
        ],
        [
            InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help")
        ]
    ])
    
    await message.reply_text(
        text=text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )

# Set metadata fields commands
@app.on_message(filters.private & filters.command('settitle'))
async def settitle_handler(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /settitle Encoded By @Codeflix_Bots**")
    title = message.text.split(" ", 1)[1]
    await db.set_title(message.from_user.id, title=title)
    await message.reply_text("**✅ Tɪᴛʟᴇ Sᴀᴠᴇᴅ**")

@app.on_message(filters.private & filters.command('setauthor'))
async def setauthor_handler(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Aᴜᴛʜᴏʀ\n\nExᴀᴍᴩʟᴇ:- /setauthor @Codeflix_Bots**")
    author = message.text.split(" ", 1)[1]
    await db.set_author(message.from_user.id, author=author)
    await message.reply_text("**✅ Aᴜᴛʜᴏʀ Sᴀᴠᴇᴅ**")

@app.on_message(filters.private & filters.command('setartist'))
async def setartist_handler(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Aʀᴛɪsᴛ\n\nExᴀᴍᴩʟᴇ:- /setartist @Codeflix_Bots**")
    artist = message.text.split(" ", 1)[1]
    await db.set_artist(message.from_user.id, artist=artist)
    await message.reply_text("**✅ Aʀᴛɪsᴛ Sᴀᴠᴇᴅ**")

@app.on_message(filters.private & filters.command('setaudio'))
async def setaudio_handler(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Aᴜᴅɪᴏ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setaudio @Codeflix_Bots**")
    audio = message.text.split(" ", 1)[1]
    await db.set_audio(message.from_user.id, audio=audio)
    await message.reply_text("**✅ Aᴜᴅɪᴏ Sᴀᴠᴇᴅ**")

@app.on_message(filters.private & filters.command('setsubtitle'))
async def setsubtitle_handler(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Sᴜʙᴛɪᴛʟᴇ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setsubtitle @Codeflix_Bots**")
    subtitle = message.text.split(" ", 1)[1]
    await db.set_subtitle(message.from_user.id, subtitle=subtitle)
    await message.reply_text("**✅ Sᴜʙᴛɪᴛʟᴇ Sᴀᴠᴇᴅ**")

@app.on_message(filters.private & filters.command('setvideo'))
async def setvideo_handler(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Gɪᴠᴇ Tʜᴇ Vɪᴅᴇᴏ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setvideo Encoded by @Codeflix_Bots**")
    video = message.text.split(" ", 1)[1]
    await db.set_video(message.from_user.id, video=video)
    await message.reply_text("**✅ Vɪᴅᴇᴏ Sᴀᴠᴇᴅ**")

# Main file handler - Auto processes based on user's media format setting
@app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))
async def auto_file_handler(client, message):
    user_id = message.from_user.id
    
    # Check if media format is set
    if not await db.is_media_format_set(user_id):
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ", callback_data='set_media_first')],
            [InlineKeyboardButton("🔙 Back", callback_data='help')]
        ])
        
        await message.reply_text(
            "❌ **Please set media format first!**\n\n"
            "You must set your media format before sending files.\n"
            "Use /setmedia or click the button below.\n\n"
            "**Why?** This determines how your files will be processed:\n"
            "• 📁 File Format: As documents\n"
            "• 🎬 Video Format: As videos",
            reply_markup=buttons
        )
        return
    
    # Check if rename format is set
    format_template = await db.get_format_template(user_id)
    if not format_template:
        await message.reply_text(
            "❌ **Please set a rename format first!**\n\n"
            "Use: `/autorename Your Format Here`\n\n"
            "**Example:** `/autorename {filename} [S{season}E{episode}]`"
        )
        return
    
    # Get file info
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name or "file"
        file_size = message.document.file_size
        media_type = "document"
        duration = 0
    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name or "video.mp4"
        file_size = message.video.file_size
        media_type = "video"
        duration = message.video.duration
    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name or "audio.mp3"
        file_size = message.audio.file_size
        media_type = "audio"
        duration = message.audio.duration
    elif message.photo:
        file_id = message.photo.file_id
        file_name = f"photo_{message.photo.file_unique_id}.jpg"
        file_size = 0
        media_type = "photo"
        duration = 0
    else:
        return
    
    # Check NSFW
    if await check_anti_nsfw(file_name, message):
        return
    
    # Get user's media format
    media_format = await db.get_media_format(user_id)
    
    # Show processing message
    format_icon = "🎬" if media_format == "video" else "📁"
    msg = await message.reply_text(f"{format_icon} **Processing as {media_format.capitalize()}...**")
    
    # Generate unique filename
    timestamp = int(time.time())
    original_ext = os.path.splitext(file_name)[1] or ('.mp4' if media_type == 'video' else '.jpg')
    download_path = f"downloads/{user_id}_{timestamp}{original_ext}"
    
    try:
        # Download with progress
        start_time = time.time()
        file_path = await message.download(
            file_name=download_path,
            progress=progress_for_pyrogram,
            progress_args=("📥 Downloading...", msg, start_time)
        )
        
        if not os.path.exists(file_path):
            await msg.edit_text("❌ Download failed!")
            return
        
        # Get actual file size
        file_size = os.path.getsize(file_path)
        
        # Get thumbnail
        thumb_path = None
        user_thumb = await db.get_thumbnail(user_id)
        
        if user_thumb:
            thumb_path = f"temp/{user_id}_thumb_{timestamp}.jpg"
            await client.download_media(user_thumb, file_name=thumb_path)
            thumb_path = await process_thumbnail(thumb_path)
        elif media_type == "video" and message.video.thumbs:
            thumb = message.video.thumbs[0]
            thumb_path = f"temp/{user_id}_video_thumb_{timestamp}.jpg"
            await client.download_media(thumb.file_id, file_name=thumb_path)
            thumb_path = await process_thumbnail(thumb_path)
        
        # Generate new filename
        new_filename, original_ext = generate_new_filename(
            format_template, file_name, file_size, duration
        )
        
        # Process based on media format
        if media_format == "video":
            # Video format - convert to MP4
            new_filename = os.path.splitext(new_filename)[0] + ".mp4"
            output_path = f"converted/{user_id}_{timestamp}.mp4"
            
            await msg.edit_text("🎬 **Converting to video format...**")
            try:
                output_path = await convert_to_video_async(file_path, output_path, thumb_path)
            except Exception as e:
                await msg.edit_text(f"❌ Video conversion failed: {str(e)[:100]}")
                # Fallback to file format
                output_path = file_path
                media_format = "file"
                new_filename = new_filename.replace('.mp4', original_ext)
        else:
            # File format - keep original
            new_filename = new_filename + original_ext
            output_path = file_path
        
        # Process metadata if enabled
        metadata_enabled = await db.get_metadata(user_id)
        final_output_path = output_path
        
        if metadata_enabled and os.path.exists(output_path):
            try:
                metadata_path = f"temp/{user_id}_metadata_{int(time.time())}{os.path.splitext(output_path)[1]}"
                final_output_path = await add_metadata(output_path, metadata_path, user_id)
                if output_path != file_path and output_path != final_output_path:
                    await cleanup_files(output_path)
            except Exception as e:
                print(f"Metadata error: {e}")
                # Continue without metadata
        
        # Get caption
        caption_template = await db.get_caption(user_id) or "{filename}"
        caption = caption_template.replace("{filename}", new_filename)\
                                 .replace("{filesize}", humanbytes(file_size))\
                                 .replace("{duration}", str(timedelta(seconds=duration)) if duration else '00:00:00')
        
        # Upload file
        await msg.edit_text("📤 **Uploading file...**")
        upload_start = time.time()
        
        if media_format == "video":
            # Get video duration
            video_duration = 0
            if os.path.exists(final_output_path):
                try:
                    info = get_media_info(final_output_path)
                    if info and 'format' in info:
                        video_duration = float(info['format'].get('duration', 0))
                except:
                    video_duration = duration
            
            # Send as video
            await client.send_video(
                chat_id=message.chat.id,
                video=final_output_path,
                caption=caption,
                thumb=thumb_path,
                duration=int(video_duration),
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", msg, upload_start)
            )
        else:
            # Send as document
            await client.send_document(
                chat_id=message.chat.id,
                document=final_output_path,
                caption=caption,
                thumb=thumb_path,
                file_name=new_filename,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", msg, upload_start)
            )
        
        # Success message
        await msg.delete()
        await message.reply_text(
            f"✅ **File processed successfully as {media_format.capitalize()}!**\n"
            f"**New name:** `{new_filename}`\n"
            f"**Format:** {'🎬 Video' if media_format == 'video' else '📁 File'}"
        )
        
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)[:200]}")
        print(f"Error: {e}")
    finally:
        # Cleanup
        await cleanup_files(
            download_path, 
            output_path if 'output_path' in locals() and output_path != download_path else None,
            final_output_path if 'final_output_path' in locals() and final_output_path != output_path else None,
            thumb_path if 'thumb_path' in locals() else None
        )

# Callback query handler
@app.on_callback_query()
async def callback_handler(client, query):
    data = query.data
    user_id = query.from_user.id
    
    if data == "home":
        media_format_set = await db.is_media_format_set(user_id)
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
            [
                InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇs', url='https://t.me/Codeflix_Bots'),
                InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/CodeflixSupport')
            ]
        ])
        
        if not media_format_set:
            buttons.inline_keyboard.insert(0, [
                InlineKeyboardButton("⚙️ ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ", callback_data='set_media_first')
            ])
        
        await query.message.edit_text(
            Txt.START_TXT.format(query.from_user.mention),
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    
    elif data == "set_media_first":
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📁 File Format", callback_data="media_file"),
                InlineKeyboardButton("🎬 Video Format", callback_data="media_video")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="home")]
        ])
        
        await query.message.edit_text(
            Txt.MEDIA_FORMAT_TXT,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    
    elif data == "media_file":
        await db.set_media_format(user_id, "file")
        await query.answer("✅ Media format set to File!")
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 ꜱᴇᴛ ʀᴇɴᴀᴍᴇ ꜰᴏʀᴍᴀᴛ", callback_data="file_names")],
            [InlineKeyboardButton("🖼️ ꜱᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="thumbnail")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="home")]
        ])
        
        await query.message.edit_text(
            "✅ **Media format set to File!**\n\n"
            "**Now you can:**\n"
            "1. Set rename format with /autorename\n"
            "2. Set thumbnail by sending a photo\n"
            "3. Send any file - it will be processed as a document\n\n"
            "**All your files will now be sent as documents.**",
            reply_markup=buttons
        )
    
    elif data == "media_video":
        await db.set_media_format(user_id, "video")
        await query.answer("✅ Media format set to Video!")
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 ꜱᴇᴛ ʀᴇɴᴀᴍᴇ ꜰᴏʀᴍᴀᴛ", callback_data="file_names")],
            [InlineKeyboardButton("🖼️ ꜱᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="thumbnail")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="home")]
        ])
        
        await query.message.edit_text(
            "✅ **Media format set to Video!**\n\n"
            "**Important:** All files will be converted to MP4 video format.\n"
            "**Video frame will match thumbnail size and ratio.**\n\n"
            "**Now you can:**\n"
            "1. Set rename format with /autorename\n"
            "2. Set thumbnail by sending a photo\n"
            "3. Send any file - it will be converted to video\n\n"
            "**All your files will now be converted to videos.**",
            reply_markup=buttons
        )
    
    elif data == "help":
        media_format_set = await db.is_media_format_set(user_id)
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
            [
                InlineKeyboardButton('• ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
                InlineKeyboardButton('ᴄᴀᴘᴛɪᴏɴ •', callback_data='caption')
            ],
            [
                InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'),
                InlineKeyboardButton('ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ •', callback_data='media_format')
            ],
            [InlineKeyboardButton('• ʜᴏᴍᴇ', callback_data='home')]
        ])
        
        if not media_format_set:
            buttons.inline_keyboard.insert(0, [
                InlineKeyboardButton("⚠️ ꜱᴇᴛ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ ꜰɪʀꜱᴛ", callback_data='set_media_first')
            ])
        
        await query.message.edit_text(
            Txt.HELP_TXT,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    
    elif data == "media_format":
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📁 File Format", callback_data="media_file"),
                InlineKeyboardButton("🎬 Video Format", callback_data="media_video")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
        
        current_format = await db.get_media_format(user_id)
        format_status = f"`{current_format.capitalize()}`" if current_format else "❌ **Not Set!**"
        
        await query.message.edit_text(
            f"**⚙️ ᴍᴇᴅɪᴀ ꜰᴏʀᴍᴀᴛ ꜱᴇᴛᴛɪɴɢꜱ**\n\n"
            f"**Current Format:** {format_status}\n\n"
            "**Select your media format:**\n"
            "• **📁 File Format:** Send files as documents\n"
            "• **🎬 Video Format:** Convert all files to video\n\n"
            "⚠️ **This setting applies to ALL your files.**",
            reply_markup=buttons
        )
    
    elif data == "file_names":
        format_template = await db.get_format_template(user_id) or "Not set"
        await query.message.edit_text(
            Txt.FILE_NAME_TXT.format(format_template=format_template),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help")]
            ]),
            disable_web_page_preview=True
        )
    
    elif data == "thumbnail":
        await query.message.edit_text(
            Txt.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help")]
            ]),
            disable_web_page_preview=True
        )
    
    elif data == "caption":
        await query.message.edit_text(
            Txt.CAPTION_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help")]
            ]),
            disable_web_page_preview=True
        )
    
    elif data == "meta":
        metadata_status = await db.get_metadata(user_id)
        status_text = "ON ✅" if metadata_status else "OFF ❌"
        
        title = await db.get_title(user_id)
        author = await db.get_author(user_id)
        artist = await db.get_artist(user_id)
        video = await db.get_video(user_id)
        audio = await db.get_audio(user_id)
        subtitle = await db.get_subtitle(user_id)
        
        text = f"""
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪs ᴄᴜʀʀᴇɴᴛʟʏ: {status_text}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪsᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
        """
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Turn ON", callback_data="metadata_on"),
                InlineKeyboardButton("Turn OFF", callback_data="metadata_off")
            ],
            [
                InlineKeyboardButton("How to Set Metadata", callback_data="metainfo")
            ],
            [
                InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help")
            ]
        ])
        
        await query.message.edit_text(
            text=text,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    
    elif data == "metadata_on":
        await db.set_metadata(user_id, True)
        await query.answer("Metadata turned ON ✅")
        await callback_handler(client, query)  # Refresh menu
    
    elif data == "metadata_off":
        await db.set_metadata(user_id, False)
        await query.answer("Metadata turned OFF ❌")
        await callback_handler(client, query)  # Refresh menu
    
    elif data == "metainfo":
        await query.message.edit_text(
            text=Txt.META_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="meta"),
                    InlineKeyboardButton("• ᴄʟᴏsᴇ", callback_data="close")
                ]
            ])
        )
    
    elif data == "close":
        await query.message.delete()
    
    elif data in ["about", "source"]:
        await query.answer("This feature will be added soon!", show_alert=True)
    
    else:
        await query.answer("Feature not implemented yet!", show_alert=True)

# Admin commands
@app.on_message(filters.command("stats") & filters.user(Config.ADMIN))
async def stats_handler(client, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))
    
    await message.reply_text(
        f"**📊 Bot Statistics**\n\n"
        f"**• Total Users:** `{total_users}`\n"
        f"**• Uptime:** `{uptime}`\n"
        f"**• Admin IDs:** `{', '.join(map(str, Config.ADMIN))}`"
    )

@app.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(client, message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to a message to broadcast!")
        return
    
    broadcast_msg = message.reply_to_message
    total_users = await db.total_users_count()
    sent = 0
    failed = 0
    
    status_msg = await message.reply_text("📢 Starting broadcast...")
    
    all_users = await db.get_all_users()
    async for user in all_users:
        try:
            await broadcast_msg.copy(chat_id=user["_id"])
            sent += 1
        except Exception as e:
            print(f"Failed to send to {user['_id']}: {e}")
            failed += 1
        
        if (sent + failed) % 10 == 0:
            await status_msg.edit_text(
                f"📢 Broadcasting...\n\n"
                f"**Sent:** {sent}\n"
                f"**Failed:** {failed}\n"
                f"**Total:** {total_users}"
            )
    
    await status_msg.edit_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"**Total Users:** {total_users}\n"
        f"**✅ Sent:** {sent}\n"
        f"**❌ Failed:** {failed}"
    )

# Restart command (admin only)
@app.on_message(filters.command("restart") & filters.user(Config.ADMIN))
async def restart_handler(client, message):
    await message.reply_text("**🔄 Restarting bot...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# ==================== MAIN ====================
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check for ffmpeg
    if not shutil.which("ffmpeg"):
        print("⚠️ WARNING: ffmpeg not found! Video conversion features will not work.")
        print("Install ffmpeg: sudo apt-get install ffmpeg")
    
    print("🚀 Starting Auto Rename Bot with Pre-Set Media Format...")
    print("🤖 Bot is running. Press Ctrl+C to stop.")
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
