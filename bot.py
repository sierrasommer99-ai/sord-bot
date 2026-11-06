import os, json

# === حذف قسري لكل الملفات الفاسدة عند التشغيل ===
for p in [
    "/data/custom_commands.json",
    "/opt/render/project/src/custom_commands.json",
    "./custom_commands.json",
    "custom_commands.json",
    "/data/locked_commands.json",
    "/opt/render/project/src/locked_commands.json"
]:
    try:
        if os.path.exists(p):
            print(f"!!! FORCE DELETING: {p}")
            os.remove(p)
            # انشئ فاضي نظيف
            with open(p,'w',encoding='utf-8') as wf:
                json.dump({}, wf)
    except Exception as e:
        print(f"delete error {p}: {e}")
        try:
            os.remove(p)
        except:
            pass

from flask import Flask
import threading, html

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "OK - FORCE CLEAN", 200
@flask_app.route('/health')
def health():
    return "OK", 200
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()

import telebot, time, requests, re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8769832522:AAF-qXZfMQ75Z1XfnLN2hA-G90qP0xYKzTA"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False, parse_mode=None)
OWNER_BOT_ID = 829238313

try:
    bot.remove_webhook()
    time.sleep(1)
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True", timeout=10)
except:
    pass

BASE_DIR = "/data" if os.path.exists("/data") else ("/opt/render/project/src" if os.path.exists("/opt/render/project/src") else ".")
def get_path(name):
    return os.path.join(BASE_DIR, name)

FILE = get_path('custom_commands.json')
LOCK_FILE = get_path('locked_commands.json')
RANKS_FILE = get_path('user_ranks.json')
TOP_FILE = get_path('top.json')
SETTINGS_FILE = get_path('settings.json')

custom = {}
locked = {}
user_ranks = {}
top_data = {}
settings = {"leave_dev_msg": "≡ المطور غادر المجموعه 💔\n≡ {الاسم} ← {الرتبة}\n-"}

def load_all():
    global custom, locked, user_ranks, top_data, settings
    # custom فاضي - نظفناه فوق
    try:
        if os.path.exists(FILE):
            with open(FILE,'r',encoding='utf-8') as f:
                data=json.load(f)
                if isinstance(data, dict) and len(data) > 0:
                    # اذا لسه فيه شي - امسحه مرة ثانية
                    if any("A_Tools" in str(v) or "Tucos" in str(v) or "To use this bot" in str(v) for v in data.values()):
                        print("STILL DIRTY - WIPING AGAIN")
                        with open(FILE,'w',encoding='utf-8') as wf:
                            json.dump({}, wf)
                    else:
                        custom.update(data)
    except:
        pass
    for fpath, dct in [(LOCK_FILE, locked), (RANKS_FILE, user_ranks), (TOP_FILE, top_data), (SETTINGS_FILE, settings)]:
        try:
            if os.path.exists(fpath):
                with open(fpath,'r',encoding='utf-8') as f:
                    data=json.load(f)
                    dct.clear()
                    dct.update(data)
        except:
            pass

load_all()

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def save_custom(): save_json(FILE, custom)
def save_locked(): save_json(LOCK_FILE, locked)
def save_ranks(): save_json(RANKS_FILE, user_ranks)
def save_top(): save_json(TOP_FILE, top_data)
def save_settings(): save_json(SETTINGS_FILE, settings)

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

def get_top_list_mention(cid, uid):
    cs=str(cid)
    if cs not in top_data or not top_data[cs]:
        return "ما فيه متفاعلين بعد"
    sorted_users=sorted(top_data[cs].items(),key=lambda x:x[1]["count"],reverse=True)[:20]
    txt = "💬 توب اكثر 20 متفاعلين بالقروب :\n─────────────\n\n"
    for i,(u_id, data) in enumerate(sorted_users,1):
        name = data.get("name","مجهول")
        cnt = data.get("count",0)
        safe_name = html.escape(name[:25])
        mention = f'<a href="tg://user?id={u_id}">{safe_name}</a>'
        txt += f"{i}) {cnt} | {mention}\n"
    txt += "\n─────────────\n"
    my_cnt, _ = get_stats(cid, uid)
    my_name = top_data[cs].get(str(uid),{}).get("name","٢٧")
    safe_my = html.escape(my_name[:25])
    my_mention = f'<a href="tg://user?id={uid}">{safe_my}</a>'
    txt += f"≡ you) {my_cnt} | {my_mention}"
    return txt

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

