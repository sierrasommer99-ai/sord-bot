# -*- coding: utf-8 -*-
# يضيف زر يدخل الناس خاصك + يحط اسم المقيد صح + معلوماتك
# Token: 8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA
# ID: 829238313

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - WITH BUTTON TO PRIVATE", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, requests, re
from telebot.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
OWNER_BOT_ID = 829238313

print(f"WITH BUTTON - {OWNER_BOT_ID}")

try:
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
except:
    pass

FILE = 'custom_commands.json'
OWNER_FILE = 'owner_info.json'

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
except:
    owner_info = {"name": "محسن", "username": "iu56v", "bio": "https://t.me/iu56v", "group": "- darkness", "private": "iu56v"}

def save_custom():
    with open(FILE,'w',encoding='utf-8') as f:
        json.dump(custom,f,ensure_ascii=False,indent=2)

def save_owner():
    with open(OWNER_FILE,'w',encoding='utf-8') as f:
        json.dump(owner_info,f,ensure_ascii=False,indent=2)

waiting = {}
pending = {}

def get_target(message):
    if message.reply_to_message:
        u = message.reply_to_message.from_user
        return u.first_name or "الشخص", u.id, u
    else:
        u = message.from_user
        return u.first_name or "الشخص", u.id, u

def format_name(text, target_name):
    if not text:
        return f"• المستخدم ذا {target_name} قيده"
    text = re.sub(r'「\s*」', f' {target_name} ', text)
    text = re.sub(r'\[\s*\]', f' {target_name} ', text)
    text = text.replace("{فلان}", target_name).replace("{الاسم}", target_name).replace("{name}", target_name).replace("فلان", target_name)
    text = text.replace("Løst", target_name).replace("L0st", target_name)
    if target_name not in text and "المستخدم ذا" in text:
        text = text.replace("المستخدم ذا", f"المستخدم ذا {target_name}")
    if "• المستخدم ذا" in text and target_name not in text:
        text = re.sub(r'المستخدم ذا\s*[•\-\s]*\s*قيده', f'المستخدم ذا {target_name} قيده', text)
    if target_name not in text and ("قيده" in text):
        text = f"• المستخدم ذا {target_name} قيده"
    return text

def get_owner_button():
    """زر يدخل الناس خاصك"""
    username = owner_info.get('username','iu56v').replace('@','')
    private_link = owner_info.get('private', username) or username
    private_link = private_link.replace('@','').replace('https://t.me/','').replace('http://t.me/','')
    url = f"https://t.me/{private_link}"
    
    markup = InlineKeyboardMarkup(row_width=1)
    # زر يدخل خاصك
    markup.add(InlineKeyboardButton(f"💬 مراسلة {owner_info.get('name','المالك')}", url=url))
    markup.add(InlineKeyboardButton(f"👤 دخول خاصي", url=url))
    return markup

