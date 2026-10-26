import os, asyncio, threading, time, json, random
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
user_messages = defaultdict(list)

RANKS_FILE = "ranks.json"
STATS_FILE = "stats.json"
CUSTOM_FILE = "custom_commands.json"
MEDIA_FILE = "media_log.json"

for f in [RANKS_FILE, STATS_FILE, CUSTOM_FILE, MEDIA_FILE]:
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
    except:
        pass

RANKS = load_json(RANKS_FILE)
STATS = load_json(STATS_FILE)
CUSTOM = load_json(CUSTOM_FILE)
MEDIA_LOG = load_json(MEDIA_FILE)

def get_ranks(cid):
    cid = str(cid)
    if cid not in RANKS:
        RANKS[cid] = {"dev2": [], "dev": [], "myth_badge": [], "myth": [], "dev_asasi": []}
    return RANKS[cid]

def get_stats(cid):
    cid = str(cid)
    if cid not in STATS:
        STATS[cid] = {}
    return STATS[cid]

def get_custom(cid):
    cid = str(cid)
    if cid not in CUSTOM:
        CUSTOM[cid] = {}
    return CUSTOM[cid]

def get_media_log(cid):
    cid = str(cid)
    if cid not in MEDIA_LOG:
        MEDIA_LOG[cid] = []
    return MEDIA_LOG[cid]

def get_rank_name(cid, uid):
    r = get_ranks(cid)
    if uid in r["dev_asasi"]:
        return "Dev² 🎖️"
    if uid in r["dev2"]:
        return "Dev² 🎖️"
    if uid in r["dev"]:
        return "Dev 🎖️"
    if uid in r["myth_badge"]:
        return "Myth 🎖️"
    if uid in r["myth"]:
        return "Myth"
    return "عضو"

