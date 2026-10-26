import os, asyncio, threading, time, json
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
user_messages = defaultdict(list)

RANKS_FILE = "ranks.json"
COMMANDS_FILE = "custom_commands.json"

for f in [RANKS_FILE, COMMANDS_FILE]:
    if not os.path.exists(f):
        with open(f, "w") as fp:
            json.dump({}, fp)

def load_json(f):
    try:
        with open(f, "r") as fp:
            return json.load(fp)
    except:
        return {}

def save_json(f, data):
    try:
        with open(f, "w") as fp:
            json.dump(data, fp)
    except: pass

RANKS = load_json(RANKS_FILE)
CUSTOM = load_json(COMMANDS_FILE)

def get_ranks(chat_id):
    chat_id = str(chat_id)
    if chat_id not in RANKS:
        RANKS[chat_id] = {"dev_asasi": [], "dev": [], "dev2": [], "extra": [], "myth": []}
    return RANKS[chat_id]

def get_custom(chat_id):
    chat_id = str(chat_id)
    if chat_id not in CUSTOM:
        CUSTOM[chat_id] = {}
    return CUSTOM[chat_id]

def get_user_rank(chat_id, user_id):
    r = get_ranks(chat_id)
    if user_id in r["dev_asasi"]: return "Dev الاساسي"
    if user_id in r["dev"]: return "Dev"
    if user_id in r["dev2"]: return "Dev 2"
    if user_id in r["extra"]: return "اكسترا"
    if user_id in r["myth"]: return "Myth"
    return "عضو"

