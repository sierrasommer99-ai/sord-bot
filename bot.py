
import os
import telebot
import json
import threading
from flask import Flask

# ===== TOKEN - مباشر بدون ENV عشان يشتغل 100% =====
BOT_TOKEN = "8769832522:AAHmQBlu9xZTw-WWks17nHNrvgT8D4YXkNY"
OWNER_ID = 829238313

print(f"TOKEN loaded: {BOT_TOKEN[:15]}...")
print("Clean file created")

# ===== BOT =====
bot = telebot.TeleBot(BOT_TOKEN, threaded=True, num_threads=2)

# ===== Flask للـ Render =====
app = Flask(__name__)

@app.route('/')
def home():
    return f'Bot Running - @{bot.get_me().username if hasattr(bot, "get_me") else "SRDT"}'

@app.route('/health')
def health():
    return 'OK'

# ===== DATA FOLDER =====
DATA_DIR = "/data" if os.path.exists("/data") else "."
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(name, default):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False)
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default

def save_json(name, data):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== تنظيف ملف الاوامر الملوث =====
custom_file = os.path.join(DATA_DIR, "custom_commands.json")
if os.path.exists(custom_file):
    try:
        with open(custom_file, 'r', encoding='utf-8') as f:
            d = json.load(f)
        bad = False
        for k,v in list(d.items()):
            txt = str(v).lower()
            if "a_tools" in txt or "a_toolsx" in txt or "t.me/a_tools" in txt or "join our channel" in txt.lower() or "tucosprofit" in txt.lower():
                del d[k]
                bad = True
        if bad:
            save_json("custom_commands.json", d)
            print("CLEANED polluted commands")
    except:
        save_json("custom_commands.json", {})
        print("Reset custom_commands.json")

# ===== تحميل =====
custom_commands = load_json("custom_commands.json", {})

# ===== START - يرد على الكل في الخاص =====
@bot.message_handler(commands=['start'])
def start_cmd(m):
    print(f"START from {m.from_user.id} : {m.text}")
    try:
        bot.reply_to(m, f"👋 اهلا ²⁷ محسن\n\n✅ البوت شغال\nID: {m.from_user.id}\n\n📋 الاوامر:\n/start - تشغيل\n/اضف_امر - اضافة امر\n/حذف_امر + الاسم\n/مسح_الكل - مسح الاوامر\n\nDev: @afiwd")
        print("REPLIED to /start")
    except Exception as e:
        print(f"Error in start: {e}")

# ===== خاص - اضافة اوامر =====
@bot.message_handler(func=lambda m: m.chat.type == 'private')
def private_all(m):
    if m.text and m.text.startswith('/start'):
        return # تجاهل لان فوق يعالجه
    
    print(f"PRIVATE {m.from_user.id}: {m.text}")
    
    # فقط المالك يضيف اوامر
    if m.from_user.id != OWNER_ID:
        bot.reply_to(m, "هذا البوت خاص")
        return
    
    txt = (m.text or "").strip()
    
    if txt == "اضف امر" or txt == "/اضف_امر" or txt == "اضف امر ²⁷":
        msg = bot.reply_to(m, "ارسل اسم الامر (مثلا: رتبتي)")
        bot.register_next_step_handler(msg, add_cmd_step1)
        return
    
    if txt.startswith("حذف امر") or txt.startswith("/حذف_امر"):
        parts = txt.split()
        if len(parts) >= 2:
            name = parts[1]
            if name in custom_commands:
                del custom_commands[name]
                save_json("custom_commands.json", custom_commands)
                bot.reply_to(m, f"✅ تم حذف {name}")
            else:
                bot.reply_to(m, "الامر مو موجود")
        else:
            bot.reply_to(m, "اكتب: حذف امر رتبتي")
        return
    
    if txt == "مسح كل الاوامر" or txt == "/مسح_الكل" or txt == "مسح الكل":
        save_json("custom_commands.json", {})
        custom_commands.clear()
        bot.reply_to(m, "✅ تم مسح كل الاوامر الملوثة")
        return
    
    if txt == "سورد" or txt.lower() == "sord":
        bot.reply_to(m, "نعم ²⁷ موجود")
        return
    
    # رد تلقائي للاوامر المخصصة
    if txt in custom_commands:
        try:
            bot.reply_to(m, custom_commands[txt])
        except Exception as e:
            print(f"Error reply custom: {e}")

def add_cmd_step1(m):
    if m.from_user.id != OWNER_ID:
        return
    cmd_name = m.text.strip()
    if not cmd_name:
        return
    msg = bot.reply_to(m, f"تمام - الامر: {cmd_name}\nالحين ارسل الرد (تقدر تستخدم {{الاسم}} {{الرتبة}} {{التفاعل}} {{الترتيب}} {{فلان}})")
    bot.register_next_step_handler(msg, lambda x: add_cmd_step2(x, cmd_name))

def add_cmd_step2(m, cmd_name):
    if m.from_user.id != OWNER_ID:
        return
    reply_text = m.text
    custom_commands[cmd_name] = reply_text
    save_json("custom_commands.json", custom_commands)
    bot.reply_to(m, f"✅ تم حفظ الامر\n{cmd_name} -> {reply_text}")

# ===== مجموعات =====
@bot.message_handler(func=lambda m: m.chat.type in ['group', 'supergroup'])
def groups(m):
    if not m.text:
        return
    txt = m.text.strip()
    # منع الاوامر الملوثة
    if "A_TOOLS" in txt or "A_ToolsX" in txt or "TucosProfit" in txt:
        return
    
    if txt in custom_commands:
        try:
            # تعويض المتغيرات
            name = m.from_user.first_name or "مستخدم"
            reply = custom_commands[txt]
            reply = reply.replace("{الاسم}", name).replace("{فلان}", name).replace("{الرتبة}", "عضو").replace("{التفاعل}", "0").replace("{الترتيب}", "0")
            bot.reply_to(m, reply)
        except Exception as e:
            print(f"Group error: {e}")

# ===== تشغيل =====
def run_bot():
    print("Starting polling...")
    bot.remove_webhook()
    try:
        me = bot.get_me()
        print(f"BOT USERNAME: @{me.username}")
    except Exception as e:
        print(f"getMe error: {e}")
    print("READY FINAL SECURE - NO CHANNEL")
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)

if __name__ == '__main__':
    # Flask في ثريد
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False, use_reloader=False), daemon=True).start()
    run_bot()