def smart_replace(text, name, rank_raw, rank_badge, count, pos):
    if not text:
        return text
    text = re.sub(r"「\s*」", f"「 {name} 」", text)
    text = re.sub(r"「\s*ذا\s*」", f"「 {name} 」", text)
    text = text.replace("{الرتبة}", rank_badge).replace("{التفاعل}", str(count)).replace("{الترتيب}", str(pos)).replace("{الرتيب}", str(pos))
    text = text.replace("{الاسم}", name)
    return text

def get_private_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ اضف امر", callback_data="p_add"),
        InlineKeyboardButton("➖ احذف امر", callback_data="p_del")
    )
    markup.add(
        InlineKeyboardButton("📜 اوامري", callback_data="p_my"),
        InlineKeyboardButton("🔒 قائمة الاقفال", callback_data="p_locks")
    )
    markup.add(
        InlineKeyboardButton("📁 الملفات", callback_data="p_files"),
        InlineKeyboardButton("✅ البوت نظيف", callback_data="p_clean_ok")
    )
    markup.add(InlineKeyboardButton("• إغلاق •", callback_data="menu_close"))
    return markup

def get_private_back():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("• رجوع للقائمة •", callback_data="p_main"))
    markup.add(InlineKeyboardButton("• إغلاق •", callback_data="menu_close"))
    return markup

def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("التفعيل والتعطيل", callback_data="menu_toggle"),
        InlineKeyboardButton("القفل والفتح", callback_data="menu_lock")
    )
    markup.add(
        InlineKeyboardButton("التسلية والخدمية", callback_data="menu_fun"),
        InlineKeyboardButton("ادارة القروب", callback_data="menu_admin")
    )
    markup.add(InlineKeyboardButton("اوامر Dev", callback_data="menu_dev"))
    markup.add(InlineKeyboardButton("الإعدادات", callback_data="menu_settings"))
    markup.add(InlineKeyboardButton("• إغلاق •", callback_data="menu_close"))
    return markup

def get_section_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("• رجوع •", callback_data="menu_main"))
    markup.add(InlineKeyboardButton("• إغلاق •", callback_data="menu_close"))
    return markup

