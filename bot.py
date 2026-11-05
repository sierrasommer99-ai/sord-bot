# -*- coding: utf-8 -*-
# تقييد حقيقي + يغير الاسم تلقائي + بدون A_TOOLSx2

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - REAL RESTRICT 829238313", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, requests
from telebot.types import ChatPermissions

BOT_TOKEN = "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
OWNER_BOT_ID = 829238313

print(f"=== REAL RESTRICT - ID {OWNER_BOT_ID} ===")

try:
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
    print("✅ Webhook محذوف")
except Exception as e:
    print(e)

custom = {}
FILE = 'custom_commands.json'
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
    """يجيب اسم الشخص اللي رديت عليه - او نفسك اذا ما رديت"""
    if message.reply_to_message:
        u = message.reply_to_message.from_user
        return u.first_name or "الشخص", u.id, u
    else:
        u = message.from_user
        return u.first_name or "الشخص", u.id, u

def format_reply(template, message):
    name, uid, user = get_target_name(message)
    username = f"@{user.username}" if user.username else name
    res = template
    res = res.replace("{الاسم}", name).replace("{فلان}", name).replace("{name}", name).replace("{المعرف}", username)
    return res, uid, user

@bot.message_handler(chat_types=['private'], func=lambda m: m.from_user.id == OWNER_BOT_ID)
def private_lab(m):
    text = m.text.strip()
    uid = m.from_user.id

    if uid in waiting and waiting[uid]['step'] == 'wait_reply':
        cmd = waiting[uid]['command']
        reply_text = m.text
        pending[uid] = {"t": cmd, "r": reply_text}
        del waiting[uid]
        bot.reply_to(m, f"تمام ✅\nالأمر: {cmd}\nالرد: {reply_text}\n\nتجربة:")
        formatted, _, _ = format_reply(reply_text, m)
        bot.send_message(m.chat.id, formatted)
        bot.send_message(m.chat.id, "اكتب: ارفعه")
        return

    if text.startswith("اضف امر:") and "->" not in text or text.startswith("اضف امر ") and "->" not in text:
        cmd = text.replace("اضف امر:", "").replace("اضف امر", "").strip()
        if not cmd:
            bot.reply_to(m, "اكتب: اضف امر: تقييد")
            return
        waiting[uid] = {"step": "wait_reply", "command": cmd}
        bot.reply_to(m, f"تمام - الأمر: {cmd}\n\nالحين ارسل لي وش تبي البوت يرد؟\nمثال: • المستخدم ذا {{فلان}} قيده")
        return

    if "->" in text and (text.startswith("اضف امر") or text.startswith("جرب امر") or text.startswith("اضف:") or text.startswith("جرب:")):
        tmp = text
        for p in ["اضف امر:", "اضف امر", "جرب امر:", "جرب امر", "اضف:", "جرب:"]:
            if tmp.startswith(p):
                tmp = tmp[len(p):].strip()
                break
        if "->" in tmp:
            a, b = tmp.split("->", 1)
            trig = a.strip(); resp = b.strip()
            pending[uid] = {"t": trig, "r": resp}
            bot.reply_to(m, f"تمام ✅\nالأمر: {trig}\nالرد: {resp}\n\nتجربة:")
            formatted, _, _ = format_reply(resp, m)
            bot.send_message(m.chat.id, formatted)
            bot.send_message(m.chat.id, "اكتب: ارفعه")
            return

    if text in ["ارفعه", "ارفعه للسيرفر", "احفظه"]:
        if uid not in pending:
            bot.reply_to(m, "ما فيه امر - اكتب: اضف امر: تقييد")
            return
        t = pending[uid]["t"]; r = pending[uid]["r"]
        custom[t] = r; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ تم حفظه!\n{t} -> {r}\nيشتغل في كل القروبات 🔥")
        return

    if text in ["الغاء", "الغه"]:
        waiting.pop(uid, None); pending.pop(uid, None)
        bot.reply_to(m, "❌ الغاء")
        return

    if text in ["اوامري", "قائمة اوامري"]:
        if not custom:
            bot.reply_to(m, "ما اضفت شي")
            return
        txt = f"📋 اوامرك - ID {uid}:\n\n"
        for k, v in custom.items():
            txt += f"• {k} -> {v}\n"
        bot.reply_to(m, txt)
        return

    if text.startswith("احذف امر:") or text.startswith("احذف امر "):
        t = text.replace("احذف امر:", "").replace("احذف امر", "").strip()
        if t in custom:
            del custom[t]; save_custom()
            bot.reply_to(m, f"✅ حذف {t}")
        else:
            bot.reply_to(m, f"ما لقيت {t}")
        return

    if text in ["/start", "start"]:
        bot.reply_to(m, f"""اهلا - ايديك {uid} ✅

الاوامر اللي تقيّد صدق:

• تقييد - بالرد على الشخص يقيده + يرد باسم
• فك التقييد - يفك عنه

طريقة اضافة اوامر جديدة (انت تعطي الامر والرد):

1️⃣ اضف امر: تقييد
[يطلب الرد]
2️⃣ - المستخدم ذا {{فلان}} قيده
3️⃣ ارفعه

او:
اضف امر: تقييد -> - المستخدم ذا {{فلان}} قيده

{{فلان}} يصير اسم الشخص تلقائي ✅
""")
        return