@bot.message_handler(chat_types=['private'], func=lambda m: m.from_user.id == OWNER_BOT_ID, content_types=['text','photo','video','document','sticker','voice','animation'])
def private_lab(m):
    global owner_info
    uid = m.from_user.id
    text_content = (m.text or m.caption or "").strip()

    # احفظ معلوماتي: الاسم | المعرف | رابط الخاص
    if text_content.startswith("احفظ معلوماتي") or text_content.startswith("ضع معلوماتي"):
        parts = text_content.replace("احفظ معلوماتي","").replace("ضع معلوماتي","").replace(":","").strip()
        if parts:
            segs = re.split(r'\||،|,', parts)
            if len(segs) >= 1 and segs[0].strip():
                owner_info["name"] = segs[0].strip()
            if len(segs) >= 2 and segs[1].strip():
                u = segs[1].strip().replace('@','').replace('https://t.me/','')
                owner_info["username"] = u
                owner_info["private"] = u
            if len(segs) >= 3 and segs[2].strip():
                b = segs[2].strip()
                owner_info["bio"] = b
                # اذا البايو رابط خاص
                if 't.me/' in b:
                    owner_info["private"] = b.replace('https://t.me/','').replace('@','')
        else:
            u = m.from_user
            owner_info["name"] = u.first_name or "محسن"
            owner_info["username"] = u.username or "iu56v"
            owner_info["private"] = u.username or "iu56v"
        
        owner_info["group"] = "- darkness"
        save_owner()
        
        markup = get_owner_button()
        bot.reply_to(m, f"""✅ تم حفظ معلوماتك:

الاسم: {owner_info['name']}
المعرف: @{owner_info['username']}
الخاص: https://t.me/{owner_info['private']}
البايو: {owner_info['bio']}

الحين زر المطور يودي الناس لخاصك:
https://t.me/{owner_info['private']} ✅
""", reply_markup=markup)
        return

    if text_content in ["معلوماتي","معلومات المالك"]:
        markup = get_owner_button()
        bot.reply_to(m, f"""📋 معلوماتك:

الاسم: {owner_info.get('name')}
الخاص: https://t.me/{owner_info.get('private')}
البايو: {owner_info.get('bio')}

الزر:
""", reply_markup=markup)
        return

    if uid in waiting and waiting[uid]['step'] == 'wait_reply':
        cmd = waiting[uid]['command']
        if m.content_type == 'text':
            data = {"type": "text", "text": m.text, "file_id": None, "caption": ""}
        elif m.content_type == 'photo':
            data = {"type": "photo", "text": "", "file_id": m.photo[-1].file_id, "caption": m.caption or ""}
        else:
            data = {"type": m.content_type, "text": m.text or m.caption or "", "file_id": getattr(m, m.content_type).file_id if hasattr(m, m.content_type) and hasattr(getattr(m, m.content_type), 'file_id') else None, "caption": m.caption or ""}
        
        pending[uid] = {"t": cmd, "data": data}
        del waiting[uid]
        bot.reply_to(m, f"تمام ✅\nالأمر: {cmd}\nالنوع: {data['type']}\nتجربة:")
        if data["type"] == "text":
            bot.send_message(m.chat.id, format_name(data["text"], "نايف"))
        elif data["type"] == "photo":
            bot.send_photo(m.chat.id, data["file_id"], caption=format_name(data["caption"], "نايف"))
        bot.send_message(m.chat.id, "اكتب: ارفعه")
        return

    if text_content.startswith("اضف امر"):
        tmp = text_content.replace("اضف امر:", "").replace("اضف امر", "").strip()
        if "->" in tmp:
            a,b = tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                data = {"type": "text", "text": resp, "file_id": None, "caption": ""}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m, f"تمام ✅\nالأمر: {trig}\nالرد: {resp}\nتجربة:")
                bot.send_message(m.chat.id, format_name(resp, "نايف"))
                bot.send_message(m.chat.id, "اكتب: ارفعه")
                return
        else:
            cmd = tmp
            if not cmd:
                return
            waiting[uid] = {"step": "wait_reply", "command": cmd}
            bot.reply_to(m, f"تمام - الأمر: {cmd}\n\nارسل الرد (نص / صورة / توجيه):")
            return

    if text_content in ["ارفعه","ارفعه للسيرفر","احفظه"]:
        if uid not in pending:
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ تم حفظه!\n{t}")
        return

    if text_content in ["الغاء","الغه"]:
        waiting.pop(uid,None); pending.pop(uid,None)
        bot.reply_to(m, "❌ الغاء")
        return

    if text_content in ["اوامري"]:
        if not custom:
            bot.reply_to(m, "ما اضفت شي")
            return
        txt="📋 اوامرك:\n\n"
        for k,v in custom.items():
            txt+=f"• {k}\n"
        bot.reply_to(m, txt)
        return

    if text_content.startswith("احذف امر"):
        t=text_content.replace("احذف امر:","").replace("احذف امر","").strip()
        if t in custom:
            del custom[t]; save_custom()
            bot.reply_to(m, f"✅ حذف {t}")
        return

    if text_content in ["/start","start","بدا"]:
        markup = get_owner_button()
        bot.reply_to(m, f"""اهلا - {uid} ✅
التوكن الجديد شغال - بدون A_TOOLSx2

👑 معلوماتك:
الاسم: {owner_info.get('name')}
الخاص: https://t.me/{owner_info.get('private')}

لتغيير الزر:
احفظ معلوماتي: محسن | iu56v | https://t.me/iu56v
الاسم | يوزر الخاص | البايو

اوامر:
اضف امر: المطور
[صورة + معلومات]
ارفعه -> يطلع مع زر يدخل خاصك ✅

تقييد -> يحط اسم الشخص صح ✅
""", reply_markup=markup)
        return

