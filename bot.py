import os, json
# حذف فوري - قبل كل شي
for p in ["/data/custom_commands.json","/opt/render/project/src/custom_commands.json","./custom_commands.json","custom_commands.json"]:
    try:
        if os.path.exists(p):
            os.remove(p)
            print(f"DELETED {p}")
    except: pass
# انشئ ملف فاضي نظيف
for p in ["/data/custom_commands.json"]:
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p,'w',encoding='utf-8') as f:
            json.dump({}, f)
    except: pass

from flask import Flask
import threading
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "OK ZERO CHANNEL", 200
@flask_app.route('/health')
def health(): return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, time, requests, html, re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
OWNER_BOT_ID = 829238313

try:
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
except: pass

BASE_DIR = "/data" if os.path.exists("/data") else "."
def get_path(n): return os.path.join(BASE_DIR, n)

FILE = get_path('custom_commands.json')
LOCK_FILE = get_path('locked_commands.json')
RANKS_FILE = get_path('user_ranks.json')
TOP_FILE = get_path('top.json')

custom = {}
user_ranks = {}
top_data = {}

def load_all():
    global custom, user_ranks, top_data
    for fp, dct in [(FILE, custom),(RANKS_FILE, user_ranks),(TOP_FILE, top_data)]:
        try:
            if os.path.exists(fp):
                with open(fp,'r',encoding='utf-8') as f:
                    data=json.load(f)
                    if isinstance(data, dict):
                        dct.clear()
                        dct.update(data)
        except: pass

load_all()

def save_json(p,d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p,'w',encoding='utf-8') as f:
        json.dump(d,f,ensure_ascii=False,indent=2)
def save_custom(): save_json(FILE, custom)
def save_ranks(): save_json(RANKS_FILE, user_ranks)
def save_top(): save_json(TOP_FILE, top_data)

RANK_ORDER = {"مميز":1,"ادمن":2,"مدير":3,"منشئ":4,"منشئ اساسي":5,"مالك":6,"مالك اساسي":7,"مالك المجموعه":8,"M":9,"MY":10,"Dev2":11,"Dev":12}

def get_rank(uid,cid):
    if uid==OWNER_BOT_ID: return "Dev"
    cs=str(cid); us=str(uid)
    if cs in user_ranks and us in user_ranks[cs]: return user_ranks[cs][us]
    return "عضو"
def get_rank_badge(uid,cid):
    r=get_rank(uid,cid)
    return f"{r} 🎖️" if RANK_ORDER.get(r,0)>=10 or uid==OWNER_BOT_ID else r
def add_count(cid,uid,name):
    cs=str(cid); us=str(uid)
    if cs not in top_data: top_data[cs]={}
    if us not in top_data[cs]: top_data[cs][us]={"count":0,"name":name}
    top_data[cs][us]["count"]+=1
    top_data[cs][us]["name"]=name
    save_top()
def get_stats(cid,uid):
    cs=str(cid); us=str(uid)
    if cs not in top_data: return 0,0
    s=sorted(top_data[cs].items(),key=lambda x:x[1]["count"],reverse=True)
    cnt=top_data[cs].get(us,{}).get("count",0)
    pos=0
    for i,(u,d) in enumerate(s,1):
        if u==us: pos=i; break
    if pos==0: pos=1
    return cnt,pos

def smart_replace(text, name, rank_badge, count, pos):
    if not text: return text
    text = re.sub(r"「\s*」", f"「 {name} 」", text)
    text = text.replace("{الاسم}", name).replace("{فلان}", name)
    text = text.replace("{الرتبة}", rank_badge).replace("الرتبة", rank_badge)
    text = text.replace("{التفاعل}", str(count)).replace("التفاعل", str(count))
    for w in ["{الترتيب}","{الرتيب}","الرتيب","الترتيب"]:
        text = text.replace(w, str(pos))
    return text

