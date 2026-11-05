import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - SOUL AUTO", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, requests
from telebot.types import MessageEntity, User

BOT_TOKEN = "8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False, parse_mode=None)
OWNER_BOT_ID = 829238313

try:
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
except:
    pass

FILE = 'custom_commands.json'
OWNER_FILE = 'owner_info.json'
LOCK_FILE = 'locked_commands.json'
RANKS_FILE = 'user_ranks.json'
TOP_FILE = 'top.json'
SETTINGS_FILE = 'group_settings.json'

custom = {}
owner_info = {}
locked = {}
user_ranks = {}
top_data = {}
group_settings = {}

def load_all():
    global custom, owner_info, locked, user_ranks, top_data, group_settings
    try:
        with open(FILE,'r',encoding='utf-8') as f:
            d=json.load(f)
            custom.clear()
            custom.update(d)
    except:
        pass
    try:
        with open(OWNER_FILE,'r',encoding='utf-8') as f:
            d=json.load(f)
            owner_info.clear()
            owner_info.update(d)
            owner_info['private']='afiwd'
            owner_info['username']='afiwd'
    except:
        owner_info.update({"name":"محسن","username":"afiwd","bio":"https://t.me/afiwd","group":"- darkness","private":"afiwd","photo":None})
    try:
        with open(LOCK_FILE,'r',encoding='utf-8') as f:
            d=json.load(f)
            locked.clear()
            locked.update(d)
    except:
        pass
    try:
        with open(RANKS_FILE,'r',encoding='utf-8') as f:
            d=json.load(f)
            if d:
                user_ranks.clear()
                user_ranks.update(d)
    except:
        pass
    try:
        with open(TOP_FILE,'r',encoding='utf-8') as f:
            d=json.load(f)
            if d:
                top_data.clear()
                top_data.update(d)
    except:
        pass
    try:
        with open(SETTINGS_FILE,'r',encoding='utf-8') as f:
            d=json.load(f)
            group_settings.clear()
            group_settings.update(d)
    except:
        pass

load_all()

def save_custom():
    with open(FILE,'w',encoding='utf-8') as f:
        json.dump(custom,f,ensure_ascii=False,indent=2)
def save_locked():
    with open(LOCK_FILE,'w',encoding='utf-8') as f:
        json.dump(locked,f,ensure_ascii=False,indent=2)
def save_ranks():
    with open(RANKS_FILE,'w',encoding='utf-8') as f:
        json.dump(user_ranks,f,ensure_ascii=False,indent=2)
def save_top():
    with open(TOP_FILE,'w',encoding='utf-8') as f:
        json.dump(top_data,f,ensure_ascii=False,indent=2)
def save_settings():
    with open(SETTINGS_FILE,'w',encoding='utf-8') as f:
        json.dump(group_settings,f,ensure_ascii=False,indent=2)

RANK_ORDER = {"مميز":1,"ادمن":2,"مدير":3,"منشئ":4,"منشئ اساسي":5,"مالك":6,"مالك اساسي":7,"مالك المجموعه":8,"M":9,"MY":10,"Dev2":11,"Dev":12}

def normalize_rank(t):
    t=t.strip()
    m={"dev":"Dev","dev2":"Dev2","my":"MY","m":"M","مالك المجموعة":"مالك المجموعه"}
    if t.lower() in m:
        return m[t.lower()]
    for r in RANK_ORDER:
        if t==r or t in r or r in t:
            return r
    return t

def get_level(uid,cid):
    if uid==OWNER_BOT_ID:
        return 100
    cs=str(cid); us=str(uid)
    if cs in user_ranks and us in user_ranks[cs]:
        return RANK_ORDER.get(user_ranks[cs][us],0)
    return 0

def get_rank(uid,cid):
    if uid==OWNER_BOT_ID:
        return "Dev"
    cs=str(cid); us=str(uid)
    if cs in user_ranks and us in user_ranks[cs]:
        return user_ranks[cs][us]
    return "عضو"

def add_count(cid,uid,name):
    cs=str(cid); us=str(uid)
    if cs not in top_data:
        top_data[cs]={}
    if us not in top_data[cs]:
        top_data[cs][us]={"count":0,"name":name}
    top_data[cs][us]["count"]+=1
    top_data[cs][us]["name"]=name
    save_top()