@bot.message_handler(content_types=['text'])
def groups(m):
    if m.chat.type == 'private':
        return
    text = (m.text or "").strip()
    chat_id = m.chat.id

    if text in ["تقييد","تقييدد","قيد","كتم","كتمم"]:
        if not m.reply_to_message:
            bot.reply_to(m, "❌ رد على الشخص")
            return
        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name or "الشخص"
        if target_id == bot.get_me().id:
            return
        try:
            bot.restrict_chat_member(chat_id=chat_id, user_id=target_id, permissions=ChatPermissions(can_send_messages=False))
            if "تقييد" in custom:
                data = custom["تقييد"]
                txt = data.get("text","") or data.get("caption","") or "• المستخدم ذا {فلان} قيده"
                reply_txt = format_name(txt, target_name)
                bot.reply_to(m, reply_txt)
            else:
                bot.reply_to(m, f"• المستخدم ذا {target_name} قيده 🔒")
        except Exception as e:
            bot.reply_to(m, f"ما قدرت اقيده\n{e}")
        return

    if text in ["فك التقييد","فك تقييد","الغاء التقييد","فك الكتم"]:
        if not m.reply_to_message:
            return
        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name or "الشخص"
        try:
            bot.restrict_chat_member(chat_id=chat_id, user_id=target_id, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            bot.reply_to(m, f"• المستخدم ذا {target_name} فكينا قيده ✅")
        except:
            pass
        return

    if text in ["المطور","المطورر"]:
        markup = get_owner_button()
        if "المطور" in custom:
            data = custom["المطور"]
            if data.get("type") == "photo":
                cap = data.get("caption","")
                # اذا الكابشن قديم فيه ٢٧ بدله بمعلوماتك
                if "٢٧" in cap or "USE ↦" in cap or "Owner Group" in cap or not cap:
                    cap = f"""Owner Group ↦ {owner_info.get('group','- darkness')}

USE ↦ {owner_info.get('name','محسن')} | {owner_info.get('username','iu56v')}

Bio ↦ {owner_info.get('bio','https://t.me/iu56v')}"""
                bot.send_photo(chat_id, data["file_id"], caption=cap, reply_markup=markup, reply_to_message_id=m.message_id)
            else:
                txt = data.get("text","")
                if "٢٧" in txt or "Owner Group" in txt or not txt:
                    txt = f"""Owner Group ↦ {owner_info.get('group','- darkness')}

USE ↦ {owner_info.get('name','محسن')} | {owner_info.get('username','iu56v')}

Bio ↦ {owner_info.get('bio','https://t.me/iu56v')}"""
                bot.reply_to(m, txt, reply_markup=markup)
        else:
            txt = f"""Owner Group ↦ {owner_info.get('group','- darkness')}

USE ↦ {owner_info.get('name','محسن')} | {owner_info.get('username','iu56v')}

Bio ↦ {owner_info.get('bio','https://t.me/iu56v')}"""
            bot.reply_to(m, txt, reply_markup=markup)
        return

    if text in custom:
        if text in ["تقييد","المطور"]:
            return
        data = custom[text]
        txt = data.get("text","") or data.get("caption","") or ""
        try:
            if data.get("type") == "photo":
                bot.send_photo(chat_id, data["file_id"], caption=txt, reply_to_message_id=m.message_id)
            else:
                bot.reply_to(m, txt)
        except:
            bot.reply_to(m, txt)

print("READY - WITH BUTTON")

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
