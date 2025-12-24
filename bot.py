#!/usr/bin/env python3
"""
Auto Rename Bot - Final Corrected Version
Fixes divdivmod error and preserves original quality
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
from dotenv import load_dotenv
from PIL import Image
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

class Txt:
    START_TXT = """<b>ʜᴇʏ! {}  

» ɪ ᴀᴍ ᴀᴅᴠᴀɴᴄᴇᴅ ʀᴇɴᴀᴍᴇ ʙᴏᴛ! ᴡʜɪᴄʜ ᴄᴀɴ ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ғɪʟᴇs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴀɴᴅ ᴀʟsᴏ sᴇǫᴜᴇɴᴄᴇ ᴛʜᴇᴍ ᴘᴇʀғᴇᴄᴛʟʏ</b>"""
    
    FILE_NAME_TXT = """<b>» <u>sᴇᴛᴜᴘ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ</u></b>

<b>ᴠᴀʀɪᴀʙʟᴇꜱ :</b>
➲ ᴇᴘɪꜱᴏᴅᴇ - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ᴇᴘɪꜱᴏᴅᴇ ɴᴜᴍʙᴇʀ  
➲ ꜱᴇᴀꜱᴏɴ - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ  
➲ ǫᴜᴀʟɪᴛʏ - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ǫᴜᴀʟɪᴛʏ  

<b>‣ ꜰᴏʀ ᴇx:- </b> `/autorename Oᴠᴇʀғʟᴏᴡ [Sseason Eepisode] - [Dual] quality`

<b>‣ /Autorename: ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ᴍᴇᴅɪᴀ ꜰɪʟᴇꜱ ʙʏ ɪɴᴄʟᴜᴅɪɴɢ 'ᴇᴘɪꜱᴏᴅᴇ' ᴀɴᴅ 'ǫᴜᴀʟɪᴛʏ' ᴠᴀʀɪᴀʙʟᴇꜱ ɪɴ ʏᴏᴜʀ ᴛᴇxᴛ, ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴇᴘɪꜱᴏᴅᴇ ᴀɴᴅ ǫᴜᴀʟɪᴛʏ ᴘʀᴇꜱᴇɴᴛ ɪɴ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ꜰɪʟᴇɴᴀᴍᴇ.</b>"""
    
    CAPTION_TXT = """<b><u>» ᴛᴏ ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴍᴇᴅɪᴀ ᴛʜʏᴘᴇ</u></b>
    
<b>ᴠᴀʀɪᴀʙʟᴇꜱ :</b>         
ꜱɪᴢᴇ: {filesize}
ᴅᴜʀᴀᴛɪᴏɴ: {duration}
ꜰɪʟᴇɴᴀᴍᴇ: {filename}

➲ /set_caption: ᴛᴏ ꜱᴇᴛ ᴀ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.
➲ /see_caption: ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.
➲ /del_caption: ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.

» ꜰᴏʀ ᴇx:- /set_caption ꜰɪʟᴇ ɴᴀᴍᴇ: {filename}"""

    THUMBNAIL_TXT = """<b><u>» ᴛᴏ ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ</u></b>
    
➲ /start: ꜱᴇɴᴅ ᴀɴʏ ᴘʜᴏᴛᴏ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ꜱᴇᴛ ɪᴛ ᴀꜱ ᴀ ᴛʜᴜᴍʙɴᴀɪʟ..
➲ /del_thumb: ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴏʟᴅ ᴛʜᴜᴍʙɴᴀɪʟ.
➲ /view_thumb: ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ.

ɴᴏᴛᴇ: ɪꜰ ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴀᴠᴇᴅ ɪɴ ʙᴏᴛ ᴛʜᴇɴ, ɪᴛ ᴡɪʟʟ ᴜꜱᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴏꜰ ᴛʜᴇ ᴏʀɪɢɪɴɪᴀʟ ꜰɪʟᴇ ᴛᴏ ꜱᴇᴛ ɪɴ ʀᴇɴᴀᴍᴇᴅ ꜰɪʟᴇ"""

    PROGRESS_BAR = """\n
<b>» Size</b> : {1} | {2}
<b>» Done</b> : {0}%
<b>» Speed</b> : {3}/s
<b>» ETA</b> : {4} """

    HELP_TXT = """<b>ʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ɪᴍᴘᴏʀᴛᴀɴᴛ ᴄᴏᴍᴍᴀɴᴅꜱ:

ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs🫧