COMMANDS_TEXT = {
    "menu_lock": "• القفل والفتح 🔒\nقفل امر X / فتح امر X",
    "menu_toggle": "• التفعيل والتعطيل ⚙️",
    "menu_fun": "• التسلية والخدمية 🎮\n\nرتبتي / رتبته / المتفاعلين مع منشن ازرق\nالاوامر - قائمة الاوامر",
    "menu_admin": "• ادارة القروب 👮‍♂️\nرفع مميز, ادمن, مدير, منشئ, مالك, M, MY, Dev\nتقييد / مق / كتم (بالرد)",
    "menu_dev": "• اوامر Dev 🛠️\nاضف امر X -> Y\n{الاسم} {الرتبة} {التفاعل}",
    "menu_settings": "• الإعدادات ⚙️"
}

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        data = call.data
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        if data == "menu_close":
            try:
                bot.delete_message(chat_id, msg_id)
            except:
                bot.edit_message_text("تم الإغلاق •", chat_id, msg_id)
            return
        if data == "p_main":
            txt = f"👋 اهلا يا {call.from_user.first_name}\n\n✅ نظيف من A_ToolsX و TucosProfit\n• اوامرك: {len(custom)}\n• مقفلة: {len(locked)}"
            bot.edit_message_text(txt, chat_id, msg_id, reply_markup=get_private_menu())
            return
        if data == "p_clean_ok":
            bot.edit_message_text("✅ البوت نظيف 100% - ما فيه اي قناة\n\nجرب:\n• رتبتي\n• /start\n• المتفاعلين\n• الاوامر\n\nكلها بدون قناة", chat_id, msg_id, reply_markup=get_private_back())
            return
        if data == "p_add":
            bot.edit_message_text("➕ اضف امر:\nاضف امر X -> Y\nمثال: اضف امر هلا -> يا هلا {الاسم}", chat_id, msg_id, reply_markup=get_private_back())
            return
        if data == "p_del":
            bot.edit_message_text("➖ احذف امر: اسم الامر", chat_id, msg_id, reply_markup=get_private_back())
            return
        if data == "p_my":
            txt = f"📜 اوامرك ({len(custom)}):\n" + "\n".join([f"• {k}" for k in list(custom.keys())[:30]]) if custom else "ما عندك اوامر - نظيف ✅\n\nالحين تقدر تضيف من جديد بدون قناة"
            bot.edit_message_text(txt, chat_id, msg_id, reply_markup=get_private_back())
            return
        if data == "p_locks":
            txt = f"🔒 مقفلة ({len(locked)}):\n" + "\n".join([f"• {k} → {v}" for k,v in locked.items()]) if locked else "ما فيه مقفلة"
            bot.edit_message_text(txt, chat_id, msg_id, reply_markup=get_private_back())
            return
        if data == "p_files":
            txt = f"📁 BASE: {BASE_DIR}\n"
            for p in [FILE, LOCK_FILE, RANKS_FILE, TOP_FILE, SETTINGS_FILE]:
                exists = "✅" if os.path.exists(p) else "❌"
                txt += f"{exists} {os.path.basename(p)}\n"
            txt += f"\n{'✅ /data موجود - دائم' if os.path.exists('/data') else '❌ /data مو موجود - لازم Disk'}"
            txt += "\n\n✅ تم حذف كل ملفات القنوات الفاسدة"
            bot.edit_message_text(txt, chat_id, msg_id, reply_markup=get_private_back())
            return
        if data == "menu_main":
            if chat_id < 0:
                bot.edit_message_text("قائمة الاوامر", chat_id, msg_id, reply_markup=get_main_menu())
            else:
                bot.edit_message_text(f"👋 اهلا - نظيف ✅\n• اوامرك: {len(custom)}", chat_id, msg_id, reply_markup=get_private_menu())
            return
        if data in COMMANDS_TEXT:
            bot.edit_message_text(COMMANDS_TEXT[data], chat_id, msg_id, reply_markup=get_section_keyboard())
            return
    except Exception as e:
        print(f"callback error: {e}")

waiting_alias = {}
waiting = {}
pending = {}
waiting_rank = {}

