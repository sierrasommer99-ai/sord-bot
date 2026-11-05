# -*- coding: utf-8 -*-
# تحكم بالاقفال من خاص البوت + قفل يمنع اللي رتبته اقل
# Token: 8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA
# ID: 829238313
# خاصك: https://t.me/afiwd

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - PRIVATE LOCK CONTROL", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, requests, re
from telebot.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity, User

BOT_TOKEN = "8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False, parse_mode=None)
OWNER_BOT_ID = 829238313

print(f"PRIVATE LOCK CONTROL - {OWNER_BOT_ID}")

try:
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
except:
    pass

FILE = 'custom_commands.json'
OWNER_FILE = 'owner_info.json'
LOCK_FILE = 'locked_commands.json'
RANKS_FILE = 'user_ranks.json'

custom = {}
try:
    with open(FILE,'r',encoding='utf-8') as f:
        custom = json.load(f)
except:
    custom = {}

owner_info = {}
try:
    with open(OWNER_FILE,'r',encoding='utf-8') as f:
        owner_info = json.load(f)
        owner_info['private'] = 'afiwd'
        owner_info['username'] = 'afiwd'
except:
    owner_info = {"name": "محسن", "username": "afiwd", "bio": "https://t.me/afiwd", "group": "- darkness", "private": "afiwd", "photo": None}

locked = {}
try:
    with open(LOCK_FILE,'r',encoding='utf-8') as f:
        locked = json.load(f)
except:
    locked = {}

user_ranks = {}
try:
    with open(RANKS_FILE,'r',encoding='utf-8') as f:
        user_ranks = json.load(f)
except:
    user_ranks = {}

def save_custom():
    with open(FILE,'w',encoding='utf-8') as f:
        json.dump(custom,f,ensure_ascii=False,indent=2)
def save_owner():
    with open(OWNER_FILE,'w',encoding='utf-8') as f:
        json.dump(owner_info,f,ensure_ascii=False,indent=2)
def save_locked():
    with open(LOCK_FILE,'w',encoding='utf-8') as f:
        json.dump(locked,f,ensure_ascii=False,indent=2)
def save_ranks():
    with open(RANKS_FILE,'w',encoding='utf-8') as f:
        json.dump(user_ranks,f,ensure_ascii=False,indent=2)

RANK_ORDER = {
    "مميز": 1,
    "ادمن": 2,
    "مدير": 3,
    "منشئ": 4,
    "منشئ اساسي": 5,
    "مالك": 6,
    "مالك اساسي": 7,
    "مالك المجموعه": 8,
    "M": 9,
    "MY": 10,
    "Dev2": 11,
    "Dev": 12
}

RANK_ALIASES = {
    "dev": "Dev",
    "dev2": "Dev2",
    "my": "MY",
    "m": "M",
    "مالك المجموعه": "مالك المجموعه",
    "مالك المجموعة": "مالك المجموعه",
    "مالك اساسي": "مالك اساسي",
    "منشئ اساسي": "منشئ اساسي",
    "منشئ": "منشئ",
    "مدير": "مدير",
    "ادمن": "ادمن",
    "مميز": "مميز"
}

def normalize_rank(text):
    text = text.strip()
    for key, val in RANK_ALIASES.items():
        if text.lower() == key.lower() or text == val:
            return val
    for rank in RANK_ORDER:
        if text in rank or rank in text:
            return rank
    return text

def get_user_rank_level(user_id, chat_id):
    if user_id == OWNER_BOT_ID:
        return 100
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str in user_ranks and user_id_str in user_ranks[chat_id_str]:
        rank_name = user_ranks[chat_id_str][user_id_str]
        return RANK_ORDER.get(rank_name, 0)
    return 0

def get_user_rank_name(user_id, chat_id):
    if user_id == OWNER_BOT_ID:
        return "Dev"
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str in user_ranks and user_id_str in user_ranks[chat_id_str]:
        return user_ranks[chat_id_str][user_id_str]
    return "عضو"

def can_use_command(user_id, chat_id, command):
    if command not in locked:
        return True
    required_rank = locked[command]
    required_level = RANK_ORDER.get(required_rank, 0)
    user_level = get_user_rank_level(user_id, chat_id)
    return user_level >= required_level

