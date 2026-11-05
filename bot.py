# -*- coding: utf-8 -*-
# ملف فيه بس نظام الرفع التلقائي من الخاص + التوكن
# ما فيه اي اوامر ثانية

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - UPLOAD ONLY MODE", 200
@flask_app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"Flask on {port}")
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

threading.Thread(target=run_flask, daemon=True).start()

import telebot
import json, re, time

# التوكن مربوط بمكانه
BOT_TOKEN = "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"
bot = telebot.TeleBot(BOT_TOKEN)
OWNER_BOT_ID = 123456789  # <--- غيره لايديك

print(f"Token: {BOT_TOKEN[:15]}... READY - UPLOAD ONLY MODE")

custom = {}
FILE = 'custom_commands.json'
try:
    with open(FILE,'r',encoding='utf-8') as f:
        custom = json.load(f)
except:
    custom = {}

def save_custom():
    with open(FILE,'w',encoding='utf-8') as f:
        json.dump(custom, f, ensure_ascii=False, indent=2)

pending = {}

# خاص البوت - نظام الرفع التلقائي فقط
@bot.message_handler(chat_types=['private'], func=lambda m: m.from_user.id == OWNER_BOT_ID)
def private_lab(m):
    text = m.text.strip()
    uid = m.from_user.id

    # جرب امر: هلا -> هلا والله
    if text.startswith("جرب امر:") or text.startswith("جرب:"):
        cmd = text.replace("جرب امر:","").replace("جرب:","").strip()
        if "->" in cmd:
            a,b = cmd.split("->",1)
            trig=a.strip(); resp=b.strip()
        else:
            mat=re.search(r'["\'](.+?)["\'].*["\'](.+?)["\']', cmd)
            if mat:
                trig=mat.group(1).strip(); resp=mat.group(2).strip()
            else:
                bot.reply_to(m, "الصيغة:\nجرب امر: هلا -> هلا والله")
                return
        pending[uid]={"t":trig,"r":resp}
        bot.reply_to(m, f"🧪 تجربة:\n{trig}\n---\n{resp}\n---\nعجبك؟ اكتب: ارفعه")
        bot.send_message(m.chat.id, resp)
        return

    # ارفعه للسيرفر
    if text in ["ارفعه","ارفعه للسيرفر"]:
        if uid not in pending:
            bot.reply_to(m, "ما فيه امر مجرب")
            return
        t=pending[uid]["t"]; r=pending[uid]["r"]
        custom[t]=r; save_custom(); del pending[uid]
        bot.reply_to(m, f"✅ تم رفعه للسيرفر!\n{t} -> {r}")
        return

    # الغاء
    if text in ["الغه","الغاء"]:
        if uid in pending:
            del pending[uid]
            bot.reply_to(m, "❌ الغاء")
        return

    # اوامري
    if text in ["اوامري","قائمة اوامري","اوامري المرفوعه"]:
        if not custom:
            bot.reply_to(m, "ما رفعت شي بعد")
            return
        txt="📋 اوامرك المرفوعه:\n\n"
        for k,v in custom.items():
            txt+=f"• {k} -> {v}\n"
        bot.reply_to(m, txt)
        return

    # حذف امر
    if text.startswith("احذف امر:"):
        t=text.replace("احذف امر:","").strip()
        if t in custom:
            del custom[t]; save_custom()
            bot.reply_to(m, f"✅ حذف {t}")
        else:
            bot.reply_to(m, f"ما لقيت {t}")
        return

# القروبات - بس الاوامر اللي رفعتها من الخاص
@bot.message_handler(content_types=['text'])
def groups_only(m):
    if m.chat.type == 'private':
        return
    text=(m.text or "").strip()
    if text in custom:
        bot.reply_to(m, custom[text])

print("="*40)
print("✅ UPLOAD ONLY MODE - فيه التوكن")
print(f"✅ {BOT_TOKEN}")
print("✅ بس نظام الرفع من الخاص")
print("✅ لا يوجد اي اوامر ثانية")
print("="*40)

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(e)
        time.sleep(5)
