# -*- coding: utf-8 -*-
# يحدث كل الاوامر تلقائيا - كل شي اوتو
# Token: 8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA
# ID: 829238313
# خاصك: https://t.me/afiwd

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - AUTO UPDATE ALL", 200
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

print(f"AUTO UPDATE ALL - {OWNER_BOT_ID}")

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
TOP_FILE = 'top.json'

# تحميل اولي
def load_all():
    global custom, owner_info, locked, user_ranks, top_data
    try:
        with open(FILE,'r',encoding='utf-8') as f:
            custom = json.load(f)
    except:
        custom = {}
    try:
        with open(OWNER_FILE,'r',encoding='utf-8') as f:
            owner_info = json.load(f)
            owner_info['private'] = 'afiwd'
            owner_info['username'] = 'afiwd'
    except:
        owner_info = {"name": "محسن", "username": "afiwd", "bio": "https://t.me/afiwd", "group": "- darkness", "private": "afiwd", "photo": None}
    try:
        with open(LOCK_FILE,'r',encoding='utf-8') as f:
            locked = json.load(f)
    except:
        locked = {}
    try:
        with open(RANKS_FILE,'r',encoding='utf-8') as f:
            user_ranks = json.load(f)
    except:
        user_ranks = {}
    try:
        with open(TOP_FILE,'r',encoding='utf-8') as f:
            top_data = json.load(f)
    except:
        top_data = {}

custom = {}
owner_info = {}
locked = {}
user_ranks = {}
top_data = {}
load_all()

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
def save_top():
    with open(TOP_FILE,'w',encoding='utf-8') as f:
        json.dump(top_data,f,ensure_ascii=False,indent=2)

# ثريد يحدث كل الملفات تلقائيا كل 15 ثانية
def auto_reload_thread():
    while True:
        try:
            time.sleep(15)
            # اعادة تحميل بدون مسح
            try:
                with open(FILE,'r',encoding='utf-8') as f:
                    new_custom = json.load(f)
                    custom.clear()
                    custom.update(new_custom)
            except:
                pass
            try:
                with open(RANKS_FILE,'r',encoding='utf-8') as f:
                    new_ranks = json.load(f)
                    user_ranks.clear()
                    user_ranks.update(new_ranks)
            except:
                pass
            try:
                with open(LOCK_FILE,'r',encoding='utf-8') as f:
                    new_locked = json.load(f)
                    locked.clear()
                    locked.update(new_locked)
            except:
                pass
            try:
                with open(TOP_FILE,'r',encoding='utf-8') as f:
                    new_top = json.load(f)
                    top_data.clear()
                    top_data.update(new_top)
            except:
                pass
            try:
                with open(OWNER_FILE,'r',encoding='utf-8') as f:
                    new_owner = json.load(f)
                    owner_info.clear()
                    owner_info.update(new_owner)
                    owner_info['private'] = 'afiwd'
                    owner_info['username'] = 'afiwd'
            except:
                pass
            # print("🔄 auto reload done")
        except Exception as e:
            print(f"auto reload error: {e}")

threading.Thread(target=auto_reload_thread, daemon=True).start()

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

def normalize_rank(text):
    text = text.strip()
    aliases = {
        "dev": "Dev", "dev2": "Dev2", "my": "MY", "m": "M",
        "مالك المجموعة": "مالك المجموعه", "مالك المجموعه": "مالك المجموعه",
        "مالك اساسي": "مالك اساسي", "منشئ اساسي": "منشئ اساسي",
        "منشئ": "منشئ", "مدير": "مدير", "ادمن": "ادمن", "مميز": "مميز"
    }
    low = text.lower()
    if low in aliases:
        return aliases[low]
    for rank in RANK_ORDER:
        if text == rank or text in rank or rank in text:
            return rank
    return text

def get_user_rank_level(user_id, chat_id):
    if user_id == OWNER_BOT_ID:
        return 100
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str in user_ranks and user_id_str in user_ranks[chat_id_str]:
        return RANK_ORDER.get(user_ranks[chat_id_str][user_id_str], 0)
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
    required_level = RANK_ORDER.get(locked[command], 0)
    return get_user_rank_level(user_id, chat_id) >= required_level