def get_private_menu():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("➕ اضف امر", callback_data="p_add"),InlineKeyboardButton("➖ احذف امر", callback_data="p_del"))
    m.add(InlineKeyboardButton("📜 اوامري", callback_data="p_my"),InlineKeyboardButton("🧹 حذف الكل", callback_data="p_wipe"))
    m.add(InlineKeyboardButton("• إغلاق •", callback_data="close"))
    return m
def get_main_menu():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("التفعيل والتعطيل", callback_data="t1"),InlineKeyboardButton("القفل والفتح", callback_data="t2"))
    m.add(InlineKeyboardButton("التسلية والخدمية", callback_data="t3"),InlineKeyboardButton("ادارة القروب", callback_data="t4"))
    m.add(InlineKeyboardButton("• إغلاق •", callback_data="close"))
    return m

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    try:
        if c.data=="close":
            try: bot.delete_message(c.message.chat.id,c.message.message_id)
            except: pass
            return
        if c.data=="p_wipe":
            custom.clear()
            save_custom()
            bot.edit_message_text("🧹 تم حذف كل الاوامر - نظيف ✅\n\nالحين /start و رتبتي مستحيل يطلعون قناة", c.message.chat.id, c.message.message_id)
            return
        if c.data=="p_my":
            txt = "\n".join([f"• {k}" for k in custom.keys()]) if custom else "فاضي - نظيف ✅"
            bot.edit_message_text(f"اوامرك:\n{txt}", c.message.chat.id, c.message.message_id)
            return
        if c.data in ["t1","t2","t3","t4","p_add","p_del"]:
            bot.edit_message_text("القائمة - ارسل اضف امر رتبتي", c.message.chat.id, c.message.message_id)
            return
    except: pass

waiting={}
pending={}

@bot.message_handler(chat_types=['private'],content_types=['text'])
def priv(m):
    if m.from_user.id!=OWNER_BOT_ID: return
    txt=m.text.strip()

    # /start - ثابت نظيف بالقوة - لا يقرا من custom ابدا
    if txt in ["/start","start","الاوامر","اوامري","القائمة"]:
        # احذف اي /start فاسد لو موجود
        if "/start" in custom or "start" in custom:
            for k in ["/start","start","مسح كل الاوامر"]:
                if k in custom:
                    del custom[k]
            save_custom()
        bot.send_message(m.chat.id, f"👋 اهلا {m.from_user.first_name} ²⁷\n\n✅ ZERO CHANNEL - نظيف 100%\n\n• اوامرك: {len(custom)}\n• /start: ثابت نظيف\n• رتبتي: {'موجود' if 'رتبتي' in custom else 'مو موجود'}\n\nاذا تبي تضيف رتبتي:\nاضف امر رتبتي -> شكلك", reply_markup=get_private_menu())
        return

    if txt in ["نظف","مسح كل الاوامر","تنظيف","امسح كل شي"]:
        custom.clear()
        save_custom()
        for p in [FILE, "/data/custom_commands.json","/opt/render/project/src/custom_commands.json"]:
            try:
                if os.path.exists(p):
                    os.remove(p)
                    with open(p,'w',encoding='utf-8') as f:
                        json.dump({}, f)
            except: pass
        bot.reply_to(m, "🧹 تم حذف كل شي ✅\n\nالحين /start نظيف 100%\n• اضف رتبتي من جديد")
        return

    if txt.startswith("اضف امر"):
        tmp=txt.replace("اضف امر:","").replace("اضف امر","").strip()
        if "->" in tmp:
            a,b=tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if "t.me" in resp or "Tucos" in resp or "A_Tools" in resp or "To use this bot" in resp:
                bot.reply_to(m, "❌ فيه قناة - ممنوع"); return
            pending[m.from_user.id]={"t":trig,"text":resp}
            bot.reply_to(m, f"تمام - الامر: {trig}\nاكتب: ارفعه")
            return
        else:
            waiting[m.from_user.id]=tmp
            bot.reply_to(m, f"تمام - الامر: {tmp}\nارسل الشكل (مثال: ≡ رتبتك هي ← الرتبة)")
            return

    if m.from_user.id in waiting:
        cmd=waiting[m.from_user.id]
        if "t.me" in m.text or "Tucos" in m.text or "A_Tools" in m.text or "To use this bot" in m.text:
            bot.reply_to(m, "❌ فيه قناة - ممنوع"); return
        pending[m.from_user.id]={"t":cmd,"text":m.text}
        del waiting[m.from_user.id]
        bot.reply_to(m, "تمام - محفوظ\nاكتب: ارفعه")
        return

    if txt in ["ارفعه","احفظه"]:
        if m.from_user.id not in pending: return
        t=pending[m.from_user.id]["t"]
        tx=pending[m.from_user.id]["text"]
        custom[t]={"text":tx}
        save_custom()
        del pending[m.from_user.id]
        bot.reply_to(m, f"✅ حفظت {t} - بنفس شكلك ✅")
        return

    if txt.startswith("احذف امر"):
        cmd=txt.replace("احذف امر:","").replace("احذف امر","").strip()
        if cmd in custom:
            del custom[cmd]
            save_custom()
            bot.reply_to(m, f"✅ حذفت {cmd}")
        else:
            bot.reply_to(m, f"✅ نظفت {cmd} (مو موجود اصلا - نظيف)")
        return