waiting = {}
pending = {}
edit_motawer = {}
waiting_rank = {}
waiting_rank_private = {}  # للخاص

def save_all_entities(message):
    result = []
    entities = message.entities or message.caption_entities or []
    for e in entities:
        ent = {"type": e.type, "offset": e.offset, "length": e.length}
        if getattr(e, 'url', None):
            ent["url"] = e.url
        if getattr(e, 'custom_emoji_id', None):
            ent["custom_emoji_id"] = e.custom_emoji_id
        if getattr(e, 'user', None) and e.user:
            ent["user"] = {"id": e.user.id, "first_name": e.user.first_name}
        if getattr(e, 'language', None):
            ent["language"] = e.language
        result.append(ent)
    return result

def restore_all_entities(entities_data):
    result = []
    for ent in entities_data:
        try:
            kwargs = {"type": ent["type"], "offset": ent["offset"], "length": ent["length"]}
            if "url" in ent:
                kwargs["url"] = ent["url"]
            if "custom_emoji_id" in ent:
                kwargs["custom_emoji_id"] = ent["custom_emoji_id"]
            if "user" in ent and ent["user"]:
                u = ent["user"]
                kwargs["user"] = User(u["id"], False, u.get("first_name",""))
            if "language" in ent:
                kwargs["language"] = ent["language"]
            result.append(MessageEntity(**kwargs))
        except:
            pass
    return result

def get_owner_button():
    url = f"https://t.me/afiwd"
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(f"💬 مراسلة {owner_info.get('name','محسن')} ²⁷", url=url))
    markup.add(InlineKeyboardButton(f"👤 دخول خاصي ↦", url=url))
    return markup

def get_motawer_text(real_group_name=None):
    group = real_group_name or owner_info.get('group','- darkness')
    return f"""Owner Group ↦ {group} ²⁷

USE ↦ {owner_info.get('name','محسن')} | {owner_info.get('username','afiwd')} ²⁷

Bio ↦ {owner_info.get('bio','https://t.me/afiwd')} ↦"""

def get_rank_list_text():
    return f"""≡ حسنًا عزيزي قم بإرسال الرتبة الان :
━━━━━━━━━━━━━━
- Dev
- Dev2
- MY
- M
- مالك المجموعه
- مالك اساسي
- مالك
- منشئ اساسي
- منشئ
- مدير
- ادمن
- مميز
━━━━━━━━━━━━━━
≡ سيتم وضع الأمر للرتبة المحددة
فقط"""