def add_message_count(chat_id, user_id, first_name):
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str not in top_data:
        top_data[chat_id_str] = {}
    if user_id_str not in top_data[chat_id_str]:
        top_data[chat_id_str][user_id_str] = {"count": 0, "name": first_name}
    top_data[chat_id_str][user_id_str]["count"] += 1
    top_data[chat_id_str][user_id_str]["name"] = first_name
    # حفظ فوري - تحديث تلقائي
    try:
        save_top()
    except:
        pass

def get_user_stats(chat_id, user_id):
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str not in top_data:
        return 0, 0
    sorted_users = sorted(top_data[chat_id_str].items(), key=lambda x: x[1]["count"], reverse=True)
    count = top_data[chat_id_str].get(user_id_str, {}).get("count", 0)
    rank_pos = 0
    for idx, (uid, data) in enumerate(sorted_users, 1):
        if uid == user_id_str:
            rank_pos = idx
            break
    if rank_pos == 0:
        rank_pos = len(sorted_users) + 1 if count == 0 else len(sorted_users) + 1
        if count > 0 and rank_pos == 1 and len(sorted_users) == 0:
            rank_pos = 1
    return count, rank_pos if rank_pos != 0 else 1

waiting = {}
pending = {}
edit_motawer = {}
waiting_rank = {}
waiting_rank_private = {}

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

    # تحديث تلقائي قبل كل امر
    try:
        load_all()
    except:
        pass

    if text_content.startswith("قفل امر ") or text_content.startswith("قفل أمر "):
        cmd_text = text_content.replace("قفل امر ","").replace("قفل أمر ","").strip()
        parts = cmd_text.split()
        if len(parts) >= 2:
            possible_rank = normalize_rank(parts[-1])
            if possible_rank in RANK_ORDER:
                command_name = " ".join(parts[:-1]).strip()
                locked[command_name] = possible_rank
                save_locked()
                bot.reply_to(m, f"🔒 تم قفل {command_name} لـ {possible_rank}\n✅ تحديث تلقائي للكل")
                return
        waiting_rank_private[uid] = {"command": cmd_text}
        bot.reply_to(m, f"🔒 قفل {cmd_text}\n{get_rank_list_text()}")
        return

    if uid in waiting_rank_private:
        rank = normalize_rank(text_content)
        if rank in RANK_ORDER:
            command = waiting_rank_private[uid]["command"]
            locked[command] = rank
            save_locked()
            del waiting_rank_private[uid]
            bot.reply_to(m, f"✅ تم قفل {command} لـ {rank}\n🔄 تحديث تلقائي للكل")
            return

    if text_content.startswith("فتح امر ") or text_content.startswith("فتح أمر "):
        cmd = text_content.replace("فتح امر ","").replace("فتح أمر ","").strip()
        if cmd in locked:
            del locked[cmd]
            save_locked()
            bot.reply_to(m, f"✅ فتح {cmd}\n🔄 تحديث تلقائي")
        else:
            bot.reply_to(m, f"❌ {cmd} مو مقفول")
        return

    if text_content in ["قائمة الاقفال","قائمه الاقفال","الاقفال","تحديث الاوامر","تحديث"]:
        # يحدث كل شي
        load_all()
        txt = "🔄 تم تحديث كل الاوامر تلقائيا ✅\n"
        txt += f"━━━━━━━━━━━━━━\n"
        txt += f"• اوامر مخصصة: {len(custom)}\n"
        txt += f"• رتب: {sum(len(v) for v in user_ranks.values())}\n"
        txt += f"• اقفال: {len(locked)}\n"
        txt += f"• متفاعلين: {sum(len(v) for v in top_data.values())}\n"
        txt += f"━━━━━━━━━━━━━━\n"
        if locked:
            txt += "🔒 الاقفال:\n"
            for cmd, rank in locked.items():
                txt += f"• {cmd} ↤ {rank}\n"
        else:
            txt += "🔓 ما فيه اقفال\n"
        bot.reply_to(m, txt)
        return

    if text_content in ["فتح الكل"]:
        locked.clear()
        save_locked()
        bot.reply_to(m, "✅ فتح الكل - تحديث تلقائي")
        return

    if text_content in ["عدل معلومات المطور","تعديل المطور","عدل المطور"]:
        edit_motawer[uid] = {"step": "name", "data": dict(owner_info)}
        bot.reply_to(m, f"✏️ الاسم: {owner_info.get('name')}\nارسل الجديد:")
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
            bot.reply_to(m, f"✅ الاسم: {data['name']}\nالبايو:")
            return
        elif step == "bio":
            edit_motawer[uid]["step"] = "photo"
            bot.reply_to(m, f"✅ البايو: {data['bio']}\nالصورة:")
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
                bot.reply_to(m, f"✅ تم\n{text_preview}", reply_markup=markup)
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
        bot.reply_to(m, f"✅ حفظت {owner_info['name']} - تحديث تلقائي", reply_markup=markup)
        return

    if text_content.startswith("ضع صورة المطور"):
        bot.reply_to(m, "📸 ارسل صورة:")
        waiting[uid] = {"step": "wait_photo_motawer"}
        return

    if uid in waiting and waiting[uid].get("step") == "wait_photo_motawer":
        if m.content_type == 'photo':
            owner_info["photo"] = m.photo[-1].file_id
            save_owner()
            del waiting[uid]
            markup = get_owner_button()
            bot.send_photo(m.chat.id, owner_info["photo"], caption=get_motawer_text(), reply_markup=markup)
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
        bot.reply_to(m, f"تمام ✅ {cmd}\nاكتب: ارفعه - بيتحدث تلقائي للكل")
        return

    if text_content.startswith("اضف امر"):
        tmp = text_content.replace("اضف امر:", "").replace("اضف امر", "").strip()
        if "->" in tmp:
            a,b = tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                data = {"type": "text", "text": resp, "entities": save_all_entities(m), "file_id": None, "caption": "", "caption_entities": []}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m, f"تمام ✅ {trig} ↦ {resp}\nارفعه")
                return
        else:
            cmd = tmp
            if not cmd:
                return
            waiting[uid] = {"step": "wait_reply", "command": cmd}
            bot.reply_to(m, f"تمام - الأمر: {cmd}\nارسل الرد:")
            return

    if text_content in ["ارفعه","احفظه","ارفعه للسيرفر"]:
        if uid not in pending:
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ حفظت {t}\n🔄 تحديث تلقائي للكل - الكل يقدر يستخدمه الحين")
        return

    if text_content in ["الغاء","الغه"]:
        waiting.pop(uid,None); pending.pop(uid,None); edit_motawer.pop(uid,None); waiting_rank_private.pop(uid,None)
        bot.reply_to(m, "❌ الغاء")
        return

    if text_content in ["/start","start"]:
        load_all()
        markup = get_owner_button()
        bot.reply_to(m, f"""اهلا {uid} ✅
خاصك: https://t.me/afiwd

🔄 التحديث التلقائي شغال:
• كل رسالة تتحدث
• كل رفع يتحدث
• كل امر يتحدث

اوامر:
قفل امر المطور Dev → قفل + تحديث تلقائي
فتح امر المطور → فتح + تحديث تلقائي
تحديث الاوامر → يحدث كل شي

الاحصائيات:
• اوامر: {len(custom)}
• رتب: {sum(len(v) for v in user_ranks.values())}
• اقفال: {len(locked)}
""", reply_markup=markup)
        return