@bot.message_handler(content_types=['text'])
def grp(m):
    if m.chat.type=='private': return
    text=(m.text or "").strip()
    chat_id=m.chat.id
    uid=m.from_user.id
    name=m.from_user.first_name or "شخص"
    add_count(chat_id,uid,name)

    # ===== اولوية قصوى - اوامر ثابتة نظيفة - لا تقرا من custom =====
    if text in ["/start","start","الاوامر","اوامر","قائمة الاوامر"]:
        # حتى لو /start موجود في custom - تجاهله
        bot.send_message(chat_id, "قائمة الاوامر", reply_markup=get_main_menu(), reply_to_message_id=m.message_id)
        return

    if text in ["رتبتي","رتبتي ²⁷"]:
        # اذا فيه مخصص نظيف - استخدمه
        if "رتبتي" in custom:
            raw=custom["رتبتي"].get("text","") if isinstance(custom["رتبتي"],dict) else ""
            if "Tucos" not in raw and "A_Tools" not in raw and "To use this bot" not in raw:
                badge=get_rank_badge(uid,chat_id)
                cnt,pos=get_stats(chat_id,uid)
                final=smart_replace(raw, name, badge, cnt, pos)
                bot.send_message(chat_id, final, reply_to_message_id=m.message_id)
                return
        # افتراضي نظيف
        badge=get_rank_badge(uid,chat_id)
        cnt,pos=get_stats(chat_id,uid)
        bot.send_message(chat_id, f"≡ رتبتك هي ← {badge}\n≡ رسائلك ← {cnt}\n≡ ترتيبك ← {pos}\n-", reply_to_message_id=m.message_id)
        return

    # باقي الاوامر المخصصة
    if text in custom:
        raw=custom[text].get("text","") if isinstance(custom[text],dict) else ""
        if "Tucos" in raw or "A_Tools" in raw or "To use this bot" in raw:
            del custom[text]
            save_custom()
            return
        badge=get_rank_badge(uid,chat_id)
        cnt,pos=get_stats(chat_id,uid)
        final=smart_replace(raw, name, badge, cnt, pos)
        bot.send_message(chat_id, final, reply_to_message_id=m.message_id)

print("READY ZERO CHANNEL - NO Tucos NO A_ToolsX")

while True:
    try:
        bot.infinity_polling(timeout=60,long_polling_timeout=60,skip_pending=True)
    except Exception as e:
        print(e)
        time.sleep(5)
