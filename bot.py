import os
from flask import Flask
import threading

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - EXACT REPLY", 200
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
RANKS_FILE = 'user_ranks.json'
TOP_FILE = 'top.json'

custom = {}
owner_info = {}
user_ranks = {}
top_data = {}

def load_all():
    global custom, owner_info, user_ranks, top_data
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
    except:
        owner_info.update({"name":"محسن","username":"afiwd","bio":"https://t.me/afiwd","group":"- darkness","photo":None})
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
def save_owner():
    with open(OWNER_FILE,'w',encoding='utf-8') as f:
        json.dump(owner_info,f,ensure_ascii=False,indent=2)
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
        pos=len(sorted_users)+1
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
        if getattr(e,'language',None):
            en["language"]=e.language
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
            if "language" in en:
                kw["language"]=en["language"]
            res.append(MessageEntity(**kw))
        except:
            pass
    return res

def replace_placeholders(text, target_name, target_rank, target_count, target_pos):
    if not text:
        return text
    text = text.replace("{الاسم}", target_name)
    text = text.replace("{فلان}", target_name)
    text = text.replace("{name}", target_name)
    text = text.replace("{الرتبة}", target_rank)
    text = text.replace("{رتبته}", target_rank)
    text = text.replace("{rank}", target_rank)
    text = text.replace("{التفاعل}", str(target_count))
    text = text.replace("{تفاعلي}", str(target_count))
    text = text.replace("{الترتيب}", str(target_pos))
    text = text.replace("{ترتيبي}", str(target_pos))
    text = text.replace("{المعرف}", target_name)
    return text

waiting={}
pending={}