@bot.message_handler(content_types=['text','photo','sticker','animation','video','voice','document'])
def groups(m):
    if m.chat.type == 'private':
        return
    
    text = (m.text or m.caption or "").strip()
    chat_id = m.chat.id
    chat_title = m.chat.title or "القروب"
    user_id = m.from_user.id
    first_name = m.from_user.first_name or "شخص"

    # ===== تحديث تلقائي لكل رسالة =====
    try:
        add_message_count(chat_id, user_id, first_name)
        # يحدث الرتب تلقائيا كل رسالة - بدون ما تحتاج امر
    except:
        pass

    # ===== رفع رتبة - يحدث كل الاوامر تلقائيا =====
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
            
            # تحديث فوري + تلقائي لكل الاوامر
            user_ranks[chat_id_str][user_id_str] = rank_name
            save_ranks()
            
            # يحدث top كمان
            if chat_id_str not in top_data:
                top_data[chat_id_str] = {}
            if user_id_str not in top_data[chat_id_str]:
                top_data[chat_id_str][user_id_str] = {"count": 1, "name": target_name}
            save_top()
            
            count, pos = get_user_stats(chat_id, target_id)
            
            # سكرين يحدث تلقائيا
            text_reply = f"""🎖️ {rank_name} ← تم رفع {target_name} إلى

≡ رتبته هي ← {rank_name} 🎖️
≡ رسائله بالتفاعل ← {count}
≡ ترتيبه بالمتفاعلين ← {pos}
-
🔄 تحديث تلقائي لكل الاوامر ✅ ²⁷"""
            bot.send_message(chat_id, text_reply, parse_mode="HTML", reply_to_message_id=m.message_id)
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
            bot.send_message(chat_id, f"✅ تم تنزيل {target_name} من {rank_name}\n🔄 تحديث تلقائي لكل الاوامر ✅", reply_to_message_id=m.message_id)
            return

    if text in ["تنزيل الكل"] and m.reply_to_message:
        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name or "الشخص"
        chat_id_str = str(chat_id)
        user_id_str = str(target_id)
        if chat_id_str in user_ranks and user_id_str in user_ranks[chat_id_str]:
            del user_ranks[chat_id_str][user_id_str]
            save_ranks()
            bot.send_message(chat_id, f"✅ تم تنزيل {target_name} من كل الرتب\n🔄 تحديث تلقائي", parse_mode="HTML", reply_to_message_id=m.message_id)
        return

    # ===== رتبتي - يحدث تلقائيا =====
    if text in ["رتبتي","رتبتي ²⁷","رتبتي 27"]:
        rank = get_user_rank_name(user_id, chat_id)
        count, pos = get_user_stats(chat_id, user_id)
        reply_text = f"""🎖️ {rank} ≡ رتبتك هي ← 

≡ رسائلك بالتفاعل ← {count}
≡ ترتيبك بالمتفاعلين ← {pos}
-
🔄 تحديث تلقائي ²⁷"""
        bot.reply_to(m, reply_text)
        return

    # ===== رتبته - يحدث تلقائيا =====
    if text in ["رتبته","رتبته ²⁷","رتبه","رتبه ²⁷"] and m.reply_to_message:
        target_id = m.reply_to_message.from_user.id
        rank = get_user_rank_name(target_id, chat_id)
        count, pos = get_user_stats(chat_id, target_id)
        bot.reply_to(m, f"≡ رتبتك هي ← {rank} 🎖️\n\n≡ رسائلك بالتفاعل ← {count}\n≡ ترتيبك بالمتفاعلين ← {pos}\n-\n🔄 تحديث تلقائي")
        return

    if text.startswith("رتبته") or text.startswith("رتبه"):
        if m.reply_to_message:
            target_id = m.reply_to_message.from_user.id
            rank = get_user_rank_name(target_id, chat_id)
            count, pos = get_user_stats(chat_id, target_id)
            bot.reply_to(m, f"≡ رتبتك هي ← {rank} 🎖️\n\n≡ رسائلك بالتفاعل ← {count}\n≡ ترتيبك بالمتفاعلين ← {pos}\n-\n🔄 تحديث تلقائي")
            return

    # ===== المتفاعلين - يحدث تلقائيا =====
    if text in ["المتفاعلين","متفاعلين","تفاعل","التفاعل"]:
        chat_id_str = str(chat_id)
        if chat_id_str not in top_data or not top_data[chat_id_str]:
            bot.reply_to(m, "❌ ما فيه تفاعل بعد")
            return
        sorted_users = sorted(top_data[chat_id_str].items(), key=lambda x: x[1]["count"], reverse=True)[:15]
        txt = f"📊 المتفاعلين في {chat_title} ²⁷\n━━━━━━━━━━━━━━\n"
        for idx, (uid, data) in enumerate(sorted_users, 1):
            uid_int = int(uid)
            name = data["name"]
            count = data["count"]
            rank = get_user_rank_name(uid_int, chat_id)
            if idx == 1:
                medal = "🥇"
            elif idx == 2:
                medal = "🥈"
            elif idx == 3:
                medal = "🥉"
            else:
                medal = f"{idx}."
            txt += f"{medal} {name} — {count} — [{rank}]\n"
        txt += "━━━━━━━━━━━━━━\n🔄 تحديث تلقائي"
        bot.reply_to(m, txt)
        return

    # تحديث الاوامر يدوي
    if text in ["تحديث الاوامر","تحديث"]:
        load_all()
        bot.reply_to(m, f"🔄 تم تحديث كل الاوامر تلقائيا ✅\n• اوامر: {len(custom)}\n• رتب: {sum(len(v) for v in user_ranks.values())}\n• اقفال: {len(locked)}")
        return

    # قفل امر - يحدث تلقائي
    if text.startswith("قفل امر ") or text.startswith("قفل أمر "):
        if user_id != OWNER_BOT_ID and get_user_rank_level(user_id, chat_id) < RANK_ORDER.get("Dev",12):
            bot.reply_to(m, "❌ فقط Dev")
            return
        cmd_text = text.replace("قفل امر ","").replace("قفل أمر ","").strip()
        parts = cmd_text.split()
        if len(parts) >= 2:
            possible_rank = normalize_rank(parts[-1])
            if possible_rank in RANK_ORDER:
                command_name = " ".join(parts[:-1]).strip()
                locked[command_name] = possible_rank
                save_locked()
                bot.reply_to(m, f"≡ تم وضع امر ↤ {command_name}\n≡ لرتبة ↤ {possible_rank} 🎖️\n≡ فقط\n🔄 تحديث تلقائي للكل ✅")
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
            bot.reply_to(m, f"≡ تم وضع امر ↤ {command}\n≡ لرتبة ↤ {rank} 🎖️\n≡ فقط\n🔄 تحديث تلقائي للكل ✅")
            return

    if text.startswith("فتح امر ") or text.startswith("فتح أمر "):
        cmd = text.replace("فتح امر ","").replace("فتح أمر ","").strip()
        if cmd in locked:
            del locked[cmd]
            save_locked()
            bot.reply_to(m, f"✅ فتح {cmd}\n🔄 تحديث تلقائي")
        else:
            bot.reply_to(m, f"❌ {cmd} مو مقفول")
        return

    if text in ["قائمة الاقفال","قائمه الاقفال","الاقفال"]:
        if not locked:
            bot.reply_to(m, "ما فيه اقفال - تحديث تلقائي ✅")
            return
        txt = "🔒 الاقفال (تحديث تلقائي):\n"
        for cmd, rank in locked.items():
            txt += f"• {cmd} ↤ {rank}\n"
        bot.reply_to(m, txt)
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
            bot.reply_to(m, f"✅ تم تغيير اسم القروب:\n{new_name}\n🔄 تحديث تلقائي")
        except Exception as e:
            bot.reply_to(m, f"❌ ما قدرت\n{e}")
        return

    if text in ["تقييد","قيد","كتم"]:
        if not can_use_command(user_id, chat_id, "كتم") and not can_use_command(user_id, chat_id, text):
            required = locked.get("كتم") or locked.get(text) or "مميز"
            bot.reply_to(m, f"❌ {text} مقفول لـ {required}")
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
            bot.reply_to(m, f"❌ ما تقدر تقيد {target_name}")
            return
        try:
            bot.restrict_chat_member(chat_id=chat_id, user_id=target_id, permissions=ChatPermissions(can_send_messages=False))
            mention_text = f"• المستخدم ذا <a href='tg://user?id={target_id}'>{target_name}</a> قيده ²⁷ 🔒"
            bot.send_message(chat_id, mention_text, parse_mode="HTML", reply_to_message_id=m.message_id)
        except Exception as e:
            bot.reply_to(m, f"ما قدرت\n{e}")
        return

    if text in ["فك التقييد","فك تقييد","فك كتم"]:
        if not can_use_command(user_id, chat_id, "كتم"):
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

    if text in ["المطور","المطورر","مطور"]:
        if not can_use_command(user_id, chat_id, "المطور"):
            required = locked.get("المطور") or "Dev"
            bot.reply_to(m, f"❌ المطور مقفول لـ {required}")
            return
        markup = get_owner_button()
        text_out = get_motawer_text(chat_title)
        if owner_info.get("photo"):
            try:
                bot.send_photo(chat_id, owner_info["photo"], caption=text_out, reply_markup=markup, reply_to_message_id=m.message_id)
                return
            except:
                pass
        bot.send_message(chat_id, text_out, reply_markup=markup, reply_to_message_id=m.message_id)
        return

    if text in custom:
        if text in ["تقييد","المطور","كتم"]:
            return
        if not can_use_command(user_id, chat_id, text):
            required = locked.get(text) or "مميز"
            bot.reply_to(m, f"❌ {text} مقفول لـ {required}")
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

print("READY - AUTO UPDATE ALL COMMANDS + RANK + TOP + AFIWD")

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
