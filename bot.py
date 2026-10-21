from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import os, threading, time
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    TOKEN = "8769832522:AAE-Ik4lcdvn1N06a3qKC0rj4THzKWyhq-M"

user_messages = defaultdict(list)

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat or update.effective_chat.type == "private":
        return True
    try:
        m = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        return m.status in ["administrator","creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔰 بوت حماية @kpcukbot7454_bot شغال 24/7 ✅\n\nالحماية:\n• حذف الروابط\n• منع تعديل الرسائل\n• منع @all\n• منع الفلود\n• منع التوجيه\n• منع اضافة البوتات")

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    if await is_admin(update, context): return
    t = update.message.text.lower()
    bad = ["http://","https://","t.me/","telegram.me","www.",".com",".net",".org",".io",".me/"]
    if any(x in t for x in bad):
        try: await update.message.delete()
        except: pass

async def anti_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if await is_admin(update, context): return
        if update.edited_message:
            await update.edited_message.delete()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚫 ممنوع تعديل الرسائل يا {update.effective_user.first_name}")
    except: pass

async def anti_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    if await is_admin(update, context): return
    t = update.message.text.lower()
    if "@all" in t or "@everyone" in t or "@here" in t:
        try: await update.message.delete()
        except: pass

async def anti_flood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user: return
    if await is_admin(update, context): return
    uid = update.effective_user.id
    now = time.time()
    user_messages[uid].append(now)
    user_messages[uid] = [x for x in user_messages[uid] if now - x < 5]
    if len(user_messages[uid]) > 4:
        try:
            await update.message.delete()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"⚠️ {update.effective_user.first_name} لا تكرر (فلود)")
        except: pass

async def anti_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    if await is_admin(update, context): return
    if update.message.forward_from or update.message.forward_from_chat:
        try: await update.message.delete()
        except: pass

async def anti_bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members: return
    for member in update.message.new_chat_members:
        if member.is_bot:
            try:
                await context.bot.ban_chat_member(update.effective_chat.id, member.id)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚫 تم طرد البوت {member.username}")
            except: pass

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"@kpcukbot7454_bot Alive 24/7")

def run_health():
    port = int(os.getenv("PORT","10000"))
    HTTPServer(("0.0.0.0",port), H).serve_forever()

def main():
    threading.Thread(target=run_health, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, anti_edit))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, anti_bots))
    app.add_handler(MessageHandler(filters.FORWARDED, anti_forward))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"@all|@everyone|@here"), anti_mention))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_link))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_flood))
    print("BOT @kpcukbot7454_bot STARTED")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
