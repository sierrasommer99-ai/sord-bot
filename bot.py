# -*- coding: utf-8 -*-
# FINAL - رابط خاصك afiwd + صورة + بايو + اسم + زر اسفل
# Token: 8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA
# ID: 829238313
# خاصك: https://t.me/afiwd

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - AFIWD PRIVATE", 200
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

print(f"FINAL AFIWD - {OWNER_BOT_ID}")

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

# افتراضي خاصك afiwd
owner_info = {}
try:
    with open(OWNER_FILE,'r',encoding='utf-8') as f:
        owner_info = json.load(f)
        # حدث خاصك الجديد اذا قديم
        if owner_info.get('private') == 'iu56v':
            owner_info['private'] = 'afiwd'
            owner_info['username'] = 'afiwd'
            owner_info['bio'] = 'https://t.me/afiwd'
except:
    owner_info = {"name": "محسن", "username": "afiwd", "bio": "https://t.me/afiwd", "group": "- darkness", "private": "afiwd", "photo": None}

# اجباري حدث لخاصك الجديد
owner_info["private"] = "afiwd"
owner_info["username"] = "afiwd"
owner_info["bio"] = "https://t.me/afiwd"
if not owner_info.get("name"):
    owner_info["name"] = "محسن"

def save_custom():
    with open(FILE,'w',encoding='utf-8') as f:
        json.dump(custom,f,ensure_ascii=False,indent=2)

def save_owner():
    with open(OWNER_FILE,'w',encoding='utf-8') as f:
        json.dump(owner_info,f,ensure_ascii=False,indent=2)

waiting = {}
pending = {}
edit_motawer = {}

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