PORN_WORDS = ["كس", "زب", "نيك", "xnxx", "porn", "sex", "xxx", "سكس", "طيز", "كسمك"]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SORD Running")

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
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id
    r = get_ranks(chat_id)
    if update.effective_user.username == "ADJkex" and user_id not in r["dev_asasi"]:
        r["dev_asasi"].append(user_id)
        save_json(RANKS_FILE, RANKS)

    text = """• أهلًا بك عزيزي أنا اسمي سورد

━━━━━━━━━━━━━━━
حرفيًا أفضل بوت!
━━━━━━━━━━━━━━━
- حماية شاملة
- أحدث الألعاب والمميزات
- منع التعديل والاباحي وكلشي
━━━━━━━━━━━━━━━
✅ إرفعني مشرف وبتفعل تلقائيًا
━━━━━━━━━━━━━━━
- مطوري ↫ راكان
- @ADJkex"""

    kb = [[InlineKeyboardButton("➕ اضفني لقروبك", url=f"https://t.me/{context.bot.username}?startgroup=true")],
          [InlineKeyboardButton("👨‍💻 المطور راكان", url="https://t.me/ADJkex")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id
    msg = update.message
    text = (msg.text or "").strip()

    # رتبتي - بدون سنايبر
    if text == "رتبتي" and msg.reply_to_message:
        target = msg.reply_to_message.from_user
        rank = get_user_rank(chat_id, target.id)
        await msg.reply_text(f"رتبته => {rank}")
        return
    if text == "رتبتي" and not msg.reply_to_message:
        rank = get_user_rank(chat_id, user_id)
        await msg.reply_text(f"رتبتك => {rank}")
        return

    # الرتب
    if text == "الرتب" or text == "/ranks":
        r = get_ranks(chat_id)
        await msg.reply_text(f"""الرتب:
Dev الاساسي: {len(r['dev_asasi'])}
Dev: {len(r['dev'])}
Dev 2: {len(r['dev2'])}
اكسترا: {len(r['extra'])}
ميث: {len(r['myth'])}""")
        return

    # الاوامر
    if text == "الاوامر" or text == "/commands":
        custom = get_custom(chat_id)
        txt = """الاوامر:
رتبتي - بالرد يطلع رتبته
رفع ديف اساسي / ديف 2 / اكسترا / ميث - بالرد
تنزيل ديف اساسي / ديف 2 / اكسترا / ميث
الرتب - عرض الرتب
اضف امر + الاسم - بالرد على رسالة
حذف امر + الاسم
تغير امر قديم الى جديد
الاوامر - عرض الاوامر

الاوامر المضافة:
"""
        if custom:
            for k in custom.keys():
                txt += f"- {k}\n"
        else:
            txt += "لا يوجد"
        await msg.reply_text(txt)
        return

    # اضف امر
    if text.startswith("اضف امر"):
        name = text.replace("اضف امر", "", 1).strip().lower()
        if not name or not msg.reply_to_message:
            await msg.reply_text("اكتب: اضف امر + الاسم بالرد على رسالة")
            return
        content = msg.reply_to_message.text or msg.reply_to_message.caption or ""
        custom = get_custom(chat_id)
        custom[name] = content
        save_json(COMMANDS_FILE, CUSTOM)
        await msg.reply_text(f"تم اضافة امر {name}")
        return

    # حذف امر
    if text.startswith("حذف امر"):
        name = text.replace("حذف امر", "", 1).strip().lower()
        custom = get_custom(chat_id)
        if name in custom:
            del custom[name]
            save_json(COMMANDS_FILE, CUSTOM)
            await msg.reply_text(f"تم حذف امر {name}")
        else:
            await msg.reply_text("الامر مو موجود")
        return

    # تغير امر
    if text.startswith("تغير امر"):
        rest = text.replace("تغير امر", "", 1).strip()
        if " الى " in rest:
            old, new = rest.split(" الى ", 1)
            old = old.strip().lower()
            new = new.strip().lower()
            custom = get_custom(chat_id)
            if old in custom:
                custom[new] = custom[old]
                del custom[old]
                save_json(COMMANDS_FILE, CUSTOM)
                await msg.reply_text(f"تم تغير امر {old} الى {new}")
            else:
                await msg.reply_text("الامر القديم مو موجود")
        else:
            await msg.reply_text("الصيغة: تغير امر قديم الى جديد")
        return

    # رفع / تنزيل الرتب
    if msg.reply_to_message and ("رفع" in text or "تنزيل" in text):
        r = get_ranks(chat_id)
        if ("ديف اساسي" in text) and user_id not in r["dev_asasi"] and msg.from_user.username != "ADJkex":
            await msg.reply_text("بس Dev الاساسي يقدر!")
            return
        rank = None
        if "ديف اساسي" in text: rank = "dev_asasi"
        elif "ديف 2" in text or "ديف2" in text: rank = "dev2"
        elif "اكسترا" in text: rank = "extra"
        elif "ميث" in text: rank = "myth"
        elif "ديف" in text: rank = "dev"
        if rank:
            tid = msg.reply_to_message.from_user.id
            tname = msg.reply_to_message.from_user.first_name
            if "رفع" in text:
                if tid not in r[rank]:
                    r[rank].append(tid)
                    save_json(RANKS_FILE, RANKS)
                    await msg.reply_text(f"تم رفع {tname} {rank}")
            else:
                if tid in r[rank]:
                    r[rank].remove(tid)
                    save_json(RANKS_FILE, RANKS)
                    await msg.reply_text(f"تم تنزيل {tname}")
            return

    # تشغيل الاوامر المضافة
    custom = get_custom(chat_id)
    if text.lower() in custom:
        await msg.reply_text(custom[text.lower()])
        return

    # حماية
    if await is_admin(update): return
    r = get_ranks(chat_id)
    if user_id in r["dev_asasi"] or user_id in r["dev"] or user_id in r["dev2"] or user_id in r["extra"] or user_id in r["myth"]:
        return
    low = text.lower()
    for bad in PORN_WORDS:
        if bad in low:
            try: await msg.delete(); return
            except: pass
    if any(x in low for x in ["http://","https://","t.me/","www."]):
        try: await msg.delete(); return
        except: pass
    if msg.forward_from or msg.forward_from_chat:
        try: await msg.delete(); return
        except: pass
    now = time.time()
    user_messages[user_id].append(now)
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < 8]
    if len(user_messages[user_id]) > 4:
        try:
            await update.effective_chat.restrict_member(user_id, permissions=None, until_date=int(now+300))
            user_messages[user_id] = []
        except: pass

async def anti_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.edited_message: return
    if update.effective_chat.type == "private": return
    chat_id = str(update.effective_chat.id)
    r = get_ranks(chat_id)
    uid = update.edited_message.from_user.id if update.edited_message.from_user else None
    if uid and (uid in r["dev_asasi"] or uid in r["dev"] or uid in r["dev2"]):
        return
    try:
        await update.edited_message.delete()
    except: pass

if __name__ == "__main__":
    if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN missing")
    threading.Thread(target=run_server, daemon=True).start()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except: pass
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all))
    app.add_handler(MessageHandler(filters.ALL & ~filters.UpdateType.EDITED_MESSAGE, handle_all))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, anti_edit))
    print("SORD Old UI - No Channel - Full Features running...")
    app.run_polling()
