import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - FIX PLACEHOLDERS", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, json, time, requests, re
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

BASE_DIR = "/opt/render/project/src" if os.path.exists("/opt/render/project/src") else "."
if os.path.exists("/data"):
    BASE_DIR = "/data"

def get_path(name):
    return os.path.join(BASE_DIR, name)

FILE = get_path('custom_commands.json')
LOCK_FILE = get_path('locked_commands.json')
RANKS_FILE = get_path('user_ranks.json')
TOP_FILE = get_path('top.json')

custom = {}
locked = {}
user_ranks = {}
top_data = {}

def load_all():
    global custom, locked, user_ranks, top_data
    try:
        with open(FILE,'r',encoding='utf-8') as f:
            d=json.load(f)
            custom.clear()
            custom.update(d)
    except:
        pass
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

def get_rank_with_badge(uid,cid):
    rank = get_rank(uid,cid)
    level = RANK_ORDER.get(rank,0)
    if level >= RANK_ORDER.get("MY",10) or uid==OWNER_BOT_ID:
        return f"{rank} 🎖️"
    else:
        return rank

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
        pos=len(sorted_users)+1 if cnt>0 else 1
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
            res.append(MessageEntity(**kw))
        except:
            pass
    return res

def replace_placeholders(text, target_name, target_rank_raw, target_rank_badge, target_count, target_pos):
    if not text:
        return text
    # مع اقواس وبدون اقواس - يفهم الاثنين
    # {الرتبة} او الرتبة
    # {التفاعل} او التفاعل
    # {الترتيب} او الترتيب او الرتيب
    # {الاسم} او الاسم
    
    # اولا مع اقواس
    text = text.replace("{الرتبة}", target_rank_badge).replace("{رتبته}", target_rank_badge).replace("{رتبتي}", target_rank_badge)
    text = text.replace("{التفاعل}", str(target_count)).replace("{تفاعلي}", str(target_count)).replace("{تفاعله}", str(target_count))
    text = text.replace("{الترتيب}", str(target_pos)).replace("{ترتيبي}", str(target_pos)).replace("{الرتيب}", str(target_pos)).replace("{الترتيب}", str(target_pos))
    text = text.replace("{الاسم}", target_name).replace("{فلان}", target_name).replace("{المعرف}", target_name)
    
    # بدون اقواس - فقط اذا كلمة مستقلة بعد ← او ≡ او مسافة
    # نستخدم regex عشان ما نخرب النص
    # الرتبة
    text = re.sub(r'←\s*الرتبة\b', f'← {target_rank_badge}', text)
    text = re.sub(r'≡\s*الرتبة\b', f'≡ {target_rank_badge}', text)
    # لو كتبت وحدها في السطر
    if text.strip() == "الرتبة":
        text = target_rank_badge
    # التفاعل
    text = re.sub(r'←\s*التفاعل\b', f'← {target_count}', text)
    # الرتيب / الترتيب
    text = re.sub(r'←\s*الرتيب\b', f'← {target_pos}', text)
    text = re.sub(r'←\s*الترتيب\b', f'← {target_pos}', text)
    text = re.sub(r'←\s*الرتيب\b', f'← {target_pos}', text)
    
    # اذا كتب ← الرتبة في الاخر
    # نستبدل ايضا اذا موجودة كقيمة مستقلة
    # مثال: "رتبتك هي ← الرتبة" -> "رتبتك هي ← MY 🎖️"
    if "الرتبة" in text and target_rank_badge not in text:
        # فقط لو ما فيه {الرتبة} اصلا وما استبدلنا
        # نستبدل اخر ظهور لـ الرتبة اذا كان بعد ←
        parts = text.split("←")
        if len(parts) > 1 and "الرتبة" in parts[-1]:
            # اذا اخر جزء فيه الرتبة
            text = text.replace("الرتبة", target_rank_badge, 1) if "الرتبة" in text else text
    
    return text

# تحسين: دالة ذكية تفهم الشكل
def smart_replace(text, name, rank_raw, rank_badge, count, pos):
    if not text:
        return text
    original = text
    
    # اذا استخدم { } - نستخدم القديم
    if "{" in text and "}" in text:
        return replace_placeholders(text, name, rank_raw, rank_badge, count, pos)
    
    # اذا كتب بدون اقواس مثل الصورة: "رتبتك هي ← الرتبة"
    # نستبدل الرتبة / التفاعل / الرتيب
    # نبحث عن النمط: ← الرتبة , ← التفاعل , ← الرتيب
    # هذا اللي في صورتك
    
    # نستبدل بذكاء
    # اذا فيه كلمة الرتبة لوحدها
    text = text.replace("الرتبة", rank_badge)
    text = text.replace("التفاعل", str(count))
    text = text.replace("الرتيب", str(pos))
    text = text.replace("الترتيب", str(pos))
    
    # اذا بعد الاستبدال لسه فيه كلمات عامة
    return text