@bot.message_handler(content_types=['text'])
def groups(m):
    if m.chat.type == 'private':
        return
    text = (m.text or "").strip()
    chat_id = m.chat.id

    # امر تقييد حقيقي
    if text in ["تقييد", "تقييدد", "قيد"]:
        if not m.reply_to_message:
            bot.reply_to(m, "❌ رد على رسالة الشخص اللي تبي تقيده")
            return
        target_user = m.reply_to_message.from_user
        target_id = target_user.id
        target_name = target_user.first_name or "الشخص"
        try:
            # تقييد حقيقي - يمنع الكتابة
            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=target_id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            # رد باسم الشخص
            if text in custom and "تقييد" in custom:
                # اذا عندك رد مخصص للتقييد
                template = custom["تقييد"]
                reply_text, _, _ = format_reply(template, m)
                bot.reply_to(m, reply_text)
            else:
                bot.reply_to(m, f"• المستخدم ذا {target_name} قيده 🔒")
        except Exception as e:
            bot.reply_to(m, f"ما قدرت اقيده - لازم البوت مشرف وعنده صلاحية حظر\n{e}")
        return

    if text in ["فك التقييد", "فك تقييد", "الغاء التقييد", "الغاء تقييد"]:
        if not m.reply_to_message:
            bot.reply_to(m, "❌ رد على رسالة الشخص")
            return
        target_id = m.reply_to_message.from_user.id
        target_name = m.reply_to_message.from_user.first_name or "الشخص"
        try:
            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=target_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            bot.reply_to(m, f"• المستخدم ذا {target_name} فكينا قيده ✅")
        except Exception as e:
            bot.reply_to(m, f"ما قدرت افك قيده\n{e}")
        return

    # الاوامر المخصصة اللي انت ضفتها
    if text in custom:
        # اذا كان الامر هو تقييد - لا تكرر - سوينا فوق
        if text in ["تقييد", "تقييدد", "قيد"]:
            return
        template = custom[text]
        reply_text, _, _ = format_reply(template, m)
        bot.reply_to(m, reply_text)

print("="*50)
print(f"✅ READY - REAL RESTRICT ID {OWNER_BOT_ID}")
print("✅ تقييد حقيقي + يغير الاسم تلقائي")
print("✅ بدون A_TOOLSx2")
print("="*50)

while True:
    try:
        print("✅ Starting polling...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True, none_stop=True)
    except Exception as e:
        err = str(e)
        if "409" in err or "Conflict" in err:
            print("⚠️ 409 - انتظار 10 ث...")
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