def get_stats(cid,uid):
    cs=str(cid); us=str(uid)
    if cs not in top_data:
        return 0,0
    sorted_users=sorted(top_data[cs].items(),key=lambda x:x[1]["count"],reverse=True)
    cnt=top_data[cs].get(us,{}).get("count",0)
    pos=0
    for i,(u,d) in enumerate(sorted_users,1):
        if u==us:
            pos=i
            break
    if pos==0:
        pos=len(sorted_users)+1 if cnt>0 else 0
    return cnt,pos

def save_entities(msg):
    res=[]
    ents=msg.entities or msg.caption_entities or []
    for e in ents:
        en={"type":e.type,"offset":e.offset,"length":e.length}
        if getattr(e,'url',None):
            en["url"]=e.url
        if getattr(e,'custom_emoji_id',None):
            en["custom_emoji_id"]=e.custom_emoji_id
        if getattr(e,'user',None) and e.user:
            en["user"]={"id":e.user.id,"first_name":e.user.first_name}
        res.append(en)
    return res

def restore_entities(data):
    res=[]
    for en in data:
        try:
            kw={"type":en["type"],"offset":en["offset"],"length":en["length"]}
            if "url" in en:
                kw["url"]=en["url"]
            if "custom_emoji_id" in en:
                kw["custom_emoji_id"]=en["custom_emoji_id"]
            if "user" in en and en["user"]:
                u=en["user"]
                kw["user"]=User(u["id"],False,u.get("first_name",""))
            res.append(MessageEntity(**kw))
        except:
            pass
    return res

def replace_placeholders(text, target_name, target_rank, target_count, target_pos):
    if not text:
        return text
    text = text.replace("{الاسم}", target_name).replace("{فلان}", target_name).replace("{name}", target_name)
    text = text.replace("{الرتبة}", target_rank).replace("{رتبته}", target_rank).replace("{rank}", target_rank)
    text = text.replace("{التفاعل}", str(target_count)).replace("{تفاعلي}", str(target_count))
    text = text.replace("{الترتيب}", str(target_pos)).replace("{ترتيبي}", str(target_pos))
    return text

def is_static_ratbti(text):
    # اذا النص فيه 420 و 7 ثابت وما فيه متغيرات {الرتبة} يعني ثابت
    if not text:
        return True
    if "{الرتبة}" in text or "{التفاعل}" in text or "{الترتيب}" in text or "{الاسم}" in text:
        return False
    # لو فيه ارقام ثابتة كبيرة وما يحدث
    return True

waiting={}
pending={}
waiting_rank={}
waiting_rank_private={}