@bot.message_handler(chat_types=['private'], func=lambda m: m.from_user.id == OWNER_BOT_ID, content_types=['text','photo','video','document','sticker','voice','animation','audio','video_note'])
def private_lab(m):
    global owner_info
    uid = m.from_user.id
    text_content = (m.text or m.caption or "").strip()

    # تعديل معلومات المطور
    if text_content in ["عدل معلومات المطور","تعديل المطور","عدل المطور","تعديل معلومات المطور"]:
        edit_motawer[uid] = {"step": "name", "data": dict(owner_info)}
        bot.reply_to(m, f"""✏️ تعديل معلومات المطور ²⁷ ↦
خاصك: https://t.me/afiwd

الحالي:
الاسم: {owner_info.get('name')}
اليوزر: @{owner_info.get('username')}
البايو: {owner_info.get('bio')}

ارسل الاسم الجديد (او تخطي):""")
        return

    if uid in edit_motawer:
        step = edit_motawer[uid]["step"]
        data = edit_motawer[uid]["data"]
        
        if text_content.lower() in ["تخطي","skip"]:
            pass
        else:
            if step == "name":
                if m.content_type == 'text':
                    data["name"] = text_content
                edit_motawer[uid]["step"] = "bio"
                bot.reply_to(m, f"✅ الاسم: {data['name']} ²⁷\nالحين البايو الجديد (او تخطي):")
                return
            elif step == "bio":
                if m.content_type == 'text':
                    data["bio"] = text_content
                edit_motawer[uid]["step"] = "photo"
                bot.reply_to(m, f"✅ البايو: {data['bio']} ²⁷\nالحين ارسل صورة المطور (او تم للحفظ):")
                return
            elif step == "photo":
                if m.content_type == 'photo':
                    data["photo"] = m.photo[-1].file_id
                    bot.reply_to(m, f"✅ حفظت الصورة ²⁷")
                elif text_content.lower() in ["تم","حفظ","انتهى","تخطي","skip"]:
                    pass
                else:
                    bot.reply_to(m, "ارسل صورة او اكتب تم")
                    return
        
        if edit_motawer[uid]["step"] == "photo":
            owner_info = edit_motawer[uid]["data"]
            owner_info["private"] = "afiwd"
            owner_info["username"] = "afiwd"
            save_owner()
            del edit_motawer[uid]
            markup = get_owner_button()
            text_preview = get_motawer_text()
            if owner_info.get("photo"):
                try:
                    bot.send_photo(m.chat.id, owner_info["photo"], caption=text_preview, reply_markup=markup)
                except:
                    bot.reply_to(m, text_preview, reply_markup=markup)
            else:
                bot.reply_to(m, f"✅ تم تعديل معلومات المطور ²⁷ ↦\n\n{text_preview}", reply_markup=markup)
            return

    if text_content.startswith("احفظ معلوماتي") or text_content.startswith("ضع معلوماتي"):
        parts = text_content.replace("احفظ معلوماتي","").replace("ضع معلوماتي","").replace(":","").strip()
        if parts:
            segs = re.split(r'\||،|,', parts)
            if len(segs) >= 1 and segs[0].strip():
                owner_info["name"] = segs[0].strip()
            if len(segs) >= 2 and segs[1].strip():
                # اجباري afiwd
                pass
            if len(segs) >= 3 and segs[2].strip():
                owner_info["bio"] = segs[2].strip()
        owner_info["private"] = "afiwd"
        owner_info["username"] = "afiwd"
        save_owner()
        markup = get_owner_button()
        bot.reply_to(m, f"✅ حفظت ²⁷:\n{owner_info['name']} ↦ @afiwd\nhttps://t.me/afiwd", reply_markup=markup)
        return

    # ضع صورة المطور
    if m.content_type == 'photo' and ("صورة المطور" in text_content or "صوره المطور" in text_content or text_content == ""):
        # اذا ارسل صورة مع كابشن فيه "ضع صورة المطور" او بدون كابشن في وضع الانتظار
        if "صورة المطور" in (m.caption or "") or text_content == "" or "صورة" in text_content:
            owner_info["photo"] = m.photo[-1].file_id
            save_owner()
            markup = get_owner_button()
            text_preview = get_motawer_text()
            try:
                bot.send_photo(m.chat.id, owner_info["photo"], caption=text_preview, reply_markup=markup)
                bot.send_message(m.chat.id, "✅ تم حفظ صورة المطور + الزر اسفل ²⁷ ↦")
            except:
                bot.reply_to(m, "✅ تم حفظ صورة المطور")
            return

    if text_content.startswith("ضع صورة المطور"):
        bot.reply_to(m, "📸 ارسل صورة المطور الحين\nالصورة + الزر بيظهر تحتها تلقائي ²⁷ ↦")
        waiting[uid] = {"step": "wait_photo_motawer", "command": "صورة المطور"}
        return

    if uid in waiting and waiting[uid].get("step") == "wait_photo_motawer":
        if m.content_type == 'photo':
            owner_info["photo"] = m.photo[-1].file_id
            save_owner()
            del waiting[uid]
            markup = get_owner_button()
            text_preview = get_motawer_text()
            bot.send_photo(m.chat.id, owner_info["photo"], caption=text_preview, reply_markup=markup)
            bot.send_message(m.chat.id, "✅ تم حفظ صورة المطور + الاسم + البايو + الزر اسفل ²⁷ ↦\nجرب المطور في القروب")
        else:
            bot.reply_to(m, "ارسل صورة ²⁷")
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
        bot.reply_to(m, f"تمام ✅ ²⁷\nالأمر: {cmd}\nاكتب: ارفعه")
        return

    if text_content.startswith("اضف امر"):
        tmp = text_content.replace("اضف امر:", "").replace("اضف امر", "").strip()
        if "->" in tmp:
            a,b = tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                data = {"type": "text", "text": resp, "entities": save_all_entities(m), "file_id": None, "caption": "", "caption_entities": []}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m, f"تمام ✅ ²⁷\n{trig} ↦ {resp}\nاكتب: ارفعه")
                return
        else:
            cmd = tmp
            if not cmd:
                return
            waiting[uid] = {"step": "wait_reply", "command": cmd}
            bot.reply_to(m, f"تمام - الأمر: {cmd} ²⁷\nارسل الرد:")
            return

    if text_content in ["ارفعه","احفظه","ارفعه للسيرفر","ارفعه ²⁷"]:
        if uid not in pending:
            bot.reply_to(m, "ما فيه امر ²⁷")
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ تم حفظه ²⁷ ↦!\n{t}")
        return

    if text_content in ["الغاء","الغه"]:
        waiting.pop(uid,None); pending.pop(uid,None); edit_motawer.pop(uid,None)
        bot.reply_to(m, "❌ الغاء ²⁷")
        return

    if text_content in ["معلوماتي","معلومات المطور","عرض المطور"]:
        markup = get_owner_button()
        text_preview = get_motawer_text()
        if owner_info.get("photo"):
            try:
                bot.send_photo(m.chat.id, owner_info["photo"], caption=text_preview, reply_markup=markup)
            except:
                bot.reply_to(m, text_preview, reply_markup=markup)
        else:
            bot.reply_to(m, text_preview, reply_markup=markup)
        return

    if text_content in ["/start","start","بدا"]:
        markup = get_owner_button()
        bot.reply_to(m, f"""اهلا - {uid} ✅ ²⁷
خاصك: https://t.me/afiwd

لتعديل معلومات المطور مع صورة + بايو + اسم + زر اسفل:

1️⃣ عدل معلومات المطور
→ يسالك اسم → بايو → صورة

2️⃣ ضع صورة المطور
→ ارسل صورة → تنحفظ مع الزر

3️⃣ احفظ معلوماتي: محسن | afiwd | https://t.me/afiwd

معلوماتك الحالية:
{get_motawer_text()}

مع صورة + زر اسفل ↦
""", reply_markup=markup)
        return

