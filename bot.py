# -*- coding: utf-8 -*-
# FINAL CLEAN - توكن جديد + بدون A_TOOLSx2 + رموز مميزة + توجيه + تقييد حقيقي
# Token: 8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA
# ID: 829238313

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - FINAL CLEAN 829238313 - NEW TOKEN", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask on {port} - NEW TOKEN")
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, requests
from telebot.types import ChatPermissions, MessageEntity

# التوكن الجديد - نظيف بدون A_TOOLSx2
BOT_TOKEN = "8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
OWNER_BOT_ID = 829238313

print(f"=== FINAL CLEAN - NEW TOKEN ===")
print(f"Token: {BOT_TOKEN[:30]}...")
print(f"Owner: {OWNER_BOT_ID}")
print(f"NO A_TOOLSx2 ✅")

try:
    print("🔧 حذف Webhook + تنظيف...")
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
    print("✅ Webhook محذوف - البوت القديم مات")
    time.sleep(1)
except Exception as e:
    print(f"Webhook: {e}")

FILE = 'custom_commands.json'
custom = {}
try:
    with open(FILE,'r',encoding='utf-8') as f:
        custom = json.load(f)
except:
    custom = {}
def save_custom():
    with open(FILE,'w',encoding='utf-8') as f:
        json.dump(custom,f,ensure_ascii=False,indent=2)

waiting = {}
pending = {}

def get_target_name(message):
    if message.reply_to_message:
        u = message.reply_to_message.from_user
        return u.first_name or "الشخص", u.id, u
    else:
        u = message.from_user
        return u.first_name or "الشخص", u.id, u

def extract_entities(msg):
    entities = []
    src_entities = None
    if msg.entities:
        src_entities = msg.entities
    elif msg.caption_entities:
        src_entities = msg.caption_entities
    if src_entities:
        for e in src_entities:
            ent = {"type": e.type, "offset": e.offset, "length": e.length}
            if e.url:
                ent["url"] = e.url
            if hasattr(e, 'custom_emoji_id') and e.custom_emoji_id:
                ent["custom_emoji_id"] = e.custom_emoji_id
            if hasattr(e, 'language') and e.language:
                ent["language"] = e.language
            entities.append(ent)
    return entities

def format_text_with_entities(template, message, template_entities=None):
    name, uid, user = get_target_name(message)
    username = f"@{user.username}" if user.username else name
    res = template
    new_entities = [dict(e) for e in (template_entities or [])]
    
    replacements = [
        ("{فلان}", name),
        ("{الاسم}", name),
        ("{name}", name),
        ("{المعرف}", username),
        ("فلان", name),
        ("Løst", name),
        ("L0st", name),
    ]
    
    for old, new in replacements:
        if old in res:
            idx = res.find(old)
            while idx != -1:
                for ent in new_entities:
                    if ent["offset"] > idx:
                        ent["offset"] += len(new) - len(old)
                    elif ent["offset"] <= idx and ent["offset"] + ent["length"] > idx:
                        ent["length"] += len(new) - len(old)
                res = res.replace(old, new, 1)
                idx = res.find(old, idx + len(new))
            break
    return res, new_entities, name

def send_with_entities(chat_id, text, entities, reply_to_msg_id):
    if not entities:
        bot.send_message(chat_id, text, reply_to_message_id=reply_to_msg_id)
        return
    try:
        tele_entities = []
        for e in entities:
            me = MessageEntity(
                type=e["type"],
                offset=e["offset"],
                length=e["length"],
                url=e.get("url"),
                custom_emoji_id=e.get("custom_emoji_id"),
                language=e.get("language")
            )
            tele_entities.append(me)
        bot.send_message(chat_id, text, entities=tele_entities, reply_to_message_id=reply_to_msg_id)
    except Exception as ex:
        print(f"entities failed {ex}")
        bot.send_message(chat_id, text, reply_to_message_id=reply_to_msg_id)