waiting={}
pending={}
waiting_rank={}

@bot.message_handler(chat_types=['private'],func=lambda m:m.from_user.id==OWNER_BOT_ID,content_types=['text','photo','sticker','animation','video','voice','document','audio'])
def private_lab(m):
    uid=m.from_user.id
    txt=(m.text or m.caption or "").strip()

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
        waiting_rank[uid] = {"command": cmd_text}
        bot.reply_to(m, f"≡ حسنًا عزيزي قم بإرسال الرتبة الان :\n- Dev\n- Dev2\n- MY\n- M\n- مالك المجموعه\n- مالك اساسي\n- مالك\n- منشئ اساسي\n- منشئ\n- مدير\n- ادمن\n- مميز\n≡ سيتم وضع الأمر ↤ {cmd_text} للرتبة المحددة فقط")
        return

    if uid in waiting_rank:
        rank = normalize_rank(txt)
        if rank in RANK_ORDER:
            command = waiting_rank[uid]["command"]
            locked[command] = rank
            save_locked()
            del waiting_rank[uid]
            bot.reply_to(m, f"≡ تم وضع امر ↤ {command}\n≡ لرتبة ↤ {rank} 🎖️\n≡ فقط")
            return

    if txt.startswith("فتح امر "):
        cmd = txt.replace("فتح امر ","").strip()
        if cmd in locked:
            del locked[cmd]
            save_locked()
            bot.reply_to(m, f"✅ فتح {cmd}")
        return

    if txt.startswith("اضف امر"):
        tmp=txt.replace("اضف امر:","").replace("اضف امر","").strip()
        if "->" in tmp:
            a,b=tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                data={"type":"text","text":resp,"entities":save_entities(m),"file_id":None,"caption":"","caption_entities":[]}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m,f"تمام - الامر: {trig}\nالشكل:\n{resp}\n\nبيرد بنفس الشكل بس يحدث ✅\nاكتب: ارفعه")
                return
        else:
            cmd=tmp
            if not cmd:
                return
            waiting[uid]={"step":"wait_reply","command":cmd}
            bot.reply_to(m,f"تمام - الامر: {cmd} ²⁷\nارسل الشكل اللي تبيه:\n\nتقدر تستخدم:\n{{الرتبة}} او الرتبة\n{{التفاعل}} او التفاعل\n{{الترتيب}} او الرتيب\n{{الاسم}}\n\nمثال:\n≡ رتبتك هي ← {{الرتبة}}\n≡ رسائلك ← {{التفاعل}}\n≡ ترتيبك ← {{الترتيب}}")
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
        bot.reply_to(m,f"تمام - محفوظ\nاكتب: ارفعه")
        return

    if txt in ["ارفعه","احفظه"]:
        if uid not in pending:
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data
        save_custom()
        del pending[uid]
        sample_text = data.get("text","") or data.get("caption","")
        preview_my = smart_replace(sample_text, "محسن", "MY", "MY 🎖️", 422, 7)
        preview_member = smart_replace(sample_text, "نايف", "مميز", "مميز", 5, 2)
        bot.reply_to(m,f"✅ حفظت {t}\n\nالشكل اللي عطيته:\n{sample_text}\n\nلو MY وفوق (مع شارة):\n{preview_my}\n\nلو مميز (بدون شارة):\n{preview_member}\n\n✅ يحدث تلقائيا لكل شخص ✅")
        return

    if txt.startswith("احذف امر"):
        cmd=txt.replace("احذف امر:","").replace("احذف امر","").strip()
        if cmd in custom:
            del custom[cmd]
            save_custom()
            bot.reply_to(m,f"✅ حذفت {cmd}")
        else:
            try:
                with open(FILE,'r',encoding='utf-8') as f:
                    d=json.load(f)
                    if cmd in d:
                        del d[cmd]
                        with open(FILE,'w',encoding='utf-8') as wf:
                            json.dump(d,wf,ensure_ascii=False,indent=2)
                        custom.pop(cmd, None)
                        bot.reply_to(m,f"✅ حذفت {cmd}")
                        return
            except:
                pass
            bot.reply_to(m,f"❌ {cmd} مو موجود")
        return

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
        bot.reply_to(m, f"≡ حسنًا عزيزي قم بإرسال الرتبة الان :\n- Dev\n- Dev2\n- MY\n- M\n- مالك المجموعه\n- مالك اساسي\n- مالك\n- منشئ اساسي\n- منشئ\n- مدير\n- ادمن\n- مميز\n≡ سيتم وضع الأمر ↤ {cmd_text} للرتبة المحددة فقط")
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
            rank_badge = get_rank_with_badge(target_id, chat_id)
            bot.send_message(chat_id,f"🎖️ تم رفع {target_name} الى {rank_badge}\n\n≡ رتبته هي ← {rank_badge}\n≡ رسائله بالتفاعل ← {cnt}\n≡ ترتيبه بالمتفاعلين ← {pos}\n-",reply_to_message_id=m.message_id)
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

    if text in ["رتبتي","رتبتي ²⁷","رتبته","رتبته ²⁷","رتبه","رتبة"]:
        target_id = user_id
        target_name = first_name
        is_ratbto = text in ["رتبته","رتبته ²⁷","رتبه","رتبة"]
        if is_ratbto:
            if not m.reply_to_message:
                bot.reply_to(m,"سوي ريبلاي على الشخص واكتب: رتبته")
                return
            target=m.reply_to_message.from_user
            target_id=target.id
            target_name=target.first_name or "الشخص"

        if text in custom or (is_ratbto and "رتبته" in custom) or (not is_ratbto and "رتبتي" in custom):
            key = text if text in custom else ("رتبته" if is_ratbto else "رتبتي")
            if key in custom:
                data=custom[key]
                rank_raw=get_rank(target_id,chat_id)
                rank_badge=get_rank_with_badge(target_id,chat_id)
                cnt,pos=get_stats(chat_id,target_id)
                raw = data.get("text","") or data.get("caption","")
                final = smart_replace(raw, target_name, rank_raw, rank_badge, cnt, pos)
                try:
                    if data.get("type")=="text":
                        bot.send_message(chat_id, final, entities=restore_entities(data.get("entities",[])), reply_to_message_id=m.message_id)
                    elif data.get("type")=="photo":
                        bot.send_photo(chat_id, data["file_id"], caption=final, reply_to_message_id=m.message_id)
                    else:
                        bot.reply_to(m, final)
                except:
                    bot.reply_to(m, final)
                return

        rank_raw=get_rank(target_id,chat_id)
        rank_badge=get_rank_with_badge(target_id,chat_id)
        cnt,pos=get_stats(chat_id,target_id)
        if is_ratbto:
            bot.reply_to(m,f"≡ رتبة {target_name} هي ← {rank_badge}\n\n≡ رسائله بالتفاعل ← {cnt}\n≡ ترتيبه بالمتفاعلين ← {pos}\n-")
        else:
            bot.reply_to(m,f"≡ رتبتك هي ← {rank_badge}\n\n≡ رسائلك بالتفاعل ← {cnt}\n≡ ترتيبك بالمتفاعلين ← {pos}\n-")
        return

    if text in custom:
        if text in locked:
            req = locked[text]
            if get_level(user_id,chat_id) < RANK_ORDER.get(req,0) and user_id!=OWNER_BOT_ID:
                bot.reply_to(m,f"❌ امر {text} مقفول لرتبة {req} فقط")
                return
        data=custom[text]
        rank_raw=get_rank(user_id,chat_id)
        rank_badge=get_rank_with_badge(user_id,chat_id)
        cnt,pos=get_stats(chat_id,user_id)
        tname = first_name
        if m.reply_to_message:
            tname = m.reply_to_message.from_user.first_name or "الشخص"
            rank_raw = get_rank(m.reply_to_message.from_user.id, chat_id)
            rank_badge = get_rank_with_badge(m.reply_to_message.from_user.id, chat_id)
            cnt,pos = get_stats(chat_id, m.reply_to_message.from_user.id)
        if isinstance(data,dict):
            try:
                ctype=data.get("type","text")
                if ctype=="text":
                    raw_text = data.get("text","")
                    final_text = smart_replace(raw_text, tname, rank_raw, rank_badge, cnt, pos)
                    bot.send_message(chat_id, final_text, reply_to_message_id=m.message_id)
                elif ctype=="photo":
                    cap = data.get("caption","")
                    final_cap = smart_replace(cap, tname, rank_raw, rank_badge, cnt, pos)
                    bot.send_photo(chat_id, data["file_id"], caption=final_cap, reply_to_message_id=m.message_id)
                elif ctype=="sticker":
                    bot.send_sticker(chat_id, data["file_id"], reply_to_message_id=m.message_id)
            except:
                raw_text = data.get("text","") or data.get("caption","")
                final_text = smart_replace(raw_text, tname, rank_raw, rank_badge, cnt, pos)
                bot.reply_to(m, final_text)
        return

print(f"READY - FIX PLACEHOLDERS - BADGE MY+")

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