@bot.message_handler(content_types=['text'])
def groups(m):
    if m.chat.type == 'private':
        return
    text = (m.text or "").strip()
    chat_id = m.chat.id
    chat_title = m.chat.title or "القروب"

    if text.startswith("ضع اسم القروب") or text.startswith("ضع اسم"):
        if m.from_user.id != OWNER_BOT_ID:
            bot.reply_to(m, "❌ فقط المالك ²⁷")
            return
        new_name = text.replace("ضع اسم القروب:","").replace("ضع اسم القروب","").replace("ضع اسم:","").replace("ضع اسم","").strip()
        if not new_name:
            return
        try:
            bot.set_chat_title(chat_id, new_name)
            owner_info["group"] = new_name
            save_owner()
            bot.reply_to(m, f"✅ تم تغيير اسم القروب ²⁷ ↦:\n{new_name}")
        except Exception as e:
            bot.reply_to(m, f"❌ ما قدرت ²⁷\n{e}")
        return

    if text in ["تقييد","تقييدد","قيد","كتم","كتمم","تقييد ²⁷"]:
        if not m.reply_to_message:
            bot.reply_to(m, "❌ رد على الشخص ²⁷")
            return
        target = m.reply_to_message.from_user
        target_id = target.id
        target_name = target.first_name or "الشخص"
        if target_id == bot.get_me().id:
            return
        try:
            bot.restrict_chat_member(chat_id=chat_id, user_id=target_id, permissions=ChatPermissions(can_send_messages=False))
            mention_text = f"• المستخدم ذا <a href='tg://user?id={target_id}'>{target_name}</a> قيده ²⁷ ↦ 🔒"
            bot.send_message(chat_id, mention_text, parse_mode="HTML", reply_to_message_id=m.message_id)
        except Exception as e:
            bot.reply_to(m, f"ما قدرت اقيده ²⁷\n{e}")
        return

    if text in ["فك التقييد","فك تقييد","فك التقييد ²⁷"]:
        if not m.reply_to_message:
            return
        target = m.reply_to_message.from_user
        target_id = target.id
        target_name = target.first_name or "الشخص"
        try:
            bot.restrict_chat_member(chat_id=chat_id, user_id=target_id, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            mention_text = f"• المستخدم ذا <a href='tg://user?id={target_id}'>{target_name}</a> فكينا قيده ✅ ²⁷ ↦"
            bot.send_message(chat_id, mention_text, parse_mode="HTML", reply_to_message_id=m.message_id)
        except:
            pass
        return

    # المطور - مع صورة + بايو + اسم + زر اسفل لخاصك afiwd
    if text in ["المطور","المطورر","المطور ²⁷","مطور"]:
        real_group_name = chat_title
        markup = get_owner_button()
        text_out = get_motawer_text(real_group_name)
        
        # اذا عندك صورة محفوظة - ارسلها مع الزر اسفل
        if owner_info.get("photo"):
            try:
                bot.send_photo(chat_id, owner_info["photo"], caption=text_out, reply_markup=markup, reply_to_message_id=m.message_id)
                return
            except Exception as e:
                print(f"photo error: {e}")
        
        # اذا ما عندك صورة خاصة، شوف اذا امر المطور فيه صورة مخصصة
        if "المطور" in custom:
            data = custom["المطور"]
            if data.get("type") == "photo":
                try:
                    # اذا الصورة من الامر المخصص - ارسلها مع معلوماتك المحدثة + زر afiwd
                    bot.send_photo(chat_id, data["file_id"], caption=text_out, reply_markup=markup, reply_to_message_id=m.message_id)
                except:
                    bot.send_message(chat_id, text_out, reply_markup=markup, reply_to_message_id=m.message_id)
                return
        
        # بدون صورة - نص + زر اسفل
        bot.send_message(chat_id, text_out, reply_markup=markup, reply_to_message_id=m.message_id)
        return

    if text in custom:
        if text in ["تقييد","المطور"]:
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
                    ents = restore_all_entities(data.get("caption_entities",[]))
                    if ents:
                        bot.send_animation(chat_id, data["file_id"], caption=data.get("caption",""), caption_entities=ents, reply_to_message_id=m.message_id)
                    else:
                        bot.send_animation(chat_id, data["file_id"], caption=data.get("caption",""), reply_to_message_id=m.message_id)
                elif ctype == "video":
                    ents = restore_all_entities(data.get("caption_entities",[]))
                    if ents:
                        bot.send_video(chat_id, data["file_id"], caption=data.get("caption",""), caption_entities=ents, reply_to_message_id=m.message_id)
                    else:
                        bot.send_video(chat_id, data["file_id"], caption=data.get("caption",""), reply_to_message_id=m.message_id)
            except Exception as e:
                print(f"error: {e}")
                bot.reply_to(m, data.get("text","") or data.get("caption",""))
        else:
            bot.reply_to(m, str(data))

print("READY - AFIWD + PHOTO + BIO + BUTTON BELOW")

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
            print(f"❌ ²⁷ {e}")
            time.sleep(5)
