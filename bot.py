# -*- coding: utf-8 -*-
"""
SRDT - ملف الرفع التلقائي لحاله
================================
تجرب الاوامر في خاص البوت والبوت يرفعها للسيرفر تلقائي

فقط: جرب امر: X -> Y  ثم ارفعه
"""

import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "<h1>SRDT - الرفع التلقائي</h1>"
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, re
BOT_TOKEN = "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"
bot = telebot.TeleBot(BOT_TOKEN)
OWNER_BOT_ID = 123456789

pending = {}
custom = {}
FILE = 'custom_commands.json'
try:
    with open(FILE,'r',encoding='utf-8') as f:
        custom = json.load(f)
except:
    custom = {}

def save():
    with open(FILE,'w',encoding='utf-8') as f:
        json.dump(custom,f,ensure_ascii=False,indent=2)

@bot.message_handler(chat_types=['private'], func=lambda m: m.from_user.id == OWNER_BOT_ID)
def lab(m):
    text = m.text.strip()
    uid = m.from_user.id
    
    if text.startswith("جرب امر:") or text.startswith("جرب:"):
        cmd = text.replace("جرب امر:","").replace("جرب:","").strip()
        # يدعم: هلا -> هلا والله  او  اذا كتب "هلا" يرد "هلا"
        if "->" in cmd:
            a,b = cmd.split("->",1)
            trig = a.strip()
            resp = b.strip()
        else:
            mat = re.search(r'["\'](.+?)["\'].*["\'](.+?)["\']', cmd)
            if mat:
                trig = mat.group(1).strip()
                resp = mat.group(2).strip()
            else:
                bot.reply_to(m, "الصيغة:\nجرب امر: هلا -> هلا والله")
                return
        
        pending[uid] = {"t":trig,"r":resp}
        bot.reply_to(m, f"🧪 تجربة:\n\nاذا كتب: {trig}\nيرد: {resp}\n\n---\nتجربة فعلية:\n{trig}")
        bot.send_message(m.chat.id, resp)
        bot.send_message(m.chat.id, "---\nعجبك؟ اكتب: ارفعه\nاو: الغه")
        return
    
    if text in ["ارفعه","ارفعه للسيرفر"]:
        if uid not in pending:
            bot.reply_to(m, "ما فيه امر - جرب:\nجرب امر: هلا -> هلا والله")
            return
        t = pending[uid]["t"]
        r = pending[uid]["r"]
        custom[t] = r
        save()
        del pending[uid]
        bot.reply_to(m, f"✅ تم رفعه للسيرفر تلقائي!\n\n{t} -> {r}\n\nالحين يشتغل في كل القروبات 🔥")
        return
    
    if text in ["الغه","الغاء"]:
        if uid in pending:
            del pending[uid]
            bot.reply_to(m, "❌ تم الغاء")
        return
    
    if text in ["اوامري","قائمة اوامري"]:
        if not custom:
            bot.reply_to(m, "ما رفعت شي بعد")
            return
        txt = "📋 اوامرك المرفوعة للسيرفر:\n\n"
        for k,v in custom.items():
            txt+=f"• {k} -> {v}\n"
        bot.reply_to(m, txt)
        return
    
    if text.startswith("احذف امر:"):
        t = text.replace("احذف امر:","").strip()
        if t in custom:
            del custom[t]
            save()
            bot.reply_to(m, f"✅ حذف {t} من السيرفر")
        else:
            bot.reply_to(m, f"ما لقيت {t}")
        return
    
    if text in ["مساعدة","خاص","اوامر الخاص"]:
        bot.reply_to(m, """
🧪 الرفع التلقائي - خاص البوت:

جرب امر: هلا -> هلا والله
ارفعه → يرفعه للسيرفر تلقائي
اوامري → عرض المرفوع
احذف امر: هلا → حذف من السيرفر
""")
        return

@bot.message_handler(func=lambda m: True, content_types=['text'])
def all_groups(m):
    text = (m.text or "").strip()
    if m.chat.type == 'private':
        return
    if text in custom:
        bot.reply_to(m, custom[text])

print("✅ ملف الرفع التلقائي لحاله - شغال")
print("✅ خاص البوت: جرب امر: هلا -> هلا والله ثم ارفعه")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"خطأ {e}")
        time.sleep(5)
