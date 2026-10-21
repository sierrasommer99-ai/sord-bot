from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import os, threading, time
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN") or "8769832522:AAE-Ik4lcdvn1N06a3qKC0rj4THzKWyhq-M"
user_messages = defaultdict(list)

async def is_admin(update, context):
    if not update.effective_chat or update.effective_chat.type == "private": return True
    try:
        m = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        return m.status in ["administrator","creator"]
    except: return False

async def start(update, context):
    await update.message.reply_text("🔰 بوت حماية @kpcukbot7454_bot شغال 24/7 ✅")

async def all_protection(update, context):
    if not update.message: return
    if await is_admin(update, context): return
    if update.message.new_chat_members:
        for mem in update.message.new_chat_members:
            if mem.is_bot:
                try: await context.bot.ban_chat_member(update.effective_chat.id, mem.id)
                except: pass
        return
    if update.message.forward_from or update.message.forward_from_chat:
        try: await update.message.delete()
        except: pass
        return
    if not update.message.text: return
    t = update.message.text.lower()
    if "@all" in t or "@everyone" in t:
        try: await update.message.delete()
        except: pass
        return
    bad = ["http://","https://","t.me/","www.",".com",".net",".org"]
    if any(x in t for x in bad):
        try: await update.message.delete()
        except: pass
        return
    if update.effective_user:
        uid = update.effective_user.id
        now = time.time()
        user_messages[uid].append(now)
        user_messages[uid] = [x for x in user_messages[uid] if now - x < 5]
        if len(user_messages[uid]) > 4:
            try: await update.message.delete()
            except: pass

async def anti_edit(update, context):
    try:
        if await is_admin(update, context): return
        if update.edited_message: await update.edited_message.delete()
    except: pass

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Alive")

def run_health():
    port = int(os.getenv("PORT","10000"))
    HTTPServer(("0.0.0.0",port), H).serve_forever()

def main():
    threading.Thread(target=run_health, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, anti_edit))
    app.add_handler(MessageHandler(filters.ALL, all_protection))
    print("BOT STARTED")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__": main()