# ===== اهم شي - اوامر التنظيف لها اولوية قبل custom =====
@bot.message_handler(chat_types=['private'],func=lambda m:m.from_user.id==OWNER_BOT_ID,content_types=['text'])
def private_handler(m):
    uid=m.from_user.id
    txt=(m.text or "").strip()

    # اوامر التنظيف - اولوية قصوى - حتى لو موجودة في custom
    if txt in ["/start","القائمة","القائمه","قائمتي","start","menu","الاوامر","اوامري","نظف","مسح كل الاوامر","تنظيف","نظف كل شي","امسح كل شي"]:
        if txt in ["مسح كل الاوامر","تنظيف","نظف كل شي","امسح كل شي","نظف"]:
            custom.clear()
            locked.clear()
            save_custom()
            save_locked()
            # احذف الملفات فعليا
            for p in [FILE, "/data/custom_commands.json", "/opt/render/project/src/custom_commands.json"]:
                try:
                    if os.path.exists(p):
                        os.remove(p)
                        with open(p,'w',encoding='utf-8') as wf:
                            json.dump({}, wf)
                except:
                    pass
            bot.reply_to(m, "🧹 تم مسح كل الاوامر الفاسدة ✅\n\nالحين البوت نظيف 100%\n\nجرب:\n• رتبتي\n• المتفاعلين\n• الاوامر\n\nكلها بدون قناة")
            return
        welcome = f"👋 اهلا يا {m.from_user.first_name} ²⁷\n\n✅ البوت نظيف - تم حذف A_ToolsX و TucosProfit\n\n• اوامرك: {len(custom)}\n• مقفلة: {len(locked)}"
        bot.send_message(m.chat.id, welcome, reply_markup=get_private_menu())
        return

    if txt == "اضف امر":
        waiting_alias[uid] = {"step":"wait_old", "chat_type":"private"}
        bot.reply_to(m, "≡ ارسل لي الامر القديم ...\n-")
        return

    if uid in waiting_alias and waiting_alias[uid]["chat_type"]=="private":
        step = waiting_alias[uid]["step"]
        if step=="wait_old":
            waiting_alias[uid]["old"] = txt
            waiting_alias[uid]["step"] = "wait_new"
            bot.reply_to(m, "≡ ارسل الامر الجديد عشان احطه مكان القديم\n-")
            return
        elif step=="wait_new":
            new = txt
            old = waiting_alias[uid].get("old")
            if old:
                if old in custom:
                    custom[new] = custom[old].copy() if isinstance(custom[old], dict) else custom[old]
                else:
                    custom[new] = {"type":"alias", "target":old, "text":old}
                save_custom()
                bot.reply_to(m, f"≡ تم حفظ الامر باسم ( {new} ) ✓\n-")
            del waiting_alias[uid]
            return

    if txt.startswith("قفل امر "):
        cmd_text = txt.replace("قفل امر ","").strip()
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
        bot.reply_to(m, f"≡ حسنًا عزيزي قم بإرسال الرتبة الان")
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
        if not tmp:
            return
        if "->" in tmp:
            a,b=tmp.split("->",1)
            trig=a.strip(); resp=b.strip()
            if trig and resp:
                if "t.me" in resp or "A_Tools" in resp or "Tucos" in resp or "join our channel" in resp.lower():
                    bot.reply_to(m, "❌ هذا الامر فيه قناة - ممنوع")
                    return
                data={"type":"text","text":resp,"entities":save_entities(m)}
                pending[uid]={"t":trig,"data":data}
                bot.reply_to(m,f"تمام - الامر: {trig}\nاكتب: ارفعه")
                return
        else:
            cmd=tmp
            waiting[uid]={"step":"wait_reply","command":cmd, "type":"normal"}
            bot.reply_to(m,f"تمام - الامر: {cmd}\nارسل الشكل")
            return

    if uid in waiting and waiting[uid]['step']=='wait_reply' and waiting[uid].get('type')=='normal':
        cmd=waiting[uid]['command']
        if "t.me" in (m.text or "") or "A_Tools" in (m.text or "") or "Tucos" in (m.text or "") or "join our channel" in (m.text or "").lower():
            bot.reply_to(m, "❌ هذا الشكل فيه قناة - ممنوع")
            return
        data={"type":"text","text":m.text,"entities":save_entities(m)}
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
        bot.reply_to(m,f"✅ حفظت {t} - نظيف بدون قناة")
        return

    if txt.startswith("احذف امر"):
        cmd=txt.replace("احذف امر:","").replace("احذف امر","").strip()
        if not cmd:
            bot.reply_to(m, "اكتب: احذف امر: اسم الامر")
            return
        # منع حذف اوامر التنظيف نفسها
        if cmd in ["مسح كل الاوامر","تنظيف","/start","القائمة"]:
            bot.reply_to(m, "❌ هذا امر نظام - ما ينحذف")
            return
        if cmd in custom:
            del custom[cmd]
            save_custom()
            bot.reply_to(m,f"✅ حذفت {cmd}")
        else:
            found=False
            for k in list(custom.keys()):
                if cmd in k or k in cmd:
                    del custom[k]
                    found=True
            if found:
                save_custom()
                bot.reply_to(m,f"✅ حذفت اوامر مشابهة لـ {cmd}")
            else:
                bot.reply_to(m,f"❌ {cmd} مو موجود - البوت نظيف اصلا")
        return

@bot.message_handler(content_types=['left_chat_member'])
def on_left(m):
    try:
        left_user = m.left_chat_member
        if left_user and left_user.id == OWNER_BOT_ID:
            name = left_user.first_name or "المطور"
            rank_badge = get_rank_with_badge(left_user.id, m.chat.id)
            cnt, pos = get_stats(m.chat.id, left_user.id)
            raw_msg = settings.get("leave_dev_msg", "≡ المطور غادر المجموعه 💔\n≡ {الاسم} ← {الرتبة}\n-")
            final_msg = smart_replace(raw_msg, name, "Dev", rank_badge, cnt, pos)
            bot.send_message(m.chat.id, final_msg)
    except:
        pass