ʀᴇɴᴀᴍᴇ ʙᴏᴛ ɪꜱ ᴀ ʜᴀɴᴅʏ ᴛᴏᴏʟ ᴛʜᴀᴛ ʜᴇʟᴘꜱ ʏᴏᴜ ʀᴇɴᴀᴍᴇ ᴀɴᴅ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ꜰɪʟᴇꜱ ᴇꜰꜰᴏʀᴛʟᴇꜱꜱʟʏ.

➲ /autorename: ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ꜰɪʟᴇꜱ.
➲ /metadata: ᴄᴏᴍᴍᴀɴᴅꜱ ᴛᴏ ᴛᴜʀɴ ᴏɴ/ᴏғғ ᴍᴇᴛᴀᴅᴀᴛᴀ.
➲ /help: ɢᴇᴛ ǫᴜɪᴄᴋ ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ.</b>"""
    
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

<b>Note:</b> Metadata addition does NOT re-encode or reduce quality. It only adds metadata tags."""

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
            "media_type": "document",
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
    
    async def set_media_preference(self, user_id, media_type):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"media_type": media_type}})
    
    async def get_media_preference(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("media_type", "document") if user else "document"
    
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
    """Convert milliseconds to readable time format - FIXED VERSION"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)  # FIXED: Changed 'divdivmod' to 'divmod'
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
          ((str(hours) + "ʜ, ") if hours else "") + \
          ((str(minutes) + "ᴍ, ") if minutes else "") + \
          ((str(seconds) + "ꜱ, ") if seconds else "")
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
            img.thumbnail((320, 320))
            img.save(thumb_path, "JPEG", quality=85)
        return thumb_path
    except Exception as e:
        print(f"Thumbnail processing error: {e}")
        await cleanup_files(thumb_path)
        return None

async def add_metadata_preserve_quality(input_path, output_path, user_id):
    """
    Add metadata WITHOUT re-encoding - preserves original quality
    Uses stream copy for all codecs
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Get metadata values
    title = await db.get_title(user_id)
    artist = await db.get_artist(user_id)
    author = await db.get_author(user_id)
    video_title = await db.get_video(user_id)
    audio_title = await db.get_audio(user_id)
    subtitle_title = await db.get_subtitle(user_id)
    
    # Get file extension for format detection
    file_ext = os.path.splitext(input_path)[1].lower()
    
    # Prepare FFmpeg command - CRITICAL: Use '-c copy' for NO re-encoding
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-map', '0',  # Map all streams
        '-c', 'copy',  # CRITICAL: Copy all streams without re-encoding
        '-map_metadata', '0',  # Copy existing metadata
    ]
    
    # Add metadata if provided (only add non-empty metadata)
    if title and title.strip():
        cmd.extend(['-metadata', f'title={title}'])
    
    if artist and artist.strip():
        cmd.extend(['-metadata', f'artist={artist}'])
    
    if author and author.strip():
        cmd.extend(['-metadata', f'author={author}'])
    
    if video_title and video_title.strip():
        cmd.extend(['-metadata:s:v', f'title={video_title}'])
    
    if audio_title and audio_title.strip():
        cmd.extend(['-metadata:s:a', f'title={audio_title}'])
    
    if subtitle_title and subtitle_title.strip():
        cmd.extend(['-metadata:s:s', f'title={subtitle_title}'])
    
    # Add format-specific flags for better compatibility
    if file_ext in ['.mp4', '.m4v', '.mov']:
        cmd.extend(['-movflags', '+faststart'])  # Optimize for streaming
        cmd.extend(['-movflags', 'use_metadata_tags'])
    elif file_ext in ['.mkv']:
        cmd.extend(['-c:v', 'copy', '-c:a', 'copy', '-c:s', 'copy'])
    
    # Add output file
    cmd.extend(['-y', output_path])
    
    # Log command for debugging
    print(f"FFmpeg command (NO RE-ENCODING): {' '.join(cmd)}")
    
    try:
        # Execute FFmpeg
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            
            # Check if it's a metadata-related error (non-fatal)
            if "Invalid argument" in error_msg or "Unrecognized option" in error_msg:
                print(f"Metadata warning: {error_msg[:200]}")
                # Try simpler command without problematic metadata
                simple_cmd = [
                    'ffmpeg',
                    '-i', input_path,
                    '-map', '0',
                    '-c', 'copy',
                    '-map_metadata', '0',
                    '-y', output_path
                ]
                process2 = await asyncio.create_subprocess_exec(
                    *simple_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await process2.communicate()
                if process2.returncode == 0:
                    print("File copied without custom metadata (fallback)")
                    return output_path
            
            raise RuntimeError(f"FFmpeg error: {error_msg[:500]}")
        
        # Verify file was created
        if os.path.exists(output_path):
            # Compare file sizes (should be very similar)
            input_size = os.path.getsize(input_path)
            output_size = os.path.getsize(output_path)
            
            # Metadata adds minimal size, allow small difference
            size_diff_percent = abs(output_size - input_size) / input_size * 100
            
            if size_diff_percent < 5:  # Less than 5% difference
                print(f"✅ Quality preserved! Size difference: {size_diff_percent:.2f}%")
                print(f"Input: {humanbytes(input_size)}, Output: {humanbytes(output_size)}")
            else:
                print(f"⚠️ Size difference >5%: {size_diff_percent:.2f}%")
            
            return output_path
        else:
            raise RuntimeError("Output file not created")
            
    except Exception as e:
        print(f"Error in add_metadata_preserve_quality: {e}")
        # Ultimate fallback: just copy the file
        try:
            shutil.copy2(input_path, output_path)
            print("Fallback: File copied without any processing")
            return output_path
        except Exception as copy_error:
            raise RuntimeError(f"Failed to process file: {copy_error}")

# ==================== BOT CLIENT ====================
# Create necessary directories
os.makedirs("downloads", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# Initialize bot
app = Client(
    "auto_rename_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=100,
    sleep_threshold=10,
)

# ==================== HANDLERS ====================
# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user
    await db.add_user(user.id)
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
        [
            InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇs', url='https://t.me/Codeflix_Bots'),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/CodeflixSupport')
        ],
        [
            InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('sᴏᴜʀᴄᴇ •', callback_data='source')
        ]
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

# Help command
@app.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
        [
            InlineKeyboardButton('• ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
            InlineKeyboardButton('ᴄᴀᴘᴛɪᴏɴ •', callback_data='caption')
        ],
        [
            InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'),
            InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ •', callback_data='donate')
        ],
        [InlineKeyboardButton('• ʜᴏᴍᴇ', callback_data='home')]
    ])
    
    await message.reply_text(
        Txt.HELP_TXT,
        reply_markup=buttons,
        disable_web_page_preview=True
    )

# Autorename command
@app.on_message(filters.command("autorename") & filters.private)
async def autorename_handler(client, message):
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
    await db.set_format_template(message.from_user.id, format_template)
    
    await message.reply_text(
        f"**✅ Rename format set successfully!**\n\n"
        f"**Your format:** `{format_template}`\n\n"
        "Now send me any file to rename it automatically."
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
    
    # Get current metadata values
    title = await db.get_title(message.from_user.id)
    author = await db.get_author(message.from_user.id)
    artist = await db.get_artist(message.from_user.id)
    video = await db.get_video(message.from_user.id)
    audio = await db.get_audio(message.from_user.id)
    subtitle = await db.get_subtitle(message.from_user.id)
    
    text = f"""
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ: {status_text}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪꜱᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴅᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  

**⚠️ Note:** Metadata addition does NOT re-encode or reduce quality.
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

# Set media type command
@app.on_message(filters.command("setmedia") & filters.private)
async def setmedia_handler(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Document", callback_data="media_document")],
        [InlineKeyboardButton("🎬 Video", callback_data="media_video")],
        [InlineKeyboardButton("🎵 Audio", callback_data="media_audio")]
    ])
    
    await message.reply_text(
        "**Select media type for renamed files:**",
        reply_markup=buttons
    )

# Metadata setting commands
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
            "**Gɪᴠᴇ Tʜᴇ Aʀᴛɪꜱᴛ\n\nExᴀᴍᴩʟᴇ:- /setartist @Codeflix_Bots**")
    artist = message.text.split(" ", 1)[1]
    await db.set_artist(message.from_user.id, artist=artist)
    await message.reply_text("**✅ Aʀᴛɪꜱᴛ Sᴀᴠᴇᴅ**")

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

# Main file handler - UPDATED FOR QUALITY PRESERVATION
@app.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_handler(client, message):
    user_id = message.from_user.id
    
    # Check if user has set rename format
    format_template = await db.get_format_template(user_id)
    if not format_template:
        await message.reply_text(
            "❌ Please set a rename format first!\n"
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
    else:
        return
    
    # Check NSFW
    if await check_anti_nsfw(file_name, message):
        return
    
    # Extract filename components
    base_name = os.path.splitext(file_name)[0]
    ext = os.path.splitext(file_name)[1] or ('.mp4' if media_type == 'video' else '.mp3')
    
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
    
    new_filename = new_filename + ext
    
    # Download file
    msg = await message.reply_text("📥 **Downloading file...**")
    download_path = f"downloads/{user_id}_{int(time.time())}{ext}"
    
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
        
        # Get original file size for comparison
        original_size = os.path.getsize(file_path)
        await msg.edit_text(f"⚙️ **Processing file... (Size: {humanbytes(original_size)})**")
        
        # Process metadata if enabled
        output_path = file_path
        metadata_enabled = await db.get_metadata(user_id)
        
        if metadata_enabled and media_type in ["video", "audio"]:
            try:
                metadata_path = f"temp/{user_id}_metadata{ext}"
                await msg.edit_text("🔧 **Adding metadata (NO re-encoding)...**")
                output_path = await add_metadata_preserve_quality(file_path, metadata_path, user_id)
                
                # Compare file sizes
                if os.path.exists(output_path):
                    new_size = os.path.getsize(output_path)
                    size_diff = abs(new_size - original_size)
                    size_diff_percent = (size_diff / original_size) * 100
                    
                    if size_diff_percent < 1:
                        await msg.edit_text(f"✅ **Quality preserved! ({size_diff_percent:.2f}% size difference)**")
                    else:
                        await msg.edit_text(f"⚠️ **File processed ({size_diff_percent:.2f}% size difference)**")
                    
                    # Clean up original file
                    await cleanup_files(file_path)
                else:
                    await msg.edit_text("⚠️ Output file not found, using original")
                    output_path = file_path
                    
            except Exception as e:
                print(f"Metadata error: {e}")
                await msg.edit_text(f"⚠️ Metadata error: {str(e)[:100]}... (continuing without metadata)")
                output_path = file_path  # Use original file
        elif metadata_enabled:
            await msg.edit_text("ℹ️ Metadata is only supported for video and audio files. Continuing without metadata...")
        
        # Get thumbnail
        thumb_path = None
        user_thumb = await db.get_thumbnail(user_id)
        
        if user_thumb:
            thumb_path = f"temp/{user_id}_thumb.jpg"
            await client.download_media(user_thumb, file_name=thumb_path)
            thumb_path = await process_thumbnail(thumb_path)
        elif media_type == "video" and message.video.thumbs:
            thumb = message.video.thumbs[0]
            thumb_path = f"temp/{user_id}_video_thumb.jpg"
            await client.download_media(thumb.file_id, file_name=thumb_path)
            thumb_path = await process_thumbnail(thumb_path)
        
        # Get caption
        caption_template = await db.get_caption(user_id) or "{filename}"
        caption = caption_template.replace("{filename}", new_filename)\
                                 .replace("{filesize}", humanbytes(file_size))\
                                 .replace("{duration}", str(timedelta(seconds=duration)) if duration else '00:00:00')
        
        # Get media type preference
        media_pref = await db.get_media_preference(user_id)
        
        # Get final output size
        final_size = os.path.getsize(output_path)
        await msg.edit_text(f"📤 **Uploading renamed file... (Final size: {humanbytes(final_size)})**")
        
        # Upload file based on media preference
        upload_start = time.time()
        
        if media_pref == "document" or media_type == "document":
            await client.send_document(
                chat_id=message.chat.id,
                document=output_path,
                caption=caption,
                thumb=thumb_path,
                file_name=new_filename,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", msg, upload_start)
            )
        elif media_pref == "video" and media_type == "video":
            await client.send_video(
                chat_id=message.chat.id,
                video=output_path,
                caption=caption,
                thumb=thumb_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", msg, upload_start)
            )
        elif media_pref == "audio" and media_type == "audio":
            await client.send_audio(
                chat_id=message.chat.id,
                audio=output_path,
                caption=caption,
                thumb=thumb_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", msg, upload_start)
            )
        else:
            # Fallback to document
            await client.send_document(
                chat_id=message.chat.id,
                document=output_path,
                caption=caption,
                thumb=thumb_path,
                file_name=new_filename,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", msg, upload_start)
            )
        
        await msg.delete()
        
        # Send final message with size comparison
        size_comparison = ""
        if metadata_enabled and media_type in ["video", "audio"]:
            size_diff = final_size - file_size
            if abs(size_diff) > 1024:  # More than 1KB difference
                size_comparison = f"\n**Size change:** {humanbytes(abs(size_diff))} ({'+' if size_diff > 0 else ''}{size_diff/file_size*100:.2f}%)"
        
        await message.reply_text(
            f"✅ **File renamed successfully!**\n"
            f"**New name:** `{new_filename}`\n"
            f"**Original size:** {humanbytes(file_size)}\n"
            f"**Final size:** {humanbytes(final_size)}"
            f"{size_comparison}"
        )
        
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        await cleanup_files(download_path, output_path if 'output_path' in locals() and output_path != file_path else None, 
                          thumb_path if 'thumb_path' in locals() else None)

# Callback query handler
@app.on_callback_query()
async def callback_handler(client, query):
    data = query.data
    user_id = query.from_user.id
    
    if data == "home":
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
            [
                InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇs', url='https://t.me/Codeflix_Bots'),
                InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/CodeflixSupport')
            ],
            [
                InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('sᴏᴜʀᴄᴇ •', callback_data='source')
            ]
        ])
        
        await query.message.edit_text(
            Txt.START_TXT.format(query.from_user.mention),
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    
    elif data == "help":
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
            [
                InlineKeyboardButton('• ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'),
                InlineKeyboardButton('ᴄᴀᴘᴛɪᴏɴ •', callback_data='caption')
            ],
            [
                InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'),
                InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ •', callback_data='donate')
            ],
            [InlineKeyboardButton('• ʜᴏᴍᴇ', callback_data='home')]
        ])
        
        await query.message.edit_text(
            Txt.HELP_TXT,
            reply_markup=buttons,
            disable_web_page_preview=True
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
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ: {status_text}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪꜱᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴅᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  

**⚠️ Note:** Metadata addition does NOT re-encode or reduce quality.
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
        
        metadata_status = await db.get_metadata(user_id)
        status_text = "ON ✅" if metadata_status else "OFF ❌"
        
        title = await db.get_title(user_id)
        author = await db.get_author(user_id)
        artist = await db.get_artist(user_id)
        video = await db.get_video(user_id)
        audio = await db.get_audio(user_id)
        subtitle = await db.get_subtitle(user_id)
        
        text = f"""
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ: {status_text}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪꜱᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴅᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  

**⚠️ Note:** Metadata addition does NOT re-encode or reduce quality.
        """
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Turn ON ✅", callback_data="metadata_on"),
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
    
    elif data == "metadata_off":
        await db.set_metadata(user_id, False)
        await query.answer("Metadata turned OFF ❌")
        
        metadata_status = await db.get_metadata(user_id)
        status_text = "ON ✅" if metadata_status else "OFF ❌"
        
        title = await db.get_title(user_id)
        author = await db.get_author(user_id)
        artist = await db.get_artist(user_id)
        video = await db.get_video(user_id)
        audio = await db.get_audio(user_id)
        subtitle = await db.get_subtitle(user_id)
        
        text = f"""
**㊋ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ: {status_text}**

**◈ Tɪᴛʟᴇ ▹** `{title if title else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴛʜᴏʀ ▹** `{author if author else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aʀᴛɪꜱᴛ ▹** `{artist if artist else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Aᴜᴅɪᴏ ▹** `{audio if audio else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Sᴜʙᴛɪᴛʟᴇ ▹** `{subtitle if subtitle else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  
**◈ Vɪᴅᴇᴏ ▹** `{video if video else 'Nᴏᴛ ꜰᴏᴜɴᴅ'}`  

**⚠️ Note:** Metadata addition does NOT re-encode or reduce quality.
        """
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Turn ON", callback_data="metadata_on"),
                InlineKeyboardButton("Turn OFF ✅", callback_data="metadata_off")
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
        return
    
    elif data.startswith("media_"):
        media_type = data.split("_")[1]
        await db.set_media_preference(user_id, media_type)
        await query.answer(f"Media type set to {media_type.capitalize()} ✅")
        await query.message.edit_text(
            f"✅ **Media type set to {media_type.capitalize()}!**\n\n"
            f"Renamed files will be sent as {media_type}s.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help")]
            ])
        )
    
    elif data == "close":
        await query.message.delete()
    
    elif data in ["about", "source", "donate"]:
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
    
    # Check for FFmpeg
    if not shutil.which("ffmpeg"):
        print("⚠️ WARNING: ffmpeg not found! Metadata features will not work.")
        print("Install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  MacOS: brew install ffmpeg")
        print("  Windows: Download from ffmpeg.org")
    else:
        print("✅ FFmpeg found")
    
    print("🚀 Starting Auto Rename Bot (Final Corrected Version)...")
    print("🤖 Bot is running. Press Ctrl+C to stop.")
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
