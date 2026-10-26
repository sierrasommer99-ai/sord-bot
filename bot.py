import os, asyncio, threading, time, random
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()

user_messages = defaultdict(list)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ARIN Bot Running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(('0.0.0.0', port), Handler)
    httpd.serve_forever()

async def is_admin(update: Update):
    try:
        member = await update.effective_chat.get_member(update.effective_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """• أهلًا بك عزيزي أنا اسمي ارين

━━━━━━━━━━━━━━━
حرفيًا أفضل بوت!
━━━━━━━━━━━━━━━
- حماية شاملة
- أحدث الألعاب والمميزات  
- تحديثات وإضافات مستمرة
━━━━━━━━━━━━━━━
✅ إرفعني مشرف وبتفعل تلقائيًا
✅ اكتب الاعدادات وضبط اعداداتي!
━━━━━━━━━━━━━━━
• مطوري ↫ راكان
• Source Soul"""

    keyboard = [
        [InlineKeyboardButton("➕ اضفني لقروبك", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("👨‍💻 المطور راكان", url="https://t.me/Rakan")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔰 الحماية", callback_data="protection"), InlineKeyboardButton("🎮 الألعاب", callback_data="games")],
        [InlineKeyboardButton("👋 الترحيب", callback_data="welcome"), InlineKeyboardButton("⚙️ الاعدادات العامة", callback_data="general")],
        [InlineKeyboardButton("🔒 قفل الروابط", callback_data="lock_links"), InlineKeyboardButton("🔓 فتح الروابط", callback_data="unlock_links")],
        [InlineKeyboardButton("🔒 قفل التوجيه", callback_data="lock_fwd"), InlineKeyboardButton("🔓 فتح التوجيه", callback_data="unlock_fwd")],
    ]
    await update.message.reply_text("⚙️ لوحة تحكم بوت ارين - المطور راكان:\n\nاختر القسم:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "protection":
        await query.edit_message_text("🔰 اعدادات الحماية - بوت راكان:\n\n• قفل الروابط: شغال\n• قفل التوجيه: شغال\n• منع السبام: شغال")
    elif data == "games":
        keyboard = [
            [InlineKeyboardButton("✊ حجر ورقة مقص", callback_data="game_rps")],
            [InlineKeyboardButton("🎲 حظك اليوم", callback_data="game_luck")],
        ]
        await query.edit_message_text("🎮 ألعاب بوت راكان:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "game_luck":
        luck = random.choice(["حظك اليوم ممتاز يا راكان 🔥", "حظك متوسط 😐", "حظك سيء اليوم 😅", "بتفوز بشي كبير قريب 🎉"])
        await query.edit_message_text(f"🎲 {luck}")
    elif "lock" in data or "unlock" in data:
        status = "تم القفل 🔒" if "lock" in data else "تم الفتح 🔓"
        await query.edit_message_text(f"{status} بواسطة بوت راكان")

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✊ حجر ورقة مقص", callback_data="game_rps")],
        [InlineKeyboardButton("🎲 حظك اليوم", callback_data="game_luck")],
    ]
    await update.message.reply_text("🎮 ألعاب بوت ارين - تطوير راكان:", reply_markup=InlineKeyboardMarkup(keyboard))

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    if not update.message.reply_to_message:
        await update.message.reply_text("رد على رسالة الشخص")
        return
    try:
        await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id)
        await update.message.reply_text(f"🚫 تم حظر {update.message.reply_to_message.from_user.first_name}")
    except: pass

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update): return
    if not update.message.reply_to_message: return
    try:
        uid = update.message.reply_to_message.from_user.id
        await update.effective_chat.ban_member(uid)
        await update.effective_chat.unban_member(uid)
        await update.message.reply_text(f"👢 تم طرد {update.message.reply_to_message.from_user.first_name}")
    except: pass

async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.effective_chat.type == "private": return
    if await is_admin(update): return
    text = update.message.text or update.message.caption or ""
    if any(x in text for x in ["http://","https://","t.me/","@"]):
        try: await update.message.delete(); return
        except: pass
   