@bot.message_handler(chat_types=['private'], func=lambda m: m.from_user.id == OWNER_BOT_ID, content_types=['text','photo','video','document','sticker','voice','animation','audio','video_note'])
def private_lab(m):
    global owner_info
    uid = m.from_user.id
    text_content = (m.text or m.caption or "").strip()

    # ===== تحكم بالاقفال من الخاص - الميزة الجديدة =====
    
    # قفل امر من الخاص: قفل امر المطور Dev
    if text_content.startswith("قفل امر ") or text_content.startswith("قفل أمر "):
        cmd_text = text_content.replace("قفل امر ","").replace("قفل أمر ","").strip()
        # هل فيه رتبة مع الامر؟
        parts = cmd_text.split()
        if len(parts) >= 2:
            possible_rank = normalize_rank(parts[-1])
            if possible_rank in RANK_ORDER:
                command_name = " ".join(parts[:-1]).strip()
                locked[command_name] = possible_rank
                save_locked()
                bot.reply_to(m, f"🔒 تم قفل امر {command_name} من الخاص ✅\n≡ لرتبة ↤ {possible_rank} 🎖️\n≡ فقط Dev واللي فوقه يقدر يشوفه\n\nاي حد رتبته اقل من {possible_rank} ما يقدر يستخدم {command_name} ❌")
                return
        
        # بدون رتبة - اسأل عن الرتبة في الخاص
        waiting_rank_private[uid] = {"command": cmd_text}
        bot.reply_to(m, f"""🔒 قفل امر {cmd_text} من الخاص

{get_rank_list_text()}

ارسل الرتبة الحين:
مثال: Dev

الامر {cmd_text} بيصير فقط لرتبة Dev وفوق
اي حد اقل من Dev ما يشوفه ❌""")
        return

    # انتظار رتبة في الخاص
    if uid in waiting_rank_private:
        rank = normalize_rank(text_content)
        if rank in RANK_ORDER:
            command = waiting_rank_private[uid]["command"]
            locked[command] = rank
            save_locked()
            del waiting_rank_private[uid]
            bot.reply_to(m, f"✅ تم قفل امر {command} من الخاص 🔒\n≡ لرتبة ↤ {rank} 🎖️\n≡ فقط\n\nالحين:\n• Dev يقدر يشوف {command} ✅\n• اي رتبة اقل من {rank} ما يقدر يشوفه ❌\n• التحكم كله من خاص البوت ✅")
            return

    # فتح امر من الخاص
    if text_content.startswith("فتح امر ") or text_content.startswith("فتح أمر "):
        cmd = text_content.replace("فتح امر ","").replace("فتح أمر ","").strip()
        if cmd in locked:
            del locked[cmd]
            save_locked()
            bot.reply_to(m, f"✅ تم فتح امر {cmd} من الخاص 🔓\nالكل يقدر يشوفه ويستخدمه الحين")
        else:
            bot.reply_to(m, f"❌ امر {cmd} مو مقفول اصلا")
        return

    # قائمة الاقفال من الخاص
    if text_content in ["قائمة الاقفال","قائمه الاقفال","الاقفال","الاوامر المقفولة","اقفالي"]:
        if not locked:
            bot.reply_to(m, "🔓 ما فيه اوامر مقفولة\nكل الاوامر مفتوحة للكل")
            return
        txt = "🔒 الاوامر المقفولة (تحكم من الخاص):\n━━━━━━━━━━━━━━\n"
        for cmd, rank in locked.items():
            txt += f"• {cmd} ↤ {rank}\n"
        txt += "━━━━━━━━━━━━━━\n"
        txt += "• Dev وفوق يقدر يشوفها ✅\n"
        txt += "• اقل من الرتبة ما يشوفها ❌\n"
        txt += "━━━━━━━━━━━━━━\n"
        txt += "لفتح: فتح امر المطور\n"
        txt += "لقفل: قفل امر المطور Dev"
        bot.reply_to(m, txt)
        return

    # فتح كل الاقفال
    if text_content in ["فتح الكل","فتح جميع الاقفال","مسح الاقفال"]:
        locked.clear()
        save_locked()
        bot.reply_to(m, "✅ تم فتح كل الاقفال 🔓\nكل الاوامر مفتوحة للكل الحين")
        return

    # تعديل معلومات المطور
    if text_content in ["عدل معلومات المطور","تعديل المطور","عدل المطور"]:
        edit_motawer[uid] = {"step": "name", "data": dict(owner_info)}
        bot.reply_to(m, f"✏️ تعديل المطور ²⁷\nالاسم الحالي: {owner_info.get('name')}\nارسل الاسم الجديد او تخطي:")
        return

    if uid in edit_motawer:
        step = edit_motawer[uid]["step"]
        data = edit_motawer[uid]["data"]
        if text_content.lower() not in ["تخطي","skip"]:
            if step == "name" and m.content_type == 'text':
                data["name"] = text_content
            elif step == "bio" and m.content_type == 'text':
                data["bio"] = text_content
            elif step == "photo" and m.content_type == 'photo':
                data["photo"] = m.photo[-1].file_id
        
        if step == "name":
            edit_motawer[uid]["step"] = "bio"
            bot.reply_to(m, f"✅ الاسم: {data['name']}\nالحين البايو (او تخطي):")
            return
        elif step == "bio":
            edit_motawer[uid]["step"] = "photo"
            bot.reply_to(m, f"✅ البايو: {data['bio']}\nالحين صورة المطور (او تم):")
            return
        elif step == "photo":
            owner_info = data
            owner_info["private"] = "afiwd"
            owner_info["username"] = "afiwd"
            save_owner()
            del edit_motawer[uid]
            markup = get_owner_button()
            text_preview = get_motawer_text()
            if owner_info.get("photo"):
                bot.send_photo(m.chat.id, owner_info["photo"], caption=text_preview, reply_markup=markup)
            else:
                bot.reply_to(m, f"✅ تم ✅\n{text_preview}", reply_markup=markup)
            return

    if text_content.startswith("احفظ معلوماتي"):
        parts = text_content.replace("احفظ معلوماتي","").replace(":","").strip()
        if parts:
            segs = re.split(r'\||،|,', parts)
            if segs[0].strip():
                owner_info["name"] = segs[0].strip()
        owner_info["private"] = "afiwd"
        owner_info["username"] = "afiwd"
        save_owner()
        markup = get_owner_button()
        bot.reply_to(m, f"✅ حفظت\n{owner_info['name']} @afiwd", reply_markup=markup)
        return

    if m.content_type == 'photo' and "صورة المطور" in (m.caption or ""):
        owner_info["photo"] = m.photo[-1].file_id
        save_owner()
        markup = get_owner_button()
        bot.send_photo(m.chat.id, owner_info["photo"], caption=get_motawer_text(), reply_markup=markup)
        return

    if text_content.startswith("ضع صورة المطور"):
        bot.reply_to(m, "📸 ارسل صورة المطور الحين:")
        waiting[uid] = {"step": "wait_photo_motawer", "command": "صورة المطور"}
        return

    if uid in waiting and waiting[uid].get("step") == "wait_photo_motawer":
        if m.content_type == 'photo':
            owner_info["photo"] = m.photo[-1].file_id
            save_owner()
            del waiting[uid]
            markup = get_owner_button()
            bot.send_photo(m.chat.id, owner_info["photo"], caption=get_motawer_text(), reply_markup=markup)
            bot.send_message(m.chat.id, "✅ حفظت الصورة + الزر اسفل ²⁷")
        return

    if uid in waiting and waiting[uid]['step'] == 'wait_reply':
        cmd = waiting[uid]['command']
        ctype = m.content_type
        if ctype == 'text':
            data = {"type": "text", "text": m.text, "entities": save_all_entities(m), "file_id": None, "caption": "", "caption_entities": []}
        elif ctype == 'photo':
            data = {"type": "photo", "text": "", "entities": [], "file_id": m.photo[-1].file_id, "caption": m.caption or "", "caption_entities": save_all_entities(m)}
        elif ctype == 'sticker':
            data = {"type": "sticker", "text": "", "entities": [], "file_id": m.sticker.file_id, "caption": "", "caption_entities": []}
        else:
            data = {"type": ctype, "text": m.text or m.caption or "", "entities": save_all_entities(m), "file_id": getattr(getattr(m, ctype, None), 'file_id', None), "caption": m.caption or "", "caption_entities": save_all_entities(m)}
        pending[uid] = {"t": cmd, "data": data}
        del waiting[uid]
        bot.reply_to(m, f"تمام ✅\nالأمر: {cmd}\nاكتب: ارفعه")
        return

    if text_content.startswith("اضف امر"):
        tmp = text_content.replace("اضف امر:", "").replace("اضف امر", "").strip()
        if "->" in tmp:
            a,b = tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                data = {"type": "text", "text": resp, "entities": save_all_entities(m), "file_id": None, "caption": "", "caption_entities": []}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m, f"تمام ✅\n{trig} ↦ {resp}\nاكتب: ارفعه")
                return
        else:
            cmd = tmp
            if not cmd:
                return
            waiting[uid] = {"step": "wait_reply", "command": cmd}
            bot.reply_to(m, f"تمام - الأمر: {cmd} ²⁷\nارسل الرد:")
            return

    if text_content in ["ارفعه","احفظه","ارفعه للسيرفر"]:
        if uid not in pending:
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ حفظت\n{t}")
        return

    if text_content in ["الغاء","الغه"]:
        waiting.pop(uid,None); pending.pop(uid,None); edit_motawer.pop(uid,None); waiting_rank_private.pop(uid,None)
        bot.reply_to(m, "❌ الغاء")
        return

    if text_content in ["/start","start"]:
        markup = get_owner_button()
        bot.reply_to(m, f"""اهلا - {uid} ✅
خاصك: https://t.me/afiwd

🔒 التحكم بالاقفال من الخاص (جديد):

قفل امر المطور Dev
→ يقفل المطور لـ Dev بس
→ اي رتبة اقل ما تشوفه ❌

قفل امر كتم MY
→ كتم لـ MY وفوق بس

فتح امر المطور
→ يفتح المطور للكل

قائمة الاقفال
→ تشوف كل الاقفال

فتح الكل
→ يفتح كل الاقفال

━━━━━━━━━━━━━━

اوامر المطور:
عدل معلومات المطور
ضع صورة المطور
احفظ معلوماتي: محسن

━━━━━━━━━━━━━━

رتب:
Dev - Dev2 - MY - M - مالك المجموعه - مالك اساسي - مالك - منشئ اساسي - منشئ - مدير - ادمن - مميز
""", reply_markup=markup)
        return

