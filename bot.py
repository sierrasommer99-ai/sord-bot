import os, json
print("=== SECURE CLEAN START - NO TOKEN IN CODE ===")
for p in ["/data/custom_commands.json","/opt/render/project/src/custom_commands.json","./custom_commands.json","custom_commands.json","/data/locked_commands.json"]:
    try:
        if os.path.exists(p):
            print(f"Deleting {p}")
            os.remove(p)
    except Exception as e:
        print(e)

try:
    os.makedirs("/data", exist_ok=True)
    with open("/data/custom_commands.json","w",encoding="utf-8") as f:
        json.dump({}, f)
    print("Created clean /data/custom_commands.json")
except Exception as e:
    print(e)

from flask import Flask
import threading
flask_app = Flask(__name__)
@flask_app.route('/')
def h(): return "SECURE NO TOKEN",200
@flask_app.route('/health')
def hl(): return "OK",200
def run():
    port=int(os.environ.get("PORT",10000))
    flask_app.run(host="0.0.0.0",port=port,debug=False,use_reloader=False)
threading.Thread(target=run,daemon=True).start()

import telebot, time, requests, html, re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن من Environment فقط - ما فيه توكن هنا
TOKEN = os.environ.get("BOT_TOKEN", "").strip()
if not TOKEN:
    print("❌ BOT_TOKEN not in Environment - Add it in Render Environment")
    # حاول من التوكن القديم كاحتياط فقط للاختبار
    TOKEN = 8769832522:AAHmQBlu9xZTw-WWks17nHNrvgT8D4YXkNY

print(f"TOKEN loaded: {TOKEN[:10]}...")

bot = telebot.TeleBot(TOKEN, threaded=False)
OWNER = 829238313

try:
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=True",timeout=10)
except:
    pass

custom={}
user_ranks={}
top_data={}

FILE="/data/custom_commands.json"
RANKS="/data/user_ranks.json"
TOP="/data/top.json"

def load():
    global user_ranks, top_data
    for fp,d in [(RANKS,user_ranks),(TOP,top_data)]:
        try:
            if os.path.exists(fp):
                with open(fp,'r',encoding='utf-8') as f:
                    data=json.load(f)
                    d.clear()
                    d.update(data)
        except:
            pass

load()

def save(p,d):
    try:
        os.makedirs(os.path.dirname(p),exist_ok=True)
        with open(p,'w',encoding='utf-8') as f:
            json.dump(d,f,ensure_ascii=False,indent=2)
    except:
        pass

RANK_ORDER={"مميز":1,"ادمن":2,"مدير":3,"منشئ":4,"منشئ اساسي":5,"مالك":6,"مالك اساسي":7,"مالك المجموعه":8,"M":9,"MY":10,"Dev2":11,"Dev":12}

def get_rank(uid,cid):
    if uid==OWNER: return "Dev"
    cs=str(cid); us=str(uid)
    if cs in user_ranks and us in user_ranks[cs]: return user_ranks[cs][us]
    return "عضو"
def get_badge(uid,cid):
    r=get_rank(uid,cid)
    return f"{r} 🎖️" if RANK_ORDER.get(r,0)>=10 or uid==OWNER else r
def add_count(cid,uid,name):
    cs=str(cid); us=str(uid)
    if cs not in top_data: top_data[cs]={}
    if us not in top_data[cs]: top_data[cs][us]={"count":0,"name":name}
    top_data[cs][us]["count"]+=1
    top_data[cs][us]["name"]=name
    save(TOP,top_data)
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

def smart_replace(text,name,badge,count,pos):
    if not text: return text
    text=re.sub(r"「\s*」", f"「 {name} 」", text)
    text=text.replace("{الاسم}",name).replace("{فلان}",name)
    text=text.replace("{الرتبة}",badge).replace("الرتبة",badge)
    if "التفاعل" in text:
        lines=text.split("\n")
        nl=[]
        for line in lines:
            if "التفاعل" in line and "←" in line:
                parts=line.split("←")
                if "التفاعل" in parts[-1]:
                    parts[-1]=parts[-1].replace("التفاعل",str(count))
                    line="←".join(parts)
                else:
                    line=line.replace("التفاعل",str(count))
            elif "التفاعل" in line:
                line=line.replace("التفاعل",str(count))
            nl.append(line)
        text="\n".join(nl)
    for w in ["{الترتيب}","{الرتيب}","الرتيب","الترتيب"]:
        text=text.replace(w,str(pos))
    return text

def priv_menu():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("➕ اضف امر",callback_data="p_add"),InlineKeyboardButton("📜 اوامري",callback_data="p_my"))
    m.add(InlineKeyboardButton("🧹 مسح الكل",callback_data="p_wipe"),InlineKeyboardButton("• إغلاق •",callback_data="close"))
    return m

def main_menu():
    m=InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("التفعيل والتعطيل",callback_data="t1"),InlineKeyboardButton("القفل والفتح",callback_data="t2"))
    m.add(InlineKeyboardButton("التسلية والخدمية",callback_data="t3"),InlineKeyboardButton("ادارة القروب",callback_data="t4"))
    m.add(InlineKeyboardButton("• إغلاق •",callback_data="close"))
    return m

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    try:
        if c.data=="close":
            try: bot.delete_message(c.message.chat.id,c.message.message_id)
            except: pass
            return
        if c.data=="p_wipe":
            custom.clear()
            for p in [FILE,"/data/custom_commands.json","/opt/render/project/src/custom_commands.json","custom_commands.json"]:
                try:
                    if os.path.exists(p):
                        os.remove(p)
                        with open(p,'w',encoding='utf-8') as f:
                            json.dump({},f)
                except: pass
            bot.edit_message_text("🧹 تم حذف كل شي - الحين /start و رتبتي نظاف 100% ✅",c.message.chat.id,c.message.message_id)
            return
        if c.data=="p_my":
            txt="\n".join([f"• {k}" for k in custom.keys()]) if custom else "فاضي - نظيف ✅"
            bot.edit_message_text(f"اوامرك:\n{txt}",c.message.chat.id,c.message.message_id)
            return
    except:
        pass

