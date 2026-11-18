
import os, json, threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask

BOT_TOKEN = "8769832522:AAHmQBlu9xZTw-WWks17nHNrvgT8D4YXkNY"
OWNER_ID = 829238313

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)
app = Flask(__name__)
@app.route('/')
def home(): return 'OK'

DATA_DIR = "/data" if os.path.exists("/data") else "."
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(n,d):
    p=os.path.join(DATA_DIR,n)
    if not os.path.exists(p):
        with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False)
        return d
    try:
        with open(p,'r',encoding='utf-8') as f: return json.load(f)
    except: return d
def save_json(n,d):
    p=os.path.join(DATA_DIR,n)
    with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

custom_commands = load_json("custom_commands.json", {})
interactions = load_json("interactions.json", {})
ranks = load_json("ranks.json", {})

# حالة الصلاحيات المؤقتة: chat_id -> target_id -> perms dict
pending_perms = {}

DEFAULT_PERMS = {
    "change_info": False,
    "delete_messages": True,
    "restrict_members": True,
    "invite_users": True,
    "pin_messages": True,
    "manage_video_chats": True,
    "manage_tags": True,
    "post_stories": False,
    "edit_stories": False,
    "delete_stories": False,
    "promote_members": False,
}

def get_perms(chat_id, target_id):
    key = f"{chat_id}_{target_id}"
    if key not in pending_perms:
        pending_perms[key] = DEFAULT_PERMS.copy()
    return pending_perms[key]

def build_panel(chat_id, target_id, target_name):
    perms = get_perms(chat_id, target_id)
    markup = InlineKeyboardMarkup(row_width=1)
    
    # زر كامل
    markup.add(InlineKeyboardButton("رفع بكامل الصلاحيات", callback_data=f"pfull:{chat_id}:{target_id}"))
    
    # ترجمة
    labels = {
        "change_info": "تغيير المعلومات",
        "delete_messages": "حذف الرسائل",
        "restrict_members": "حظر وتقييد الاعضاء",
        "invite_users": "دعوة المستخدمين",
        "pin_messages": "تثبيت الرسائل",
        "manage_video_chats": "ادارة المكالمات",
        "manage_tags": "ادارة الوسوم",
        "post_stories": "نشر القصص",
        "edit_stories": "تعديل القصص",
        "delete_stories": "حذف القصص",
        "promote_members": "اضافة مشرفين",
    }
    
    for k, label in labels.items():
        val = "نعم" if perms[k] else "لا"
        markup.add(InlineKeyboardButton(f"{label} : {val}", callback_data=f"ptog:{k}:{chat_id}:{target_id}"))
    
    markup.add(InlineKeyboardButton("✅ تنفيذ الرفع", callback_data=f"pdo:{chat_id}:{target_id}"))
    markup.add(InlineKeyboardButton("تنزيل من الاشراف", callback_data=f"pdem:{chat_id}:{target_id}"))
    
    row = [InlineKeyboardButton("لوحة التحكم", callback_data=f"pboard:{chat_id}:{target_id}"), InlineKeyboardButton("اغلاق", callback_data=f"pclose:{chat_id}:{target_id}")]
    markup.add(*row)
    
    text = f"• اضغط على اي صلاحية تفعّلها او توقفها\n\nالمستهدف: {target_name}\nID: {target_id}\n"
    return text, markup

def format_custom(text, user, chat_id):
    name = user.first_name or "مستخدم"
    rank = ranks.get(str(chat_id), {}).get(str(user.id), "عضو")
    if str(user.id) == str(OWNER_ID): rank = "MY"
    count = interactions.get(str(chat_id), {}).get(str(user.id), 0)
    # order
    sorted_users = sorted(interactions.get(str(chat_id), {}).items(), key=lambda x: x[1], reverse=True)
    order = 1
    for i,(uid,cnt) in enumerate(sorted_users,1):
        if uid == str(user.id): order=i; break
    mention = f"[{name}](tg://user?id={user.id})"
    repl = {"{الاسم}":mention,"{فلان}":mention,"الاسم":mention,"فلان":mention,"{الرتبة}":rank,"الرتبة":rank,"{التفاعل}":str(count),"التفاعل":str(count),"{الترتيب}":str(order),"الترتيب":str(order)}
    for k,v in repl.items(): text=text.replace(k,v)
    return text

@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "✅ البوت شغال", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.chat.type == 'private')
def priv(m):
    if m.text and m.text.startswith('/start'): return
    if m.from_user.id != OWNER_ID: return
    txt=(m.text or "").strip()
    if txt in ["اضف امر","/اضف_امر"]:
        msg=bot.reply_to(m,"اسم الامر"); bot.register_next_step_handler(msg, add1); return
    if txt.startswith("حذف امر"):
        n=txt.split()[2] if len(txt.split())>2 else txt.split()[1] if len(txt.split())>1 else ""
        if n in custom_commands: del custom_commands[n]; save_json("custom_commands.json", custom_commands); bot.reply_to(m,f"حذف {n}")
        return
    if txt in custom_commands:
        bot.reply_to(m, format_custom(custom_commands[txt], m.from_user, m.chat.id), parse_mode="Markdown")

def add1(m):
    cmd=m.text.strip()
    msg=bot.reply_to(m,f"الامر {cmd}\nارسل الرد"); bot.register_next_step_handler(msg, lambda x: add2(x,cmd))
def add2(m,cmd):
    custom_commands[cmd]=m.text; save_json("custom_commands.json", custom_commands); bot.reply_to(m,f"تم {cmd}")

