import os, asyncio, threading, time
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
user_messages = defaultdict(list)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SORD Bot Running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(('0.0.0.0', port), Handler)
    httpd.serve_forever()

async def is_admin(update: Update):
    try:
        m = await update.effective_chat.get_member(update.effective_user.id)
        return m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """• أهلًا بك عزيزي أنا اسمي سورد

━━━━━━━━━━━━━━━
حرفيًا أفضل بوت!
━━━━━━━━━━━━━━━
- حماية شاملة
- أحدث الألعاب والمميزات
━━━━━━━━━━━━━━━
✅ إرفعني مشرف وبتفعل تلقائيًا
✅ اكتب الاعدادات
━━━━━━━━━━━━━━━
- مطوري ↫ راكان"""

    kb = [[InlineKeyboardButton("➕ اضفني لقروبك", url=f"https://t.me/{context.bot.username}?startgroup=true")],
          [InlineKeyboardButton("👨‍💻 المطور راكان", url="https://t.me/ADJkex")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🔰 الحماية", callback_data="prot"), InlineKeyboardButton("🎮 الألعاب", callback_data="games")],
          [InlineKeyboardButton("🔒 قفل الروابط", callback_data="lock"), InlineKeyboardButton("🔓 فتح الروابط", callback_data="unlock")]]
    await update.message.reply_text("⚙️ لوحة تحكم سورد - تطوير راكان", reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "prot":
        await q.edit_message_text("🔰 حماية سورد شغالة:\n- حذف الروابط\n- حذف التوجيه\n- منع السبام")
    elif q.data == "games":
        await q.edit_message_text("🎮 ألعاب سورد قريبًا!")
    else:
        await q.edit_message_text(f"تم: {q.data} - بوت سورد")

async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.effective_chat.type == "private": return
    if await is_admin(update): return
    txt = update.message.text or update.message.caption or ""
    if txt == "الاعدادات":
        await settings(update, context)
        return
    if any(x in txt for x in ["http://","https://","t.me/","@"]):
        try: await update.message.delete(); return
        except: pass
    if update.message.forward_from or update.message.forward_from_chat:
        try: await update.message.delete(); return
        except: pass
    now = time.time()
    uid = update.effective_user.id
    user_messages[uid].append(now)
    user_messages[uid] = [t for t in user_messages[uid] if now - t < 10]
    if len(user_messages[uid]) > 5:
        try:
            await update.effective_chat.restrict_member(uid, permissions=None, until_date=int(now+300))
            user_messages[uid] = []
        except: pass

if __name__ == "__main__":
    if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN missing")
    threading.Thread(target=run_server, daemon=True).start()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except: pass
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start
