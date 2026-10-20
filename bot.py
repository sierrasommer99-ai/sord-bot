from telegram.ext import Application,CommandHandler,MessageHandler,filters
import os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
TOKEN = os.getenv("BOT_TOKEN", "8769832522:AAE-Ik4lcdvn1N06a3qKC0rj4THzKWyhq-M")
async def start(u,c):
    await u.message.reply_text("بوت سورد شغال 24/7 ✅")
async def prot(u,c):
    if not u.message or not u.message.text: return
    t = u.message.text.lower()
    if "http" in t or "t.me/" in t:
        try: await u.message.delete()
        except: pass
async def antiedit(u,c):
    try:
        await u.edited_message.delete()
        await c.bot.send_message(chat_id=u.effective_chat.id, text="ممنوع تعديل الرسائل 🚫")
    except: pass
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Alive")
def run_health():
    port = int(os.getenv("PORT", "8000"))
    HTTPServer(("0.0.0.0", port), H).serve_forever()
def main():
    threading.Thread(target=run_health, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, antiedit))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, prot))
    app.run_polling()
if __name__ == "__main__":
    main()