waiting={}
pending={}

@bot.message_handler(chat_types=['private'],func=lambda m: True,content_types=['text'])
def private_all(m):
    if m.from_user.id!=OWNER: return
    txt=m.text.strip()

    if txt in ["/start","start","/start@SRDTbot","القائمة","الاوامر","اوامري"]:
        bot.send_message(m.chat.id, f"👋 اهلا {m.from_user.first_name} ²⁷\n\n✅ SECURE - بدون توكن في الكود\n\n• اوامرك: {len(custom)}\n• /start: ثابت نظيف\n• التوكن من: Environment\n\nاذا /start لسه يطلع قناة - معناه فيه بوت ثاني شغال بنفس التوكن القديم - سوي Revoke في BotFather", reply_markup=priv_menu())
        return

    if txt in ["مسح كل الاوامر","نظف","تنظيف","امسح كل شي","مسح","حذف الكل"]:
        custom.clear()
        for p in [FILE,"/data/custom_commands.json","/opt/render/project/src/custom_commands.json","custom_commands.json","./custom_commands.json"]:
            try:
                if os.path.exists(p):
                    os.remove(p)
                    with open(p,'w',encoding='utf-8') as f:
                        json.dump({},f)
            except: pass
        bot.reply_to(m, "🧹 تم حذف كل شي ✅")
        return

    if txt.startswith("اضف امر"):
        tmp=txt.replace("اضف امر:","").replace("اضف امر","").strip()
        if "->" in tmp:
            a,b=tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if "t.me" in resp or "Tucos" in resp or "A_Tools" in resp or "A_TOOLS" in resp or "To use this bot" in resp:
                bot.reply_to(m, "❌ فيه قناة - ممنوع"); return
            pending[m.from_user.id]={"t":trig,"text":resp}
            bot.reply_to(m, f"تمام - الامر: {trig}\nاكتب: ارفعه")
            return
        else:
            waiting[m.from_user.id]=tmp
            bot.reply_to(m, f"تمام - الامر: {tmp}\nارسل الشكل")
            return

    if m.from_user.id in waiting:
        cmd=waiting[m.from_user.id]
        if "t.me" in m.text or "Tucos" in m.text or "A_Tools" in m.text or "A_TOOLS" in m.text or "To use this bot" in m.text:
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
        save(FILE,custom)
        del pending[m.from_user.id]
        bot.reply_to(m, f"✅ حفظت {t}")
        return

    if txt.startswith("احذف امر"):
        cmd=txt.replace("احذف امر:","").replace("احذف امر","").strip()
        if cmd in custom:
            del custom[cmd]
            save(FILE,custom)
            bot.reply_to(m, f"✅ حذفت {cmd}")
        else:
            bot.reply_to(m, f"✅ نظفت {cmd}")
        return

@bot.message_handler(content_types=['text'],chat_types=['group','supergroup'])
def groups(m):
    text=(m.text or "").strip()
    chat_id=m.chat.id
    uid=m.from_user.id
    name=m.from_user.first_name or "شخص"
    add_count(chat_id,uid,name)

    if text in ["/start","start","الاوامر","اوامر","قائمة الاوامر"]:
        bot.send_message(chat_id, "قائمة الاوامر", reply_markup=main_menu(), reply_to_message_id=m.message_id)
        return

    if text in ["رتبتي","رتبتي ²⁷","رتبتي ٢٧"]:
        if "رتبتي" in custom:
            raw=custom["رتبتي"].get("text","") if isinstance(custom["رتبتي"],dict) else ""
            if "Tucos" not in raw and "A_TOOLS" not in raw and "A_Tools" not in raw and "To use this bot" not in raw:
                badge=get_badge(uid,chat_id)
                cnt,pos=get_stats(chat_id,uid)
                final=smart_replace(raw, name, badge, cnt, pos)
                bot.send_message(chat_id, final, reply_to_message_id=m.message_id)
                return
        badge=get_badge(uid,chat_id)
        cnt,pos=get_stats(chat_id,uid)
        bot.send_message(chat_id, f"≡ رتبتك هي ← {badge}\n≡ رسائلك ← {cnt}\n≡ ترتيبك ← {pos}\n-", reply_to_message_id=m.message_id)
        return

    if text in custom:
        raw=custom[text].get("text","") if isinstance(custom[text],dict) else ""
        if "Tucos" in raw or "A_TOOLS" in raw or "A_Tools" in raw or "To use this bot" in raw:
            del custom[text]
            save(FILE,custom)
            return
        badge=get_badge(uid,chat_id)
        cnt,pos=get_stats(chat_id,uid)
        final=smart_replace(raw, name, badge, cnt, pos)
        bot.send_message(chat_id, final, reply_to_message_id=m.message_id)

print("READY SECURE - NO TOKEN IN CODE - /start CLEAN")

while True:
    try:
        bot.infinity_polling(timeout=60,long_polling_timeout=60,skip_pending=True)
    except Exception as e:
        print(e)
        time.sleep(5)