@bot.message_handler(chat_types=['private'],func=lambda m:m.from_user.id==OWNER_BOT_ID,content_types=['text','photo','sticker','animation','video','voice','document','audio'])
def private_lab(m):
    uid=m.from_user.id
    txt=(m.text or m.caption or "").strip()

    # قفل امر المطور Dev - يشتغل من الخاص
    if txt.startswith("قفل امر ") or txt.startswith("قفل أمر "):
        cmd_text = txt.replace("قفل امر ","").replace("قفل أمر ","").strip()
        parts = cmd_text.split()
        if len(parts) >= 2:
            possible_rank = normalize_rank(parts[-1])
            if possible_rank in RANK_ORDER:
                command_name = " ".join(parts[:-1]).strip()
                locked[command_name] = possible_rank
                save_locked()
                bot.reply_to(m, f"≡ تم وضع امر ↤ {command_name}\n≡ لرتبة ↤ {possible_rank} 🎖️\n≡ فقط")
                return
        waiting_rank_private[uid] = {"command": cmd_text}
        bot.reply_to(m, f"≡ حسنًا عزيزي قم بإرسال الرتبة الان :\n━━━━━━━━━━━━━━\n- Dev\n- Dev2\n- MY\n- M\n- مالك المجموعه\n- مالك اساسي\n- مالك\n- منشئ اساسي\n- منشئ\n- مدير\n- ادمن\n- مميز\n━━━━━━━━━━━━━━\n≡ سيتم وضع الأمر ↤ {cmd_text} للرتبة المحددة\nفقط")
        return

    if uid in waiting_rank_private:
        rank = normalize_rank(txt)
        if rank in RANK_ORDER:
            command = waiting_rank_private[uid]["command"]
            locked[command] = rank
            save_locked()
            del waiting_rank_private[uid]
            bot.reply_to(m, f"≡ تم وضع امر ↤ {command}\n≡ لرتبة ↤ {rank} 🎖️\n≡ فقط")
            return

    if txt.startswith("فتح امر ") or txt.startswith("فتح أمر "):
        cmd = txt.replace("فتح امر ","").replace("فتح أمر ","").strip()
        if cmd in locked:
            del locked[cmd]
            save_locked()
            bot.reply_to(m, f"✅ فتح {cmd}")
        else:
            bot.reply_to(m, f"❌ {cmd} مو مقفول")
        return

    if txt in ["قائمة الاقفال","قائمه الاقفال"]:
        if not locked:
            bot.reply_to(m,"ما فيه اقفال")
            return
        t="🔒 الاقفال:\n"
        for k,v in locked.items():
            t+=f"• {k} ↤ {v}\n"
        bot.reply_to(m,t)
        return

    if txt.startswith("اضف امر"):
        tmp=txt.replace("اضف امر:","").replace("اضف امر","").strip()
        if "->" in tmp:
            a,b=tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                data={"type":"text","text":resp,"entities":save_entities(m),"file_id":None,"caption":"","caption_entities":[]}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m,f"تمام - الامر: {trig}\nاكتب: ارفعه")
                return
        else:
            cmd=tmp
            if not cmd:
                return
            waiting[uid]={"step":"wait_reply","command":cmd}
            bot.reply_to(m,f"تمام - الامر: {cmd} ²⁷\nارسل الرد اللي تبيه يرد فيه بالضبط:")
            return

    if uid in waiting and waiting[uid]['step']=='wait_reply':
        cmd=waiting[uid]['command']
        ctype=m.content_type
        if ctype=='text':
            data={"type":"text","text":m.text,"entities":save_entities(m),"file_id":None,"caption":"","caption_entities":[]}
        elif ctype=='photo':
            data={"type":"photo","text":"","entities":[],"file_id":m.photo[-1].file_id,"caption":m.caption or "","caption_entities":save_entities(m)}
        elif ctype=='sticker':
            data={"type":"sticker","text":"","entities":[],"file_id":m.sticker.file_id,"caption":"","caption_entities":[]}
        else:
            data={"type":ctype,"text":m.text or m.caption or "","entities":save_entities(m),"file_id":getattr(getattr(m,ctype,None),'file_id',None),"caption":m.caption or "","caption_entities":save_entities(m)}
        pending[uid]={"t":cmd,"data":data}
        del waiting[uid]
        bot.reply_to(m,f"تمام\nالامر: {cmd}\nالرد محفوظ - اكتب: ارفعه")
        return

    if txt in ["ارفعه","احفظه"]:
        if uid not in pending:
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data
        save_custom()
        del pending[uid]
        bot.reply_to(m,f"✅ حفظت {t}\nالحين يرد نفس الرد اللي عطيته")
        return

    if txt.startswith("احذف امر"):
        cmd=txt.replace("احذف امر:","").replace("احذف امر","").strip()
        if cmd in custom:
            del custom[cmd]
            save_custom()
            bot.reply_to(m,f"✅ حذفت {cmd}\nالحين رتبتي بيرجع للنظام الاساسي ويحدث تلقائيا ✅")
        else:
            bot.reply_to(m,f"❌ {cmd} مو موجود في الاوامر المخصصة")
        return

    if txt in ["اوامري"]:
        if not custom:
            bot.reply_to(m,"ما فيه اوامر مخصصة")
            return
        t="اوامرك المخصصة:\n"
        for k in custom:
            t+=f"• {k}\n"
        t+="\nاحذف امر: رتبتي ← عشان يرجع يحدث تلقائيا"
        bot.reply_to(m,t)
        return

    if txt in ["/start"]:
        bot.reply_to(m,"خاصك: https://t.me/afiwd\n\nاذا رتبتي ما يحدث:\nاحذف امر: رتبتي\n\nقفل امر: قفل امر المطور Dev\n\nاضف امر: هلا -> يا هلا {الاسم}")

