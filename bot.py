# -*- coding: utf-8 -*-
# الملف النهائي - ايديك 829238313 + التوكن + اضف امر ورد + حل 409

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - 829238313 READY", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask on {port}")
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, requests

BOT_TOKEN = "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
OWNER_BOT_ID = 829238313  # ايديك - جاهز

print(f"=== READY ID {OWNER_BOT_ID} ===")

try:
    print("🔧 حذف Webhook...")
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
    print("✅ Webhook محذوف")
    time.sleep(1)
except Exception as e:
    print(f"Webhook: {e}")

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

def format_reply(template, m):
    name="الشخص"
    username=""
    if m.reply_to_message:
        u=m.reply_to_message.from_user
        name=u.first_name or "الشخص"
        username=f"@{u.username}" if u.username else name
    else:
        u=m.from_user
        name=u.first_name or "الشخص"
        username=f"@{u.username}" if u.username else name
    res=template
    res=res.replace("{الاسم}",name).replace("{فلان}",name).replace("{name}",name)
    res=res.replace("{المعرف}",username).replace("{username}",username)
    return res

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
        bot.send_message(m.chat.id, format_reply(reply_text, m))
        bot.send_message(m.chat.id, "عجبك؟ اكتب: ارفعه\nما عجبك؟ الغاء")
        return

    if text.startswith("اضف امر:") and "->" not in text:
        cmd = text.replace("اضف امر:","").strip()
        if not cmd:
            bot.reply_to(m, "اكتب: اضف امر: تقييد")
            return
        waiting[uid] = {"step": "wait_reply", "command": cmd}
        bot.reply_to(m, f"تمام - الأمر: {cmd}\n\nالحين ارسل لي وش تبي البوت يرد؟\nمثال: تم تقييددد {cmd} 🔒")
        return

    if (text.startswith("اضف امر:") or text.startswith("جرب امر:") or text.startswith("اضف:") or text.startswith("جرب:")) and "->" in text:
        tmp = text
        for p in ["اضف امر:","جرب امر:","اضف:","جرب:"]:
            tmp = tmp.replace(p,"")
        tmp=tmp.strip()
        if "->" in tmp:
            a,b = tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            pending[uid]={"t":trig,"r":resp}
            bot.reply_to(m, f"تمام ✅\nالأمر: {trig}\nالرد: {resp}\n\nتجربة:")
            bot.send_message(m.chat.id, format_reply(resp, m))
            bot.send_message(m.chat.id, "اكتب: ارفعه")
            return

    if text in ["ارفعه","ارفعه للسيرفر","احفظه"]:
        if uid not in pending:
            bot.reply_to(m, "ما فيه امر - اكتب: اضف امر: تقييد")
            return
        t=pending[uid]["t"]; r=pending[uid]["r"]
        custom[t]=r; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ تم حفظه!\n\nالأمر: {t}\nالرد: {r}\n\nيشتغل في كل القروبات 🔥")
        return

    if text in ["الغاء","الغه"]:
        waiting.pop(uid,None)
        pending.pop(uid,None)
        bot.reply_to(m, "❌ الغاء")
        return

    if text in ["اوامري","قائمة اوامري","اوامري المرفوعه"]:
        if not custom:
            bot.reply_to(m, "ما اضفت شي بعد")
            return
        txt=f"📋 اوامرك - ID {uid}:\n\n"
        for k,v in custom.items():
            txt+=f"• {k} -> {v}\n"
        bot.reply_to(m, txt)
        return

    if text.startswith("احذف امر:"):
        t=text.replace("احذف امر:","").strip()
        if t in custom:
            del custom[t]; save_custom()
            bot.reply_to(m, f"✅ حذف {t}")
        else:
            bot.reply_to(m, f"ما لقيت {t}")
        return

    if text in ["/start","start"]:
        bot.reply_to(m, f"""اهلا - ايديك {uid} ✅

طريقة الاضافة (انت تعطي الامر والرد):

1️⃣ اضف امر: تقييد
[البوت يطلب الرد]
2️⃣ تم تقييددد {{فلان}} 🔒
3️⃣ ارفعه

او بسطر واحد:
اضف امر: تقييد -> تم تقييد {{فلان}} 🔒

اوامري - عرض اللي اضفته
احذف امر: تقييد - حذف
""")
        return

@bot.message_handler(content_types=['text'])
def groups(m):
    if m.chat.type == 'private':
        return
    text=(m.text or "").strip()
    if text in custom:
        bot.reply_to(m, format_reply(custom[text], m))

print("="*50)
print(f"✅ READY - ID {OWNER_BOT_ID}")
print(f"✅ TOKEN {BOT_TOKEN[:20]}...")
print("✅ انت تعطي الامر + تعطي الرد")
print("✅ 409 FIXED")
print("="*50)

while True:
    try:
        print("✅ Starting polling...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True, none_stop=True)
    except Exception as e:
        err=str(e)
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
