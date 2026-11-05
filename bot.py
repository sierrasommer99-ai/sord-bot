# -*- coding: utf-8 -*-
# FIX 409 CONFLICT - يحذف الويب هوك ويحل مشكلة مكانين

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - 409 FIXED", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, re, requests

BOT_TOKEN = "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)  # threaded=False يحل Conflict
OWNER_BOT_ID = 123456789

print("=== حل مشكلة 409 Conflict ===")

# 1. احذف الويب هوك + احذف التحديثات المعلقة
try:
    print("🔧 حذف Webhook...")
    bot.remove_webhook()
    time.sleep(1)
    # حذف مباشر عبر API
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
    print("✅ Webhook تم حذفه + drop_pending_updates=True")
    time.sleep(2)
except Exception as e:
    print(f"Webhook error (عادي): {e}")

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
    if m.reply_to_message:
        name=m.reply_to_message.from_user.first_name or "الشخص"
    else:
        name=m.from_user.first_name or "الشخص"
    return template.replace("{الاسم}",name).replace("{فلان}",name).replace("{name}",name)

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
        bot.send_message(m.chat.id, "اكتب: ارفعه")
        return

    if text.startswith("اضف امر:") and "->" not in text:
        cmd = text.replace("اضف امر:","").strip()
        if not cmd:
            bot.reply_to(m, "اكتب: اضف امر: تقييد")
            return
        waiting[uid] = {"step": "wait_reply", "command": cmd}
        bot.reply_to(m, f"تمام - الأمر: {cmd}\n\nالحين ارسل وش تبي البوت يرد؟")
        return

    if (text.startswith("اضف امر:") or text.startswith("جرب امر:")) and "->" in text:
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
            bot.reply_to(m, "ما فيه امر - اضف امر: تقييد")
            return
        t=pending[uid]["t"]; r=pending[uid]["r"]
        custom[t]=r; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ تم حفظه!\n{t} -> {r}\nيشتغل في كل القروبات 🔥")
        return

    if text in ["الغاء","الغه"]:
        waiting.pop(uid,None)
        pending.pop(uid,None)
        bot.reply_to(m, "❌ الغاء")
        return

    if text in ["اوامري"]:
        if not custom:
            bot.reply_to(m, "ما اضفت شي")
            return
        txt="📋 اوامرك:\n\n"
        for k,v in custom.items():
            txt+=f"• {k} -> {v}\n"
        bot.reply_to(m, txt)
        return

    if text.startswith("احذف امر:"):
        t=text.replace("احذف امر:","").strip()
        if t in custom:
            del custom[t]; save_custom()
            bot.reply_to(m, f"✅ حذف {t}")
        return

@bot.message_handler(content_types=['text'])
def groups(m):
    if m.chat.type == 'private':
        return
    text=(m.text or "").strip()
    if text in custom:
        bot.reply_to(m, format_reply(custom[text], m))

print("="*50)
print("✅ FIXED 409 - threaded=False + remove_webhook")
print("✅ انت تعطي الامر + تعطي الرد")
print("="*50)

# Polling مع حماية 409
while True:
    try:
        print("✅ Starting polling with 409 fix...")
        # infinity_polling بدون threading
        bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True, none_stop=True)
    except Exception as e:
        err = str(e)
        if "409" in err or "Conflict" in err:
            print(f"⚠️ 409 Conflict detected - انتظار 10 ثواني واعادة المحاولة...")
            print("تأكد انك مو مشغل البوت في مكان ثاني (VS Code, Termux, لابتوب)")
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