@bot.message_handler(content_types=['text','photo','sticker','animation','video','voice','document','audio'])
def groups(m):
    if m.chat.type=='private':
        return
    text=(m.text or m.caption or "").strip()
    chat_id=m.chat.id
    user_id=m.from_user.id
    first_name=m.from_user.first_name or "شخص"

    try:
        add_count(chat_id,user_id,first_name)
    except:
        pass

    # قفل امر المطور - نفس سول
    if text.startswith("قفل امر ") or text.startswith("قفل أمر "):
        if get_level(user_id,chat_id) < RANK_ORDER.get("Dev",12) and user_id!=OWNER_BOT_ID:
            bot.reply_to(m,"❌ فقط Dev")
            return
        cmd_text = text.replace("قفل امر ","").replace("قفل أمر ","").strip()
        parts = cmd_text.split()
        if len(parts) >= 2:
            possible_rank = normalize_rank(parts[-1])
            if possible_rank in RANK_ORDER:
                command_name = " ".join(parts[:-1]).strip()
                locked[command_name] = possible_rank
                save_locked()
                bot.reply_to(m, f"≡ تم وضع امر ↤ {command_name}\n≡ لرتبة ↤ {possible_rank} 🎖️\n≡ فقط")
                return
        waiting_rank[chat_id] = {"command": cmd_text, "user": user_id}
        bot.reply_to(m, f"≡ حسنًا عزيزي قم بإرسال الرتبة الان :\n━━━━━━━━━━━━━━\n- Dev\n- Dev2\n- MY\n- M\n- مالك المجموعه\n- مالك اساسي\n- مالك\n- منشئ اساسي\n- منشئ\n- مدير\n- ادمن\n- مميز\n━━━━━━━━━━━━━━\n≡ سيتم وضع الأمر ↤ {cmd_text} للرتبة المحددة\nفقط")
        return

    if chat_id in waiting_rank and waiting_rank[chat_id]["user"] == user_id:
        rank = normalize_rank(text)
        if rank in RANK_ORDER:
            command = waiting_rank[chat_id]["command"]
            locked[command] = rank
            save_locked()
            del waiting_rank[chat_id]
            bot.reply_to(m, f"≡ تم وضع امر ↤ {command}\n≡ لرتبة ↤ {rank} 🎖️\n≡ فقط")
            return

    if text.startswith("فتح امر "):
        cmd = text.replace("فتح امر ","").strip()
        if cmd in locked:
            del locked[cmd]
            save_locked()
            bot.reply_to(m, f"✅ فتح {cmd}")
        return

    if text.startswith("رفع ") and m.reply_to_message:
        rank_name=normalize_rank(text.replace("رفع ","").strip())
        if rank_name in RANK_ORDER:
            target_id=m.reply_to_message.from_user.id
            target_name=m.reply_to_message.from_user.first_name or "الشخص"
            if get_level(user_id,chat_id) <= RANK_ORDER.get(rank_name,0) and user_id!=OWNER_BOT_ID:
                bot.reply_to(m,f"❌ ما تقدر ترفع {rank_name}")
                return
            cs=str(chat_id); us=str(target_id)
            if cs not in user_ranks:
                user_ranks[cs]={}
            user_ranks[cs][us]=rank_name
            save_ranks()
            cnt,pos=get_stats(chat_id,target_id)
            # مثل سول بالضبط - يحدث الرتبة
            bot.send_message(chat_id,f"🎖️ تم رفع {target_name} الى {rank_name}\n\n≡ رتبته هي ← {rank_name} 🎖️\n≡ رسائله بالتفاعل ← {cnt}\n≡ ترتيبه بالمتفاعلين ← {pos}\n-",reply_to_message_id=m.message_id)
            return

    if text.startswith("تنزيل ") and m.reply_to_message:
        target_id=m.reply_to_message.from_user.id
        target_name=m.reply_to_message.from_user.first_name or "الشخص"
        cs=str(chat_id); us=str(target_id)
        if cs in user_ranks and us in user_ranks[cs]:
            del user_ranks[cs][us]
            save_ranks()
            bot.send_message(chat_id,f"✅ تم تنزيل {target_name}",reply_to_message_id=m.message_id)
        return

    # رتبتي - مثل سول - يحدث تلقائيا لكل شخص
    if text in ["رتبتي","رتبتي ²⁷"]:
        # اذا فيه امر مخصص ثابت 420 - تجاهله وخل النظام الاساسي يشتغل
        if "رتبتي" in custom:
            raw = custom["رتبتي"].get("text","") or custom["رتبتي"].get("caption","")
            if is_static_ratbti(raw) and "420" in raw:
                # تجاهل المخصص الثابت واستخدم النظام الاساسي
                pass
            else:
                # فيه متغيرات {الرتبة} استخدمه
                data=custom["رتبتي"]
                rank=get_rank(user_id,chat_id)
                cnt,pos=get_stats(chat_id,user_id)
                final = replace_placeholders(data.get("text","") or data.get("caption",""), first_name, rank, cnt, pos)
                bot.reply_to(m, final)
                return
        # النظام الاساسي - يحدث تلقائيا لكل شخص
        rank=get_rank(user_id,chat_id)
        cnt,pos=get_stats(chat_id,user_id)
        # نفس ستايل الصورة بالضبط
        bot.reply_to(m,f"🎖️ رتبتك هي ← {rank}\n\nرسائلك بالتفاعل ← {cnt}\nترتيبك بالمتفاعلين ← {pos}\n-")
        return

    if text in ["رتبته","رتبته ²⁷","رتبه"]:
        if not m.reply_to_message:
            bot.reply_to(m,"سوي ريبلاي على الشخص واكتب: رتبته")
            return
        target=m.reply_to_message.from_user
        target_id=target.id
        target_name=target.first_name or "الشخص"
        # نفس المشكلة - اذا رتبته مخصص ثابت تجاهله
        if "رتبته" in custom:
            raw = custom["رتبته"].get("text","") or custom["رتبته"].get("caption","")
            if is_static_ratbti(raw) and "420" in raw:
                pass
            else:
                data=custom["رتبته"]
                rank=get_rank(target_id,chat_id)
                cnt,pos=get_stats(chat_id,target_id)
                final = replace_placeholders(data.get("text","") or data.get("caption",""), target_name, rank, cnt, pos)
                bot.reply_to(m, final)
                return
        rank=get_rank(target_id,chat_id)
        cnt,pos=get_stats(chat_id,target_id)
        bot.reply_to(m,f"🎖️ رتبة {target_name} هي ← {rank}\n\nرسائله بالتفاعل ← {cnt}\nترتيبه بالمتفاعلين ← {pos}\n-")
        return

    # اوامر مخصصة - ترد نفس اللي عطيته في الخاص
    if text in custom and text not in ["رتبتي","رتبته","رتبه","رتبتي ²⁷","رتبته ²⁷"]:
        data=custom[text]
        target_name = first_name
        target_rank = get_rank(user_id,chat_id)
        target_count, target_pos = get_stats(chat_id,user_id)
        if m.reply_to_message:
            target = m.reply_to_message.from_user
            target_name = target.first_name or "الشخص"
            target_rank = get_rank(target.id, chat_id)
            target_count, target_pos = get_stats(chat_id, target.id)

        if isinstance(data,dict):
            try:
                ctype=data.get("type","text")
                if ctype=="text":
                    raw_text = data.get("text","")
                    final_text = replace_placeholders(raw_text, target_name, target_rank, target_count, target_pos)
                    ents=restore_entities(data.get("entities",[]))
                    if ents and "{" not in raw_text:
                        bot.send_message(chat_id, final_text, entities=ents, reply_to_message_id=m.message_id)
                    else:
                        bot.send_message(chat_id, final_text, reply_to_message_id=m.message_id)
                elif ctype=="photo":
                    cap = data.get("caption","")
                    final_cap = replace_placeholders(cap, target_name, target_rank, target_count, target_pos)
                    bot.send_photo(chat_id, data["file_id"], caption=final_cap, reply_to_message_id=m.message_id)
                elif ctype=="sticker":
                    bot.send_sticker(chat_id, data["file_id"], reply_to_message_id=m.message_id)
            except:
                raw_text = data.get("text","") or data.get("caption","")
                final_text = replace_placeholders(raw_text, target_name, target_rank, target_count, target_pos)
                bot.reply_to(m, final_text)
        return

    # قفل امر
    if text in locked:
        # اذا مقفول
        req = locked[text]
        if get_level(user_id,chat_id) < RANK_ORDER.get(req,0) and user_id!=OWNER_BOT_ID:
            bot.reply_to(m,f"❌ امر {text} مقفول لرتبة {req} فقط")
            return

print("READY - SOUL AUTO UPDATE - FIXED 420 BUG")

while True:
    try:
        bot.infinity_polling(timeout=60,long_polling_timeout=60,skip_pending=True,none_stop=True)
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
            print(f"{e}")
            time.sleep(5)