@bot.message_handler(chat_types=['private'], func=lambda m: m.from_user.id == OWNER_BOT_ID, content_types=['text','photo','video','document','sticker','voice','animation'])
def private_lab(m):
    uid = m.from_user.id
    text_content = (m.text or m.caption or "").strip()

    if uid in waiting and waiting[uid]['step'] == 'wait_reply':
        cmd = waiting[uid]['command']
        entities = extract_entities(m)
        
        if m.content_type == 'text':
            data = {"type": "text", "text": m.text, "entities": entities, "file_id": None, "caption": "", "caption_entities": []}
        elif m.content_type == 'photo':
            cap_entities = []
            if m.caption_entities:
                for e in m.caption_entities:
                    ent = {"type": e.type, "offset": e.offset, "length": e.length}
                    if hasattr(e, 'custom_emoji_id') and e.custom_emoji_id:
                        ent["custom_emoji_id"] = e.custom_emoji_id
                    if e.url:
                        ent["url"] = e.url
                    cap_entities.append(ent)
            data = {"type": "photo", "text": "", "entities": [], "file_id": m.photo[-1].file_id, "caption": m.caption or "", "caption_entities": cap_entities}
        elif m.content_type == 'video':
            cap_entities = []
            if m.caption_entities:
                for e in m.caption_entities:
                    ent = {"type": e.type, "offset": e.offset, "length": e.length}
                    if hasattr(e, 'custom_emoji_id') and e.custom_emoji_id:
                        ent["custom_emoji_id"] = e.custom_emoji_id
                    cap_entities.append(ent)
            data = {"type": "video", "text": "", "entities": [], "file_id": m.video.file_id, "caption": m.caption or "", "caption_entities": cap_entities}
        else:
            data = {"type": m.content_type, "text": m.text or m.caption or "", "entities": entities, "file_id": getattr(m, m.content_type).file_id if hasattr(m, m.content_type) and hasattr(getattr(m, m.content_type), 'file_id') else None, "caption": m.caption or "", "caption_entities": []}
        
        pending[uid] = {"t": cmd, "data": data}
        del waiting[uid]
        
        bot.reply_to(m, f"تمام ✅\nالأمر: {cmd}\nالنوع: {data['type']}\nالرموز المميزة: {'✅' if entities or data.get('caption_entities') else 'لا يوجد'}\n\nتجربة:")
        if data["type"] == "text":
            formatted, new_ents, _ = format_text_with_entities(data["text"], m, data["entities"])
            send_with_entities(m.chat.id, formatted, new_ents, None)
        elif data["type"] == "photo":
            cap = data["caption"]
            if cap:
                cap, new_ents, _ = format_text_with_entities(cap, m, data["caption_entities"])
            else:
                new_ents = []
            try:
                if new_ents:
                    tele_ents = [MessageEntity(type=e["type"], offset=e["offset"], length=e["length"], url=e.get("url"), custom_emoji_id=e.get("custom_emoji_id")) for e in new_ents]
                    bot.send_photo(m.chat.id, data["file_id"], caption=cap, caption_entities=tele_ents)
                else:
                    bot.send_photo(m.chat.id, data["file_id"], caption=cap)
            except:
                bot.send_photo(m.chat.id, data["file_id"], caption=cap)
        
        bot.send_message(m.chat.id, "عجبك؟ اكتب: ارفعه")
        return

    if text_content.startswith("اضف امر"):
        tmp = text_content.replace("اضف امر:", "").replace("اضف امر", "").strip()
        if "->" in tmp:
            a,b = tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                entities = extract_entities(m)
                data = {"type": "text", "text": resp, "entities": entities, "file_id": None, "caption": "", "caption_entities": []}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m, f"تمام ✅\nالأمر: {trig}\nالرد: {resp}\n\nتجربة:")
                formatted, new_ents, _ = format_text_with_entities(resp, m, entities)
                send_with_entities(m.chat.id, formatted, new_ents, None)
                bot.send_message(m.chat.id, "اكتب: ارفعه")
                return
        else:
            cmd = tmp
            if not cmd:
                bot.reply_to(m, "اكتب: اضف امر: المطور")
                return
            waiting[uid] = {"step": "wait_reply", "command": cmd}
            bot.reply_to(m, f"تمام - الأمر: {cmd}\n\nالحين ارسل الرد:\n• نص مع رموز مميزة ²⁷ ↦ •\n• ايموجي بريميوم\n• صورة + كلام\n• توجيه\n\nكلها تنحفظ ✅")
            return

    if text_content in ["ارفعه","ارفعه للسيرفر","احفظه"]:
        if uid not in pending:
            bot.reply_to(m, "ما فيه امر")
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ تم حفظه!\n{t} -> {data['type']} ✅\nيشتغل في كل القروبات 🔥")
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
            if isinstance(v, str):
                txt+=f"• {k} -> {v}\n"
            else:
                txt+=f"• {k} -> [{v.get('type')}] {v.get('text','')[:30]}\n"
        bot.reply_to(m, txt)
        return

    if text_content.startswith("احذف امر"):
        t=text_content.replace("احذف امر:","").replace("احذف امر","").strip()
        if t in custom:
            del custom[t]; save_custom()
            bot.reply_to(m, f"✅ حذف {t}")
        else:
            bot.reply_to(m, f"ما لقيت {t}")
        return

    if text_content in ["/start","start","بدا"]:
        bot.reply_to(m, f"""اهلا - {uid} ✅
التوكن الجديد شغال - بدون A_TOOLSx2

يدعم:
• الرموز المميزة ²⁷ ↦ • ⭐
• ايموجي بريميوم
• التوجيه + صور

اضافة:
اضف امر: المطور
[ارسل نص مع رموز او صورة]
ارفعه

تقييد حقيقي:
تقييد - بالرد يقيده + اسم متغير {{فلان}}
فك التقييد

اوامري - عرض
""")
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
                if isinstance(data, str):
                    formatted, _, _ = format_text_with_entities(data, m, [])
                    bot.reply_to(m, formatted)
                else:
                    txt = data.get("text","") or data.get("caption","")
                    ents = data.get("entities") or data.get("caption_entities") or []
                    formatted, new_ents, _ = format_text_with_entities(txt, m, ents)
                    send_with_entities(chat_id, formatted, new_ents, m.message_id)
            else:
                bot.reply_to(m, f"• المستخدم ذا {target_name} قيده 🔒")
        except Exception as e:
            bot.reply_to(m, f"ما قدرت اقيده - البوت لازم مشرف\n{e}")
        return

    if text in ["فك التقييد","فك تقييد","فك الكتم"]:
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

    if text in custom:
        if text in ["تقييد","تقييدد","قيد","كتم"]:
            return
        data = custom[text]
        if isinstance(data, str):
            formatted, _, _ = format_text_with_entities(data, m, [])
            bot.reply_to(m, formatted)
        else:
            ctype = data.get("type","text")
            txt = data.get("text","") or ""
            cap = data.get("caption","") or ""
            entities = data.get("entities") or []
            cap_entities = data.get("caption_entities") or []
            
            if txt:
                txt, new_ents, _ = format_text_with_entities(txt, m, entities)
                entities = new_ents
            if cap:
                cap, new_cap_ents, _ = format_text_with_entities(cap, m, cap_entities)
                cap_entities = new_cap_ents
            
            try:
                if ctype == "text":
                    send_with_entities(chat_id, txt, entities, m.message_id)
                elif ctype == "photo":
                    if cap_entities:
                        tele_ents = [MessageEntity(type=e["type"], offset=e["offset"], length=e["length"], url=e.get("url"), custom_emoji_id=e.get("custom_emoji_id")) for e in cap_entities]
                        bot.send_photo(chat_id, data["file_id"], caption=cap or txt, caption_entities=tele_ents, reply_to_message_id=m.message_id)
                    else:
                        bot.send_photo(chat_id, data["file_id"], caption=cap or txt, reply_to_message_id=m.message_id)
                elif ctype == "video":
                    bot.send_video(chat_id, data["file_id"], caption=cap or txt, reply_to_message_id=m.message_id)
                else:
                    send_with_entities(chat_id, txt or cap, entities or cap_entities, m.message_id)
            except Exception as e:
                print(f"send err {e}")
                bot.reply_to(m, txt or cap)

print("="*50)
print("✅ FINAL CLEAN - NEW TOKEN")
print("✅ 8769832522:AAF-qXZf...")
print("✅ NO A_TOOLSx2")
print("✅ SPECIAL SYMBOLS ²⁷ ↦ •")
print("✅ FORWARD + PHOTO")
print("✅ REAL RESTRICT + {فلان}")
print("="*50)

while True:
    try:
        print("✅ Starting polling with NEW TOKEN...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True, none_stop=True)
    except Exception as e:
        err=str(e)
        if "409" in err or "Conflict" in err:
            print("⚠️ 409 - انتظار...")
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