PORN_WORDS = ["كس", "زب", "نيك", "xnxx", "porn", "sex", "xxx", "سكس", "طيز"]

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
    cid = str(update.effective_chat.id)
    uid = update.effective_user.id
    r = get_ranks(cid)
    if update.effective_user.username == "ADJkex" and uid not in r["dev_asasi"]:
        r["dev_asasi"].append(uid)
        if uid not in r["dev2"]:
            r["dev2"].append(uid)
        save_json(RANKS_FILE, RANKS)
    
    text = """• أهلًا بك عزيزي أنا اسمي سورد

━━━━━━━━━━━━━━━
حرفيًا أفضل بوت!
━━━━━━━━━━━━━━━
🎖️ الرتب:
- Dev² 🎖️
- Dev 🎖️
- Myth 🎖️
- Myth
━━━━━━━━━━━━━━━
- مطوري ↫ راكان @ADJkex"""

    kb = [[InlineKeyboardButton("➕ اضفني لقروبك", url=f"https://t.me/{context.bot.username}?startgroup=true")],
          [InlineKeyboardButton("👨‍💻 راكان ADJkex", url="https://t.me/ADJkex")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    cid = str(update.effective_chat.id)
    uid = update.effective_user.id
    msg = update.message
    text = (msg.text or "").strip()
    
    stats = get_stats(cid)
    s_uid = str(uid)
    if s_uid not in stats:
        stats[s_uid] = {"count": 0, "first_seen": datetime.now().strftime("%Y/%m/%d"), "name": msg.from_user.first_name}
    stats[s_uid]["count"] += 1
    stats[s_uid]["name"] = msg.from_user.first_name
    save_json(STATS_FILE, STATS)
    
    if msg.photo or msg.video or msg.sticker or msg.animation:
        mlog = get_media_log(cid)
        mlog.append(msg.message_id)
        if len(mlog) > 500:
            mlog = mlog[-500:]
        MEDIA_LOG[cid] = mlog
        save_json(MEDIA_FILE, MEDIA_LOG)

    if msg.new_chat_members:
        for member in msg.new_chat_members:
            if member.is_bot and member.username != context.bot.username:
                try:
                    await context.bot.ban_chat_member(cid, member.id)
                    await msg.reply_text(f"🚫 تم طرد البوت {member.first_name}")
                except:
                    pass

    if text == "رتبتي":
        if msg.reply_to_message:
            target = msg.reply_to_message.from_user
            rank = get_rank_name(cid, target.id)
            await msg.reply_text(f"رتبته => {rank}")
        else:
            rank = get_rank_name(cid, uid)
            await msg.reply_text(f"رتبتك => {rank}")
        return

    if text == "الرتب":
        r = get_ranks(cid)
        await msg.reply_text(f"الرتب:\nDev² 🎖️ : {len(r['dev2'])}\nDev 🎖️ : {len(r['dev'])}\nMyth 🎖️ : {len(r['myth_badge'])}\nMyth : {len(r['myth'])}")
        return

    if text in ["توب", "توب المتفاعلين", "تفاعل"]:
        stats = get_stats(cid)
        sorted_users = sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
        txt = "🏆 توب المتفاعلين:\n\n"
        for i, (uid_key, data) in enumerate(sorted_users, 1):
            txt += f"{i}. {data['name']} - {data['count']} رسالة\n"
        await msg.reply_text(txt)
        return

    if text == "الالعاب":
        kb = [
            [InlineKeyboardButton("✊ حجر", callback_data="rps_rock"), InlineKeyboardButton("✋ ورقة", callback_data="rps_paper"), InlineKeyboardButton("✌️ مقص", callback_data="rps_scissors")],
            [InlineKeyboardButton("🎲 حظ", callback_data="luck")]
        ]
        await msg.reply_text("🎮 العاب سورد:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if text.startswith("اضف امر"):
        name = text.replace("اضف امر", "", 1).strip().lower()
        if not name or not msg.reply_to_message:
            await msg.reply_text("اكتب: اضف امر + الاسم بالرد")
            return
        content = msg.reply_to_message.text or msg.reply_to_message.caption or ""
        custom = get_custom(cid)
        custom[name] = content
        save_json(CUSTOM_FILE, CUSTOM)
        await msg.reply_text(f"تم اضافة امر {name}")
        return

    if text.startswith("حذف امر"):
        name = text.replace("حذف امر", "", 1).strip().lower()
        custom = get_custom(cid)
        if name in custom:
            del custom[name]
            save_json(CUSTOM_FILE, CUSTOM)
            await msg.reply_text(f"تم حذف امر {name}")
        return

    if text.startswith("تغير امر"):
        rest = text.replace("تغير امر", "", 1).strip()
        if " الى " in rest:
            old, new = rest.split(" الى ", 1)
            old = old.strip().lower()
            new = new.strip().lower()
            custom = get_custom(cid)
            if old in custom:
                custom[new] = custom[old]
                del custom[old]
                save_json(CUSTOM_FILE, CUSTOM)
                await msg.reply_text(f"تم تغير امر {old} الى {new}")
        return

    if text == "الاوامر":
        custom = get_custom(cid)
        txt = "الاوامر المضافة:\n"
        has = False
        for k in custom.keys():
            if not k.startswith("whisper_"):
                txt += f"- {k}\n"
                has = True
        if not has:
            txt += "لا يوجد"
        await msg.reply_text(txt)
        return

    if msg.reply_to_message and ("رفع" in text or "تنزيل" in text):
        r = get_ranks(cid)
        if ("ديف اساسي" in text or "Dev²" in text) and uid not in r["dev_asasi"] and uid not in r["dev2"] and msg.from_user.username != "ADJkex":
            await msg.reply_text("بس Dev² 🎖️ يقدر!")
            return
        rank_key = None
        if "Dev²" in text or "ديف 2" in text or "dev2" in text.lower():
            rank_key = "dev2"
        elif "Myth 🎖️" in text:
            rank_key = "myth_badge"
        elif "Myth" in text or "ميث" in text:
            rank_key = "myth"
        elif "Dev 🎖️" in text or "Dev" in text or "ديف" in text:
            rank_key = "dev"
        
        if rank_key:
            target = msg.reply_to_message.from_user
            tid = target.id
            tname = target.first_name
            if "رفع" in text:
                if tid not in r[rank_key]:
                    r[rank_key].append(tid)
                    save_json(RANKS_FILE, RANKS)
                    await msg.reply_text(f"تم رفع {tname} {rank_key}")
            else:
                if tid in r[rank_key]:
                    r[rank_key].remove(tid)
                    save_json(RANKS_FILE, RANKS)
                    await msg.reply_text(f"تم تنزيل {tname}")
            return

    if text.startswith("رفع مشرف") and msg.reply_to_message:
        if not await is_admin(update):
            return
        try:
            target_id = msg.reply_to_message.from_user.id
            await context.bot.promote_chat_member(cid, target_id, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False, can_manage_chat=True, can_manage_video_chats=True)
            await msg.reply_text(f"تم رفع {msg.reply_to_message.from_user.first_name} مشرف")
        except Exception as e:
            await msg.reply_text(f"خطأ: {e}")
        return

    if text.startswith("تنزيل مشرف") and msg.reply_to_message:
        if not await is_admin(update):
            return
        try:
            target_id = msg.reply_to_message.from_user.id
            await context.bot.promote_chat_member(cid, target_id, can_delete_messages=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False, can_manage_chat=False, is_anonymous=False)
            await msg.reply_text(f"تم تنزيل {msg.reply_to_message.from_user.first_name}")
        except Exception as e:
            await msg.reply_text(f"خطأ: {e}")
        return

    if text.startswith("كتم") and msg.reply_to_message:
        if not await is_admin(update):
            return
        try:
            target_id = msg.reply_to_message.from_user.id
            await context.bot.restrict_chat_member(cid, target_id, permissions=None, until_date=int(time.time()+3600))
            await msg.reply_text(f"تم كتم {msg.reply_to_message.from_user.first_name}")
        except:
            pass
        return

    if text.startswith("حظر") and msg.reply_to_message:
        if not await is_admin(update):
            return
        try:
            await context.bot.ban_chat_member(cid, msg.reply_to_message.from_user.id)
            await msg.reply_text(f"تم حظر {msg.reply_to_message.from_user.first_name}")
        except:
            pass
        return

    if text.startswith("تثبيت") and msg.reply_to_message:
        if not await is_admin(update):
            return
        try:
            await context.bot.pin_chat_message(cid, msg.reply_to_message.message_id)
            await msg.reply_text("تم التثبيت")
        except:
            pass
        return

    if text.startswith("الغاء التثبيت"):
        if not await is_admin(update):
            return
        try:
            if msg.reply_to_message:
                await context.bot.unpin_chat_message(cid, msg.reply_to_message.message_id)
            else:
                await context.bot.unpin_all_chat_messages(cid)
            await msg.reply_text("تم الغاء التثبيت")
        except:
            pass
        return

    if text == "مسح" and msg.reply_to_message:
        if not await is_admin(update):
            return
        try:
            await context.bot.delete_message(cid, msg.reply_to_message.message_id)
            await msg.delete()
        except:
            pass
        return

    if text == "تنظيف":
        if not await is_admin(update):
            return
        mlog = get_media_log(cid)
        deleted = 0
        for mid in mlog[-100:]:
            try:
                await context.bot.delete_message(cid, mid)
                deleted += 1
            except:
                pass
        MEDIA_LOG[cid] = []
        save_json(MEDIA_FILE, MEDIA_LOG)
        await msg.reply_text(f"تم تنظيف {deleted} رسالة")
        return

    if text.startswith("همسه"):
        if not msg.reply_to_message:
            await msg.reply_text("رد على شخص واكتب همسه")
            return
        whisper_text = text.replace("همسه", "", 1).strip()
        if not whisper_text:
            await msg.reply_text("اكتب همسه + الكلام")
            return
        target = msg.reply_to_message.from_user
        try:
            await msg.delete()
        except:
            pass
        kb = [[InlineKeyboardButton("👁️ عرض الهمسه", callback_data=f"whisper_{target.id}")]]
        custom = get_custom(cid)
        custom[f"whisper_{target.id}_{int(time.time())}"] = whisper_text
        save_json(CUSTOM_FILE, CUSTOM)
        await context.bot.send_message(cid, f"🔒 عندك همسه من {msg.from_user.first_name} الى {target.first_name}", reply_markup=InlineKeyboardMarkup(kb))
        return

    custom = get_custom(cid)
    if text.lower() in custom:
        await msg.reply_text(custom[text.lower()])
        return

    if await is_admin(update):
        return
    r = get_ranks(cid)
    if uid in r["dev_asasi"] or uid in r["dev"] or uid in r["dev2"] or uid in r["myth_badge"] or uid in r["myth"]:
        return

    low = text.lower()
    for bad in PORN_WORDS:
        if bad in low:
            try:
                await msg.delete()
                if msg.photo or msg.video:
                    await context.bot.ban_chat_member(cid, uid)
            except:
                pass
            return

    if any(x in low for x in ["http://","https://","t.me/","www."]):
        try:
            await msg.delete()
            return
        except:
            pass
    if msg.forward_from or msg.forward_from_chat:
        try:
            await msg.delete()
            return
        except:
            pass

    now = time.time()
    user_messages[uid].append(now)
    user_messages[uid] = [t for t in user_messages[uid] if now - t < 8]
    if len(user_messages[uid]) > 4:
        try:
            await update.effective_chat.restrict_chat_member(uid, permissions=None, until_date=int(now+300))
            user_messages[uid] = []
        except:
            pass

async def anti_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.edited_message:
        return
    if update.effective_chat.type == "private":
        return
    cid = str(update.effective_chat.id)
    r = get_ranks(cid)
    uid = update.edited_message.from_user.id if update.edited_message.from_user else None
    if uid and (uid in r["dev_asasi"] or uid in r["dev2"]):
        return
    try:
        await update.edited_message.delete()
        await context.bot.send_message(cid, f"تعدل مره ثانيه بلعن امك يا {update.edited_message.from_user.first_name} 😂")
    except:
        pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    cid = str(update.effective_chat.id)
    
    if data.startswith("whisper_"):
        target_id = int(data.split("_")[1])
        if query.from_user.id != target_id:
            await query.answer("مو لك الهمسه!", show_alert=True)
            return
        custom = get_custom(cid)
        for k, v in custom.items():
            if k.startswith(f"whisper_{target_id}"):
                await query.answer(v, show_alert=True)
                return
        await query.answer("الهمسه انحذفت", show_alert=True)
        return
    
    if data.startswith("rps_"):
        user_choice = data.replace("rps_", "")
        bot_choice = random.choice(["rock", "paper", "scissors"])
        names = {"rock": "حجر", "paper": "ورقة", "scissors": "مقص"}
        if user_choice == bot_choice:
            res = "تعادل!"
        elif (user_choice == "rock" and bot_choice == "scissors") or (user_choice == "paper" and bot_choice == "rock") or (user_choice == "scissors" and bot_choice == "paper"):
            res = "فزت!"
        else:
            res = "خسرت!"
        await query.edit_message_text(f"انت: {names[user_choice]} - البوت: {names[bot_choice]}\n{res}")
        return
    
    if data == "luck":
        luck = random.choice(["حظك اليوم ممتاز 🔥", "حظك متوسط 😐", "حظك سيء 😅"])
        await query.edit_message_text(luck)
        return

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing")
    threading.Thread(target=run_server, daemon=True).start()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except:
        pass
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all))
    app.add_handler(MessageHandler(filters.ALL & ~filters.UpdateType.EDITED_MESSAGE, handle_all))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, anti_edit))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("SORD Fixed running...")
    app.run_polling()