@bot.message_handler(func=lambda m: m.chat.type in ['group','supergroup'])
def groups(m):
    if not m.text: return
    txt=m.text.strip()
    # تفاعل
    cid=str(m.chat.id); uid=str(m.from_user.id)
    if cid not in interactions: interactions[cid]={}
    interactions[cid][uid]=interactions[cid].get(uid,0)+1
    save_json("interactions.json", interactions)
    
    # اوامر مخصصة
    if txt in custom_commands:
        bot.reply_to(m, format_custom(custom_commands[txt], m.from_user, m.chat.id), parse_mode="Markdown")
        return
    
    # رفع مشرف - بالرد
    if txt in ["رفع مشرف","رفع مشرف ²⁷","رفع مشرف جديد","رفع ادمن"]:
        target = None
        target_name = ""
        if m.reply_to_message:
            target = m.reply_to_message.from_user
        else:
            # اذا معه يوزر
            parts = txt.split()
            if len(parts)>2 and parts[2].startswith('@'):
                # يحتاج بحث - نستخدم الرد فقط للبساطة
                bot.reply_to(m, "↦ رد على رسالة الشخص اللي تبي ترفعه واكتب `رفع مشرف`", parse_mode="Markdown")
                return
            else:
                bot.reply_to(m, "↦ رد على رسالة الشخص اللي تبي ترفعه واكتب `رفع مشرف`", parse_mode="Markdown")
                return
        
        if target:
            if target.id == bot.get_me().id:
                bot.reply_to(m, "ما اقدر ارفع نفسي")
                return
            # تحقق البوت مشرف
            try:
                bot_me = bot.get_chat_member(m.chat.id, bot.get_me().id)
                if not bot_me.status in ['administrator','creator'] or not getattr(bot_me,'can_promote_members',False):
                    bot.reply_to(m, "❌ انا مو مشرف او ما عندي صلاحية اضافة مشرفين\nفعل لي صلاحية `اضافة مشرفين` اول")
                    return
            except Exception as e:
                print(e)
            
            t, markup = build_panel(m.chat.id, target.id, target.first_name)
            bot.reply_to(m, t, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('p'))
def callback_perms(c):
    try:
        data=c.data
        chat_id = c.message.chat.id
        
        if data.startswith("ptog:"):
            # ptog:key:chat:target
            _, key, ch, targ = data.split(':',3)
            perms = get_perms(ch, targ)
            perms[key] = not perms[key]
            t, markup = build_panel(ch, targ, f"ID {targ}")
            bot.edit_message_text(t, chat_id, c.message.message_id, reply_markup=markup)
            bot.answer_callback_query(c.id, f"{key} = {'نعم' if perms[key] else 'لا'}")
        
        elif data.startswith("pfull:"):
            _, ch, targ = data.split(':',2)
            perms = get_perms(ch, targ)
            for k in perms: perms[k]=True
            t, markup = build_panel(ch, targ, f"ID {targ}")
            bot.edit_message_text(t, chat_id, c.message.message_id, reply_markup=markup)
            bot.answer_callback_query(c.id, "تم تفعيل الكل")
        
        elif data.startswith("pdo:"):
            _, ch, targ = data.split(':',2)
            perms = get_perms(ch, targ)
            ch=int(ch); targ=int(targ)
            try:
                bot.promote_chat_member(
                    ch, targ,
                    can_change_info=perms["change_info"],
                    can_delete_messages=perms["delete_messages"],
                    can_restrict_members=perms["restrict_members"],
                    can_invite_users=perms["invite_users"],
                    can_pin_messages=perms["pin_messages"],
                    can_promote_members=perms["promote_members"],
                    can_manage_video_chats=perms["manage_video_chats"],
                    can_post_stories=perms["post_stories"],
                    can_edit_stories=perms["edit_stories"],
                    can_delete_stories=perms["delete_stories"],
                )
                # حفظ رتبة
                cid=str(ch); uid=str(targ)
                if cid not in ranks: ranks[cid]={}
                ranks[cid][uid]="مشرف"
                save_json("ranks.json", ranks)
                bot.edit_message_text(f"✅ تم رفع [{targ}](tg://user?id={targ}) مشرف بالصلاحيات المحددة", chat_id, c.message.message_id, parse_mode="Markdown")
                bot.answer_callback_query(c.id, "تم الرفع")
            except Exception as e:
                bot.answer_callback_query(c.id, f"خطأ: {e}", show_alert=True)
        
        elif data.startswith("pdem:"):
            _, ch, targ = data.split(':',2)
            ch=int(ch); targ=int(targ)
            try:
                bot.promote_chat_member(ch, targ, can_change_info=False, can_delete_messages=False, can_restrict_members=False, can_invite_users=False, can_pin_messages=False, can_promote_members=False)
                cid=str(ch); uid=str(targ)
                if cid in ranks and uid in ranks[cid]: del ranks[cid][uid]; save_json("ranks.json", ranks)
                bot.edit_message_text(f"✅ تم تنزيل [{targ}](tg://user?id={targ}) من الاشراف", chat_id, c.message.message_id, parse_mode="Markdown")
            except Exception as e:
                bot.answer_callback_query(c.id, f"خطأ: {e}", show_alert=True)
        
        elif data.startswith("pclose:"):
            bot.delete_message(chat_id, c.message.message_id)
        
        elif data.startswith("pboard:"):
            bot.answer_callback_query(c.id, "لوحة التحكم - قريبا")
    
    except Exception as e:
        print(f"callback error {e}")

def run_bot():
    print("READY PROMOTE REAL")
    bot.remove_webhook()
    try: print(f"@{bot.get_me().username}")
    except: pass
    bot.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)), use_reloader=False), daemon=True).start()
    run_bot()
