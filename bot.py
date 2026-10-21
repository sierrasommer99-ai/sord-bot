import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set in Environment!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔰 بوت حماية {context.bot.username} شغال 24/7 ✅")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text
    if "http://" in text or "https://" in text or "t.me/" in text:
        try:
            await update.message.delete()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🚫 ممنوع الروابط يا {update.effective_user.first_name}")
        except:
            pass

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_links))
    app.run_polling()

if __name__ == "__main__":
    main()