@bot.message_handler(content_types=['text'])
def groups(m):
    if m.chat.type == 'private':
        return
    text = (m.text or "").strip()
    chat_id = m.chat.id
    chat_title = m.chat.title or "القروب"
    user_id = m.from_user.id

    # قفل امر من القروب ايضا
    if text.startswith("قفل امر ") or text.startswith("قفل أمر "):
        if user_id != OWNER_BOT_ID and get_user_rank_level(user_id, chat_id) < RANK_ORDER.get("Dev",12):
            bot.reply_to(m, "❌ فقط Dev يقدر يقفل")
            return
        cmd_text = text.replace("قفل امر ","").replace("قفل أمر ","").strip()
        parts = cmd_text.split()
        if len(parts) >= 2:
            possible_rank = normalize_rank(parts[-1])
            if possible_rank in RANK_ORDER:
                command_name = " ".join(parts[:-1]).strip()
                locked[command_name] = possible_rank
                save_locked()
                bot.reply_to(m, f"≡ تم وضع امر ↤ {command_name}\n≡ لرتبة ↤ {possible_rank} 🎖️\n≡ فقط")
                return
        waiting_rank[chat_id] = {"command": cmd_text, "user": user_id}
        bot.reply_to(m, f"""≡ حسنًا عزيزي قم بإرسال الرتبة الان :
━━━━━━━━━━━━━━
- Dev
- Dev2
- MY
- M
- مالك المجموعه
- مالك اساسي
- مالك
- منشئ اساسي
- منشئ
- مدير
- ادمن
- مميز
━━━━━━━━━━━━━━
≡ سيتم وضع الأمر ↤ {cmd_text} للرتبة المحددة
فقط""")
        return

    if chat_id in waiting_rank and waiting_rank[chat_id]["user"] == user_id:
        rank = normalize_rank(text)
        if rank in RANK_ORDER:
            command = waiting_rank[chat_id]["command"]
            locked[command] = rank
            save_locked()
            del waiting_rank[chat_id]
            bot.reply_to(m, f"≡ تم وضع امر ↤ {command}\n≡ لرتبة ↤ {rank} 🎖️\n≡ فقط\n\n• {rank} وفوق يشوفه ✅\n• اقل من {rank} ما يشوفه ❌")
            return

    if text.startswith("فتح امر ") or text.startswith("فتح أمر "):
        cmd = text.replace("فتح امر ","").replace("فتح أمر ","").strip()
        if cmd in locked:
            del locked[cmd]
            save_locked()
            bot.reply_to(m, f"✅ تم فتح امر {cmd} 🔓\nالكل يقدر يشوفه الحين")
        else:
            bot.reply_to(m, f"❌ امر {cmd} مو مقفول")
        return

    if text in ["قائمة الاقفال","قائمه الاقفال","الاقفال"]:
        if not locked:
            bot.reply_to(m, "🔓 ما فيه اوامر مقفولة")
            return
        txt = "🔒 الاوامر المقفولة:\n━━━━━━━━━━━━━━\n"
        for cmd, rank in locked.items():
            txt += f"• {cmd} ↤ {rank}\n"
        txt += "━━━━━━━━━━━━━━\nاقل من الرتبة ما يشوفها ❌"
        bot.reply_to(m, txt)
        return

    if text.startswith("رفع ") and m.reply_to_message:
        rank_name = normalize_rank(text.replace("رفع ","").strip())
        if rank_name in RANK_ORDER:
            target_id = m.reply_to_message.from_user.id
            target_name = m.reply_to_message.from_user.first_name or "الشخص"
            if get_user_rank_level(user_id, chat_id) <= RANK_ORDER.get(rank_name,0) and user_id != OWNER_BOT_ID:
                bot.reply_to(m, f"❌ ما تقدر ترفع {rank_name}")
                return
            chat_id_str = str(chat_id)
            user_id_str = str(target_id)
            if chat_id_str not in user_ranks:
                user_ranks[chat_id_str] = {}
            user_ranks[chat_id_str][user_id_str] = rank_name
            save_ranks()
            mention = f"<a href='tg://user?id={target_id}'>{target_name}</a>"
            bot.send_message(chat_id, f"✅ تم رفع {mention}\nإلى {rank_name} ²⁷", parse_mode="HTML", reply_to_message_id=m.message_id)
            return

    if text.startswith("تنزيل ") and m.reply_to_message:
        rank_name = normalize_rank(text.replace("تنزيل ","").strip())
        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name or "الشخص"
        chat_id_str = str(chat_id)
        user_id_str = str(target_id)
        if chat_id_str in user_ranks and user_id_str in user_ranks[chat_id_str]:
            del user_ranks[chat_id_str][user_id_str]
            save_ranks()
            mention = f"<a href='tg://user?id={target_id}'>{target_name}</a>"
            bot.send_message(chat_id, f"✅ تم تنزيل {mention}", parse_mode="HTML", reply_to_message_id=m.message_id)
            return

    if text in ["رتبتي","رتبتي ²⁷"]:
        rank = get_user_rank_name(user_id, chat_id)
        bot.reply_to(m, f"رتبتك: {rank} ²⁷")
        return

    if text.startswith("ضع اسم القروب") or text.startswith("ضع اسم"):
        if user_id != OWNER_BOT_ID:
            bot.reply_to(m, "❌ فقط المالك")
            return
        new_name = text.replace("ضع اسم القروب:","").replace("ضع اسم القروب","").replace("ضع اسم:","").replace("ضع اسم","").strip()
        if not new_name:
            return
        try:
            bot.set_chat_title(chat_id, new_name)
            owner_info["group"] = new_name
            save_owner()
            bot.reply_to(m, f"✅ تم تغيير اسم القروب:\n{new_name}")
        except Exception as e:
            bot.reply_to(m, f"❌ ما قدرت\n{e}")
        return

    # تقييد مع تشييك القفل - يمنع اللي رتبته اقل
    if text in ["تقييد","تقييدد","قيد","كتم","كتمم"]:
        # تشييك القفل
        if not can_use_command(user_id, chat_id, "كتم") and not can_use_command(user_id, chat_id, text):
            required = locked.get("كتم") or locked.get(text) or "مميز"
            bot.reply_to(m, f"❌ امر {text} مقفول لرتبة {required} فقط\nرتبتك اقل ما تقدر تشوفه")
            return
        
        if not m.reply_to_message:
            bot.reply_to(m, "❌ رد على الشخص")
            return
        target = m.reply_to_message.from_user
        target_id = target.id
        target_name = target.first_name or "الشخص"
        if target_id == bot.get_me().id:
            return
        if get_user_rank_level(target_id, chat_id) >= get_user_rank_level(user_id, chat_id) and user_id != OWNER_BOT_ID:
            bot.reply_to(m, f"❌ ما تقدر تقيد {target_name} - رتبته اعلى")
            return
        try:
            bot.restrict_chat_member(chat_id=chat_id, user_id=target_id, permissions=ChatPermissions(can_send_messages=False))
            mention_text = f"• المستخدم ذا <a href='tg://user?id={target_id}'>{target_name}</a> قيده ²⁷ 🔒"
            bot.send_message(chat_id, mention_text, parse_mode="HTML", reply_to_message_id=m.message_id)
        except Exception as e:
            bot.reply_to(m, f"ما قدرت اقيده\n{e}")
        return

    if text in ["فك التقييد","فك تقييد","فك كتم"]:
        if not can_use_command(user_id, chat_id, "كتم"):
            required = locked.get("كتم") or "مميز"
            bot.reply_to(m, f"❌ امر فك التقييد مقفول لرتبة {required} فقط")
            return
        if not m.reply_to_message:
            return
        target = m.reply_to_message.from_user
        target_id = target.id
        target_name = target.first_name or "الشخص"
        try:
            bot.restrict_chat_member(chat_id=chat_id, user_id=target_id, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            mention_text = f"• المستخدم ذا <a href='tg://user?id={target_id}'>{target_name}</a> فكينا قيده ✅ ²⁷"
            bot.send_message(chat_id, mention_text, parse_mode="HTML", reply_to_message_id=m.message_id)
        except:
            pass
        return

    # المطور مع تشييك القفل
    if text in ["المطور","المطورر","المطور ²⁷","مطور"]:
        if not can_use_command(user_id, chat_id, "المطور"):
            required = locked.get("المطور") or "Dev"
            bot.reply_to(m, f"❌ امر المطور مقفول لرتبة {required} فقط\nرتبتك: {get_user_rank_name(user_id, chat_id)} - ما تقدر تشوفه")
            return
        
        real_group_name = chat_title
        markup = get_owner_button()
        text_out = get_motawer_text(real_group_name)
        
        if owner_info.get("photo"):
            try:
                bot.send_photo(chat_id, owner_info["photo"], caption=text_out, reply_markup=markup, reply_to_message_id=m.message_id)
                return
            except:
                pass
        
        if "المطور" in custom:
            data = custom["المطور"]
            if data.get("type") == "photo":
                try:
                    bot.send_photo(chat_id, data["file_id"], caption=text_out, reply_markup=markup, reply_to_message_id=m.message_id)
                except:
                    bot.send_message(chat_id, text_out, reply_markup=markup, reply_to_message_id=m.message_id)
                return
        
        bot.send_message(chat_id, text_out, reply_markup=markup, reply_to_message_id=m.message_id)
        return

    if text in custom:
        if text in ["تقييد","المطور","كتم"]:
            return
        if not can_use_command(user_id, chat_id, text):
            required = locked.get(text) or "مميز"
            bot.reply_to(m, f"❌ امر {text} مقفول لرتبة {required} فقط")
            return
        data = custom[text]
        if isinstance(data, dict):
            try:
                ctype = data.get("type","text")
                if ctype == "text":
                    ents = restore_all_entities(data.get("entities",[]))
                    if ents:
                        bot.send_message(chat_id, data.get("text",""), entities=ents, reply_to_message_id=m.message_id)
                    else:
                        bot.reply_to(m, data.get("text",""))
                elif ctype == "photo":
                    ents = restore_all_entities(data.get("caption_entities",[]))
                    if ents:
                        bot.send_photo(chat_id, data["file_id"], caption=data.get("caption",""), caption_entities=ents, reply_to_message_id=m.message_id)
                    else:
                        bot.send_photo(chat_id, data["file_id"], caption=data.get("caption",""), reply_to_message_id=m.message_id)
                elif ctype == "sticker":
                    bot.send_sticker(chat_id, data["file_id"], reply_to_message_id=m.message_id)
                elif ctype == "animation":
                    bot.send_animation(chat_id, data["file_id"], caption=data.get("caption",""), reply_to_message_id=m.message_id)
                elif ctype == "video":
                    bot.send_video(chat_id, data["file_id"], caption=data.get("caption",""), reply_to_message_id=m.message_id)
            except:
                bot.reply_to(m, data.get("text","") or data.get("caption",""))
        else:
            bot.reply_to(m, str(data))

print("READY - PRIVATE LOCK CONTROL + AFIWD + MENTION")

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True, none_stop=True)
    except Exception as e:
        err=str(e)
        if "409" in err or "Conflict" in err:
            time.sleep(10)
            try:
                bot.remove_webhook()
                requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
            except:
                pass
            time.sleep(5)
        else:
            print(f"❌ {e}")
            time.sleep(5)