def handle_builtin_restrict(m):
    try:
        if not m.reply_to_message:
            bot.reply_to(m, "رد على الشخص واكتب تقييد / مق")
            return
        target_id = m.reply_to_message.from_user.id
        bot.restrict_chat_member(m.chat.id, target_id, can_send_messages=False, until_date=int(time.time())+3600)
        safe = html.escape(m.reply_to_message.from_user.first_name or "الشخص")
        mention = f'<a href="tg://user?id={target_id}">{safe}</a>'
        bot.send_message(m.chat.id, f"≡ تم تقييد المستخدم {mention} ✓", parse_mode="HTML", reply_to_message_id=m.message_id)
    except Exception as e:
        bot.reply_to(m, f"❌ ما قدرت اقيده - تأكد ان البوت مشرف")

@bot.message_handler(content_types=['text','photo','sticker','animation','video','voice','document','audio'])
def groups(m):
    if m.chat.type=='private':
        return
    text=(m.text or m.caption or "").strip()
    chat_id=m.chat.id
    user_id=m.from_user.id
    first_name=m.from_user.first_name or "شخص"

    # اولوية قصوى - اوامر النظام قبل custom
    if text in ["الاوامر","اوامر","قائمة الاوامر","/start","رتبتي","رتبتي ²⁷","رتبته","المتفاعلين","مت","توب","تقييد","مق","كتم"]:
        if text in ["الاوامر","اوامر","قائمة الاوامر"]:
            bot.send_message(chat_id, "قائمة الاوامر\n\n─────────────\n\n• اختر القسم وبتطلع لك اوامره", reply_markup=get_main_menu(), reply_to_message_id=m.message_id)
            return
        if text in ["المتفاعلين","مت","توب","متفاعلين"]:
            top_txt = get_top_list_mention(chat_id, user_id)
            bot.send_message(chat_id, top_txt, parse_mode="HTML", reply_to_message_id=m.message_id)
            return
        if text in ["تقييد","كتم","مق","اسكات"]:
            if get_level(user_id, chat_id) < RANK_ORDER.get("ادمن",2) and user_id!=OWNER_BOT_ID:
                return
            handle_builtin_restrict(m)
            return
        if text in ["رتبتي","رتبتي ²⁷","رتبته","رتبته ²⁷","رتبه","رتبة"]:
            target_id = user_id
            target_name = first_name
            is_ratbto = text in ["رتبته","رتبته ²⁷","رتبه","رتبة"]
            if is_ratbto:
                if not m.reply_to_message:
                    bot.reply_to(m,"سوي ريبلاي على الشخص واكتب: رتبته")
                    return
                target_id=m.reply_to_message.from_user.id
                target_name=m.reply_to_message.from_user.first_name or "الشخص"
            rank_badge=get_rank_with_badge(target_id,chat_id)
            cnt,pos=get_stats(chat_id,target_id)
            safe = html.escape(target_name)
            mention = f'<a href="tg://user?id={target_id}">{safe}</a>'
            bot.send_message(chat_id, f"≡ رتبة {mention} هي ← {rank_badge}\n≡ رسائله ← {cnt}\n≡ ترتيبه ← {pos}\n-", parse_mode="HTML", reply_to_message_id=m.message_id)
            return

    try:
        add_count(chat_id,user_id,first_name)
    except:
        pass

    key_alias = f"{chat_id}_{user_id}"
    if text == "اضف امر":
        if get_level(user_id, chat_id) < RANK_ORDER.get("ادمن",2) and user_id!=OWNER_BOT_ID:
            bot.reply_to(m, "❌ تحتاج ادمن")
            return
        waiting_alias[key_alias] = {"step":"wait_old", "chat_type":"group", "chat_id":chat_id, "user_id":user_id}
        bot.reply_to(m, "≡ ارسل لي الامر القديم ...\n-")
        return

    if key_alias in waiting_alias:
        step = waiting_alias[key_alias]["step"]
        if step=="wait_old":
            waiting_alias[key_alias]["old"] = text
            waiting_alias[key_alias]["step"] = "wait_new"
            bot.reply_to(m, "≡ ارسل الامر الجديد عشان احطه مكان القديم\n-")
            return
        elif step=="wait_new":
            new = text
            old = waiting_alias[key_alias].get("old")
            if old:
                if old in custom:
                    custom[new] = custom[old].copy() if isinstance(custom[old], dict) else custom[old]
                else:
                    custom[new] = {"type":"alias", "target":old, "text":old}
                save_custom()
                bot.reply_to(m, f"≡ تم حفظ الامر باسم ( {new} ) ✓\n-")
            del waiting_alias[key_alias]
            return

    if text.startswith("قفل امر "):
        if get_level(user_id,chat_id) < 12 and user_id!=OWNER_BOT_ID:
            bot.reply_to(m,"❌ فقط Dev")
            return
        cmd_text = text.replace("قفل امر ","").strip()
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
        bot.reply_to(m, f"≡ حسنًا عزيزي قم بإرسال الرتبة الان")
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
            safe_tname = html.escape(target_name)
            mention = f'<a href="tg://user?id={target_id}">{safe_tname}</a>'
            full_cmd = f"رفع {rank_name}"
            if full_cmd in custom:
                data=custom[full_cmd]
                raw = data.get("text","") or ""
                if "A_Tools" in raw or "Tucos" in raw or "t.me" in raw or "To use this bot" in raw:
                    raw = "≡ المستخدم ذا 「 {الاسم} 」\n≡ تم رفعه ✓\n≡ رتبته ← {الرتبة}"
                final = smart_replace(raw, target_name, rank_name, rank_badge, cnt, pos)
                final = re.sub(r"「\s*」", f"「 {target_name} 」", final)
                final_html = final.replace(target_name, mention) if target_name in final else final
                if mention not in final_html and "「" in final_html:
                    final_html = re.sub(r"「[^」]*」", f"「 {mention} 」", final_html, count=1)
                bot.send_message(chat_id, final_html, parse_mode="HTML", reply_to_message_id=m.message_id)
            else:
                bot.send_message(chat_id, f'≡ المستخدم ذا 「 {mention} 」\n≡ تم رفعه ✓\n≡ رتبته ← {rank_badge}\n≡ تفاعله ← {cnt}', parse_mode="HTML", reply_to_message_id=m.message_id)
            return

    if text.startswith("تنزيل ") and m.reply_to_message:
        target_id=m.reply_to_message.from_user.id
        cs=str(chat_id); us=str(target_id)
        if cs in user_ranks and us in user_ranks[cs]:
            del user_ranks[cs][us]
            save_ranks()
            safe = html.escape(m.reply_to_message.from_user.first_name or "الشخص")
            mention = f'<a href="tg://user?id={target_id}">{safe}</a>'
            bot.send_message(chat_id, f"✅ تم تنزيل {mention}", parse_mode="HTML", reply_to_message_id=m.message_id)
        return

    if text in custom:
        if text in locked:
            req = locked[text]
            if get_level(user_id,chat_id) < RANK_ORDER.get(req,0) and user_id!=OWNER_BOT_ID:
                bot.reply_to(m,f"❌ امر {text} مقفول لرتبة {req} فقط")
                return
        data=custom[text]
        if isinstance(data, dict) and data.get("type")=="alias":
            target = data.get("target","")
            if target in ["تقييد","كتم","مق","اسكات"]:
                handle_builtin_restrict(m)
                return
        tname = first_name
        t_id = user_id
        if m.reply_to_message:
            tname = m.reply_to_message.from_user.first_name or "الشخص"
            t_id = m.reply_to_message.from_user.id
        if isinstance(data,dict):
            raw_text = data.get("text","")
            if raw_text:
                if "A_Tools" in raw_text or "Tucos" in raw_text or "To use this bot" in raw_text or "join our channel" in raw_text.lower():
                    del custom[text]
                    save_custom()
                    return
                rank_badge=get_rank_with_badge(t_id,chat_id)
                cnt,pos=get_stats(chat_id,t_id)
                final_text = smart_replace(raw_text, tname, get_rank(t_id,chat_id), rank_badge, cnt, pos)
                final_text = re.sub(r"「\s*」", f"「 {tname} 」", final_text)
                if tname in final_text:
                    safe = html.escape(tname)
                    mention = f'<a href="tg://user?id={t_id}">{safe}</a>'
                    final_html = final_text.replace(tname, mention)
                    bot.send_message(chat_id, final_html, parse_mode="HTML", reply_to_message_id=m.message_id)
                else:
                    bot.send_message(chat_id, final_text, reply_to_message_id=m.message_id)
                return

print(f"READY - FORCE CLEAN - NO CHANNEL EVER")

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