@bot.message_handler(chat_types=['private'],func=lambda m:m.from_user.id==OWNER_BOT_ID,content_types=['text','photo','sticker','animation','video','voice','document','audio'])
def private_lab(m):
    uid=m.from_user.id
    txt=(m.text or m.caption or "").strip()

    if txt.startswith("اضف امر"):
        tmp=txt.replace("اضف امر:","").replace("اضف امر","").strip()
        if "->" in tmp:
            a,b=tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                data={"type":"text","text":resp,"entities":save_entities(m),"file_id":None,"caption":"","caption_entities":[]}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m,f"تمام\n{trig}\nاكتب: ارفعه")
                return
        else:
            cmd=tmp
            if not cmd:
                return
            waiting[uid]={"step":"wait_reply","command":cmd}
            bot.reply_to(m,f"تمام - الامر: {cmd}\nارسل الرد اللي تبيه يرد فيه بالضبط:")
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
        elif ctype=='animation':
            data={"type":"animation","text":"","entities":[],"file_id":m.animation.file_id,"caption":m.caption or "","caption_entities":save_entities(m)}
        elif ctype=='video':
            data={"type":"video","text":"","entities":[],"file_id":m.video.file_id,"caption":m.caption or "","caption_entities":save_entities(m)}
        else:
            data={"type":ctype,"text":m.text or m.caption or "","entities":save_entities(m),"file_id":getattr(getattr(m,ctype,None),'file_id',None),"caption":m.caption or "","caption_entities":save_entities(m)}
        pending[uid]={"t":cmd,"data":data}
        del waiting[uid]
        bot.reply_to(m,f"تمام\nالامر: {cmd}\nالرد محفوظ - اكتب: ارفعه")
        return

    if txt in ["ارفعه","احفظه"]:
        if uid not in pending:
            bot.reply_to(m,"ما فيه شي")
            return
        t=pending[uid]["t"]; data=pending[uid]["data"]
        custom[t]=data
        save_custom()
        del pending[uid]
        bot.reply_to(m,f"حفظت {t}\nالحين يرد نفس الرد اللي عطيته بالضبط")
        return

    if txt.startswith("احذف امر"):
        cmd=txt.replace("احذف امر:","").replace("احذف امر","").strip()
        if cmd in custom:
            del custom[cmd]
            save_custom()
            bot.reply_to(m,f"حذفت {cmd}")
        else:
            bot.reply_to(m,f"{cmd} مو موجود")
        return

    if txt in ["اوامري","اوامر","قائمتي"]:
        if not custom:
            bot.reply_to(m,"ما فيه اوامر")
            return
        txt_list="اوامرك:\n"
        for k in custom.keys():
            txt_list+=f"• {k}\n"
        bot.reply_to(m,txt_list)
        return

    if txt in ["الغاء","الغه"]:
        waiting.pop(uid,None); pending.pop(uid,None)
        bot.reply_to(m,"الغاء")
        return

    if txt in ["/start","start"]:
        bot.reply_to(m,f"اهلا {uid}\nخاصك: https://t.me/afiwd\n\nالطريقة:\nاضف امر: رتبته -> ردك\nاضف امر: هلا\nترسل الرد\nارفعه\n\nيدعم {{الاسم}} {{الرتبة}} {{التفاعل}} {{الترتيب}}")
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

    if text.startswith("رفع ") and m.reply_to_message:
        rank_name=normalize_rank(text.replace("رفع ","").strip())
        if rank_name in RANK_ORDER:
            target_id=m.reply_to_message.from_user.id
            target_name=m.reply_to_message.from_user.first_name or "الشخص"
            if get_level(user_id,chat_id) <= RANK_ORDER.get(rank_name,0) and user_id!=OWNER_BOT_ID:
                bot.reply_to(m,f"ما تقدر ترفع {rank_name}")
                return
            cs=str(chat_id); us=str(target_id)
            if cs not in user_ranks:
                user_ranks[cs]={}
            user_ranks[cs][us]=rank_name
            save_ranks()
            cnt,pos=get_stats(chat_id,target_id)
            bot.send_message(chat_id,f"تم رفع {target_name} الى {rank_name}\n\nرتبته هي ← {rank_name}\nرسائله ← {cnt}\nترتيبه ← {pos}",reply_to_message_id=m.message_id)
            return

    if text.startswith("تنزيل ") and m.reply_to_message:
        target_id=m.reply_to_message.from_user.id
        target_name=m.reply_to_message.from_user.first_name or "الشخص"
        cs=str(chat_id); us=str(target_id)
        if cs in user_ranks and us in user_ranks[cs]:
            del user_ranks[cs][us]
            save_ranks()
            bot.send_message(chat_id,f"تم تنزيل {target_name}",reply_to_message_id=m.message_id)
        return

    if text in ["رتبتي","رتبتي ²⁷"] and "رتبتي" not in custom:
        rank=get_rank(user_id,chat_id)
        cnt,pos=get_stats(chat_id,user_id)
        bot.reply_to(m,f"رتبتك هي ← {rank}\nرسائلك ← {cnt}\nترتيبك ← {pos}")
        return

    if text in ["رتبته","رتبته ²⁷","رتبه","رتبة"] and "رتبته" not in custom and "رتبه" not in custom:
        if not m.reply_to_message:
            bot.reply_to(m,"سوي ريبلاي على الشخص واكتب: رتبته")
            return
        target=m.reply_to_message.from_user
        target_id=target.id
        target_name=target.first_name or "الشخص"
        rank=get_rank(target_id,chat_id)
        cnt,pos=get_stats(chat_id,target_id)
        bot.reply_to(m,f"رتبة {target_name} هي ← {rank}\nرسائله ← {cnt}\nترتيبه ← {pos}")
        return

    if text in custom:
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
                    ents=restore_entities(data.get("caption_entities",[]))
                    if ents and "{" not in cap:
                        bot.send_photo(chat_id, data["file_id"], caption=final_cap, caption_entities=ents, reply_to_message_id=m.message_id)
                    else:
                        bot.send_photo(chat_id, data["file_id"], caption=final_cap, reply_to_message_id=m.message_id)
                elif ctype=="sticker":
                    bot.send_sticker(chat_id, data["file_id"], reply_to_message_id=m.message_id)
                elif ctype=="animation":
                    cap = data.get("caption","")
                    final_cap = replace_placeholders(cap, target_name, target_rank, target_count, target_pos)
                    bot.send_animation(chat_id, data["file_id"], caption=final_cap, reply_to_message_id=m.message_id)
                elif ctype=="video":
                    cap = data.get("caption","")
                    final_cap = replace_placeholders(cap, target_name, target_rank, target_count, target_pos)
                    bot.send_video(chat_id, data["file_id"], caption=final_cap, reply_to_message_id=m.message_id)
                else:
                    raw_text = data.get("text","") or data.get("caption","")
                    final_text = replace_placeholders(raw_text, target_name, target_rank, target_count, target_pos)
                    bot.reply_to(m, final_text)
            except Exception as e:
                print(f"custom error: {e}")
                raw_text = data.get("text","") or data.get("caption","")
                final_text = replace_placeholders(raw_text, target_name, target_rank, target_count, target_pos)
                bot.reply_to(m, final_text)
        else:
            bot.reply_to(m, str(data))
        return

print("READY - EXACT SAME REPLY AS PRIVATE - FIXED SYNTAX")

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
