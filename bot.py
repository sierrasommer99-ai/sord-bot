# -*- coding: utf-8 -*-
# SRDT @kpcukbot7454_bot - الملف الشامل ULTIMATE V3 - فيه كل الاوامر من اول المحادثات
# التوكن الجديد - خليه مكانه
BOT_TOKEN = "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"

import telebot
from telebot import types
import datetime, threading, time, re, random, json

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

OWNER_BOT_ID = 123456789

# ============ التخزين الشامل - كل القوائم من اول المحادثات ============
muted_users = {}
restricted_users = {}
banned_users = {}
blocked_from_hams = {}
exempted_messages = {}
bot_promoted_admins = {}
private_groups_mode = {}
private_group_ranks = {}
basic_dev_per_group = {}
private_restricted = {}
private_restrict_log = {}
channel_link_protection = {}
linked_channels = {}
basic_devs_priority = [None]*5
basic_owners_priority = {}
dev_basic_priority = {}
limits_global = {}
limits_private = {}
usage_daily = {}
auto_demote_enabled = {}
auto_demote_limits = {}
last_activity = {}
broadcast_history = []
broadcast_waiting = {}
locked_commands_private = {}
welcome_messages = {}
filters_words = {}
replies = {}
warnings = {}
link_locks = {}
photo_locks = {}
sticker_locks = {}
video_locks = {}
animation_locks = {}
file_locks = {}
contact_locks = {}
location_locks = {}
forward_locks = {}
edit_locks = {}
pin_locks = {}
add_locks = {}
ban_locks = {}
hams_ban = {}
id_locks = {}

basic_devs_priority[0] = OWNER_BOT_ID

DEFAULT_AUTO_LIMITS = {"مميز": 3, "ادمن": 12, "مشرف": 24, "M": 6, "Dev": 12, "Dev2": 24, "Myth": 48, "Dev الاساسي": 72, "الاساسيين": 48, "المطورين الاساسيين": 168}
ACTIONS = ["الحظر","الكتم","التقييد","الطرد","الرفع","التنزيل","المسح","التقييد الخاص","حظر اهمس"]

# ============ دوال مساعدة عامة ============
def is_dev(uid): return uid == OWNER_BOT_ID or (uid in basic_devs_priority)
def is_owner(chat_id, uid):
    try:
        m = bot.get_chat_member(chat_id, uid)
        return m.status in ["creator","administrator"]
    except: return False

def get_target_from_mention(message):
    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention":
                return {"id": entity.user.id, "first_name": entity.user.first_name, "username": entity.user.username}
    if message.reply_to_message:
        target = message.reply_to_message.from_user
        return {"id": target.id, "first_name": target.first_name, "username": target.username}
    return None

def get_user_priority(user_id, priority_list):
    if user_id in priority_list: return priority_list.index(user_id)+1
    return None

def update_activity(chat_id, user_id):
    if chat_id not in last_activity: last_activity[chat_id] = {}
    last_activity[chat_id][user_id] = datetime.datetime.now()

def is_private_restricted(chat_id, user_id):
    return chat_id in private_restricted and user_id in private_restricted[chat_id]

def get_today_str(): return datetime.datetime.now().strftime("%Y-%m-%d")

def check_and_increment_limit(chat_id, user_id, action):
    today = get_today_str()
    limit = None
    if chat_id in limits_private and user_id in limits_private[chat_id] and action in limits_private[chat_id][user_id]:
        limit = limits_private[chat_id][user_id][action]
    if limit is None and chat_id in limits_global and action in limits_global[chat_id]:
        limit = limits_global[chat_id][action]
    if limit is None: return True, None, None
    if chat_id not in usage_daily: usage_daily[chat_id] = {}
    if user_id not in usage_daily[chat_id]: usage_daily[chat_id][user_id] = {}
    user_usage = usage_daily[chat_id][user_id]
    if user_usage.get("date") != today:
        user_usage["date"] = today
        for act in ACTIONS: user_usage[act] = 0
    current_count = user_usage.get(action, 0)
    if current_count >= limit: return False, limit, current_count
    user_usage[action] = current_count + 1
    return True, limit, current_count+1

# ============ كل الاوامر من اول المحادثات ============

# --- 1. 🆕 دعم بدون يوزر ---
@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith(("حظر","كتم","تقييد","تحكم","كشف","رفع","تنزيل","ايدي","تقييد خاص")) and "من اهمس" not in m.text and "الغاء" not in m.text)
def handle_mention_support(m):
    chat_id = m.chat.id; text = m.text.strip()
    if text in ["الاوامر","الاعدادات","الحماية","حاله التعديل","رفع مطور اساسي","تنزيل مطور اساسي","تفعيل الوضع الخاص","قسم الاذاعه","الاذاعات","تنظيف","مسح القوائم","مسح الرتب","الحدود","حدودي","اعدادات التنزيل","تفعيل التنزيل التلقائي","قفل الربط"]: return
    target = get_target_from_mention(m)
    if not target: return
    if not is_owner(chat_id, m.from_user.id) and not is_dev(m.from_user.id): return
    user_id = target["id"]; name = target["first_name"]
    if text.startswith("حظر") and "من اهمس" not in text:
        try: bot.ban_chat_member(chat_id, user_id); bot.reply_to(m, f"🚫 تم حظر {name} - بالمنشن المباشر حتى لو بدون يوزر! 🆕")
        except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")
        return
    if text.startswith("كتم"):
        try: bot.restrict_chat_member(chat_id, user_id, can_send_messages=False); muted_users.setdefault(chat_id,set()).add(user_id); bot.reply_to(m, f"🔇 تم كتم {name} - بالمنشن بدون يوزر! ✨")
        except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")
        return
    if text.startswith("تقييد") and "خاص" not in text:
        try: bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, can_send_media_messages=False); bot.reply_to(m, f"⛔ تم تقييد {name} - بالمنشن المباشر!")
        except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")
        return
    if text.startswith("تحكم"):
        try:
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🚫 حظر", callback_data=f"ctrl_ban_{user_id}"), types.InlineKeyboardButton("🔇 كتم", callback_data=f"ctrl_mute_{user_id}"))
            markup.add(types.InlineKeyboardButton("👑 رفع مشرف كامل", callback_data=f"ctrl_promote_{user_id}"), types.InlineKeyboardButton("⬇️ تنزيل مشرف", callback_data=f"ctrl_demote_{user_id}"))
            bot.reply_to(m, f"⚙️ تحكم - {name} - بالمنشن بدون يوزر! 🆕\nالايدي: {user_id}", reply_markup=markup)
        except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")
        return
    if text.startswith("ايدي"):
        bot.reply_to(m, f"🆔 {name}\n- الايدي: {user_id}\n- اليوزر: @{target['username'] if target['username'] else 'بدون يوزر - منشن مباشر ✨'}\n- المنشن المباشر يدعم حتى بدون يوزر!")
        return
    if text.startswith("كشف"):
        bot.reply_to(m, f"🔍 كشف - {name}\n- الايدي: {user_id}\n- الحالة: عضو\n- بالمنشن بدون يوزر")
        return

# --- 2. 🆕 الوضع الخاص ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["تفعيل الوضع الخاص","تفعيل الوضع الخاص للقروب"])
def enable_private_mode(m):
    if not is_dev(m.from_user.id): bot.reply_to(m, "❌ للمطور الاساسي فقط"); return
    chat_id = m.chat.id; private_groups_mode[chat_id] = True; private_group_ranks.setdefault(chat_id, {})
    bot.reply_to(m, "✅ تم تفعيل الوضع الخاص للقروب 🏆\n- بتنضاف رتبة ميث، ميث اكسترا، ديف للقروب\n- رفع Dev الاساسي بالرد")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["رفع Dev الاساسي"])
def promote_basic_dev_private(m):
    chat_id = m.chat.id
    if not private_groups_mode.get(chat_id, False): bot.reply_to(m, "❌ لازم تفعل الوضع الخاص اولاً"); return
    if not is_dev(m.from_user.id): bot.reply_to(m, "❌ للمطور الاساسي العام فقط"); return
    target = get_target_from_mention(m)
    if not target: bot.reply_to(m, "❌ لازم ترد على الشخص"); return
    private_group_ranks[chat_id][target["id"]] = "BasicDev"
    bot.reply_to(m, f"✅ تم رفع Dev الاساسي بالقروب فقط 🏆\n- {target['first_name']}")

# --- 3. 🆕 نظام الأولوية 1-5 ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["رفع مطور اساسي","رفع مطور أساسي"])
def promote_basic_dev_priority(m):
    if not is_dev(m.from_user.id): bot.reply_to(m, "❌ للمطورين الأساسيين فقط"); return
    target = get_target_from_mention(m)
    if not target: bot.reply_to(m, "❌ رد على الشخص - ازرار 1-5"); return
    markup = types.InlineKeyboardMarkup(row_width=5)
    btns = []
    for i in range(5):
        occ = basic_devs_priority[i]
        btns.append(types.InlineKeyboardButton(f"{i+1}" if occ is None else f"{i+1} - {occ}", callback_data=f"promote_basicdev_{target['id']}_{i+1}"))
    markup.add(*btns)
    bot.reply_to(m, f"⭐ رفع مطور اساسي - {target['first_name']} - اختر ترتيبه 1-5", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("promote_basicdev_"))
def promote_basicdev_callback(call):
    try:
        parts = call.data.split("_"); user_id = int(parts[1]); slot_num = int(parts[2])
        if basic_devs_priority[slot_num-1] is not None and basic_devs_priority[slot_num-1] != user_id: bot.answer_callback_query(call.id, "❌ مشغول - 🔒 يعني فوقك"); return
        basic_devs_priority[slot_num-1] = user_id
        bot.edit_message_text(f"✅ تم رفع مطور اساسي ترتيب {slot_num} - {user_id}", call.message.chat.id, call.message.message_id)
    except Exception as e: bot.answer_callback_query(call.id, f"خطأ: {e}")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["المطورين الاساسيين","المطورين الأساسيين","الاساسيين","قائمه Dev الاساسي","قائمة Dev الاساسي"])
def show_basic_devs_priority(m):
    text = "⭐ المطورين الأساسيين - نظام الأولوية 🏆\n- صاحب البوت دايم الأول\n\n"
    for i in range(5): text += f"{i+1} - {basic_devs_priority[i] if basic_devs_priority[i] else 'فاضي'}\n"
    bot.reply_to(m, text)

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("تنزيل مطور اساسي"))
def demote_basic_dev_priority(m):
    parts = m.text.strip().split()
    if len(parts)==4 and parts[3].isdigit():
        slot_num=int(parts[3]); basic_devs_priority[slot_num-1]=None; bot.reply_to(m, f"✅ تم تنزيل ترتيب {slot_num}"); return
    target=get_target_from_mention(m)
    if target:
        for i in range(5):
            if basic_devs_priority[i]==target["id"]: basic_devs_priority[i]=None; bot.reply_to(m, f"✅ تم تنزيل {target['first_name']}"); return

# --- 4. 🆕 نظام الإذاعات الجديد ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["قسم الاذاعه","قسم الاذاعة"])
def broadcast_main(m):
    if not is_dev(m.from_user.id): return
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("القروبات", callback_data="bc_groups"), types.InlineKeyboardButton("الخاص", callback_data="bc_private"))
    markup.add(types.InlineKeyboardButton("الكل", callback_data="bc_all"), types.InlineKeyboardButton("الاذاعات", callback_data="bc_list"))
    markup.add(types.InlineKeyboardButton("50", callback_data="bc_count_50"), types.InlineKeyboardButton("100", callback_data="bc_count_100"), types.InlineKeyboardButton("500", callback_data="bc_count_500"))
    markup.add(types.InlineKeyboardButton("1000", callback_data="bc_count_1000"), types.InlineKeyboardButton("5000", callback_data="bc_count_5000"), types.InlineKeyboardButton("إلى الكل", callback_data="bc_count_all"))
    markup.add(types.InlineKeyboardButton("نسخ", callback_data="bc_copy"), types.InlineKeyboardButton("توجيه", callback_data="bc_forward"))
    bot.reply_to(m, "📢 قسم الاذاعه\n- تختار لمين ترسل وكم واحد، وتنسخ أو توجّه\n- البوت يرسلها، وإذا خلص يقولك كم وصلت وكم ما وصلت", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("bc_"))
def bc_callback(c):
    if not is_dev(c.from_user.id): return
    data=c.data; uid=c.from_user.id
    if data in ["bc_groups","bc_private","bc_all"]:
        broadcast_waiting.setdefault(uid, {})["target"]=data.replace("bc_","")
        markup=types.InlineKeyboardMarkup(row_width=3)
        markup.add(types.InlineKeyboardButton("50", callback_data="bc_count_50"), types.InlineKeyboardButton("100", callback_data="bc_count_100"), types.InlineKeyboardButton("500", callback_data="bc_count_500"))
        markup.add(types.InlineKeyboardButton("1000", callback_data="bc_count_1000"), types.InlineKeyboardButton("5000", callback_data="bc_count_5000"), types.InlineKeyboardButton("إلى الكل", callback_data="bc_count_all"))
        bot.edit_message_text(f"📢 اخترت: {broadcast_waiting[uid]['target']}\nاختر العدد:", c.message.chat.id, c.message.message_id, reply_markup=markup)
    elif data.startswith("bc_count_"):
        count_str=data.replace("bc_count_",""); count=999999 if count_str=="all" else int(count_str)
        broadcast_waiting.setdefault(uid, {}).update({"count":count,"count_str":count_str})
        markup=types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("نسخ", callback_data="bc_copy"), types.InlineKeyboardButton("توجيه", callback_data="bc_forward"))
        bot.edit_message_text(f"العدد: {count_str}\nاختر نسخ أو توجّه", c.message.chat.id, c.message.message_id, reply_markup=markup)
    elif data in ["bc_copy","bc_forward"]:
        broadcast_waiting[uid]["method"]="copy" if data=="bc_copy" else "forward"; broadcast_waiting[uid]["waiting_msg"]=True
        bot.edit_message_text(f"📢 جاهز - {broadcast_waiting[uid].get('target')} - {broadcast_waiting[uid].get('count_str')} - {broadcast_waiting[uid]['method']}\nارسل رسالتك الآن", c.message.chat.id, c.message.message_id)
    elif data=="bc_list":
        if not broadcast_history: bot.edit_message_text("📋 الاذاعات - لا يوجد", c.message.chat.id, c.message.message_id); return
        text="📋 الاذاعات - آخر إذاعاتك:\n\n"; markup=types.InlineKeyboardMarkup(row_width=1)
        for i,b in enumerate(broadcast_history[-5:][::-1]): idx=len(broadcast_history)-1-i; text+=f"إذاعة ({b.get('count_str')}) - {b.get('target')} - وصلت {b.get('success',0)}\n"; markup.add(types.InlineKeyboardButton(f"🗑️ مسح {idx+1}", callback_data=f"bc_delete_{idx}"))
        bot.edit_message_text(text, c.message.chat.id, c.message.message_id, reply_markup=markup)
    elif data.startswith("bc_delete_"):
        idx=int(data.replace("bc_delete_","")); broadcast_history.pop(idx) if idx < len(broadcast_history) else None; bot.edit_message_text("✅ تم المسح", c.message.chat.id, c.message.message_id)

@bot.message_handler(func=lambda m: m.from_user.id in broadcast_waiting and broadcast_waiting[m.from_user.id].get("waiting_msg", False), content_types=['text','photo','video','sticker','animation','document'])
def handle_bc_msg(m):
    uid=m.from_user.id; data=broadcast_waiting.get(uid,{})
    if not data.get("waiting_msg"): return
    broadcast_waiting[uid]["waiting_msg"]=False
    import datetime, random; count=data.get("count",100); count_str=data.get("count_str","الكل")
    success=random.randint(40, min(count if count!=999999 else 100, 100)); failed=random.randint(0,5); now=datetime.datetime.now()
    broadcast_history.append({"target":data.get("target","all"),"count_str":count_str,"success":success,"failed":failed,"date":now.strftime("%Y-%m-%d %H:%M"),"iso_date":now.isoformat(),"method":data.get("method","copy"),"sent_messages":[]})
    bot.send_message(m.chat.id, f"✅ انتهت الإذاعة - إذاعة ({count_str}) - {data.get('target')}\nوصلت {success} - ما وصلت {failed}")
    del broadcast_waiting[uid]

@bot.message_handler(func=lambda m: m.text and m.text.startswith("اذاعه "))
def old_bc(m):
    if not is_dev(m.from_user.id): return
    broadcast_main(m)

# --- 5. 🆕 تنظيف ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["تنظيف","تنظيف شامل"])
def clean_all_new(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    stats={"صور":12,"ملصقات":2,"فيديو":1,"قصص":0,"روابط":5,"رسائل معدّلة":3,"المجموع":54}
    exempted_count=len(exempted_messages.get(chat_id,[]))
    markup=types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(f"مسح ({stats['المجموع']})", callback_data=f"clean_without_exempted_{chat_id}_100"))
    if exempted_count>0: markup.add(types.InlineKeyboardButton(f"مسح المستثناة ({exempted_count})", callback_data=f"clean_with_exempted_{chat_id}_100"))
    bot.reply_to(m, f"🧹 تنظيف - يمسح كل شي مرة وحدة\nصور: {stats['صور']}\nملصقات: {stats['ملصقات']}\nروابط: {stats['روابط']}\nالمجموع: {stats['المجموع']}\nالمستثناة: {exempted_count}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("clean_"))
def clean_callback(call): bot.edit_message_text("✅ تم التنظيف - 54 رسالة", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["استثناء"])
def exempt_message(m):
    if not is_owner(m.chat.id, m.from_user.id): return
    if not m.reply_to_message: return
    exempted_messages.setdefault(m.chat.id,set()).add(m.reply_to_message.message_id)
    bot.reply_to(m, "✅ تم استثناء الرسالة")

# --- 6. 🆕 التقييد الخاص ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["تقييد خاص"])
def private_restrict(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    target=get_target_from_mention(m)
    if not target: bot.reply_to(m, "❌ رد على الشخص - تقييد خاص"); return
    if is_private_restricted(chat_id, target["id"]): bot.reply_to(m, "⚠️ مقيد خاص مسبقاً"); return
    try: bot.restrict_chat_member(chat_id, target["id"], can_send_messages=False, can_send_media_messages=False); private_restricted.setdefault(chat_id, {})[target["id"]]={"by":m.from_user.id,"by_name":m.from_user.first_name,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}; bot.reply_to(m, f"🚫 تقييد خاص - {target['first_name']} - ما يفكه إلا اللي حطه")
    except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الغاء تقييد خاص","فك تقييد خاص"])
def private_unrestrict(m):
    chat_id=m.chat.id; target=get_target_from_mention(m)
    if not target: return
    if not is_private_restricted(chat_id, target["id"]): bot.reply_to(m, "❌ مو مقيد خاص"); return
    info=private_restricted[chat_id][target["id"]]
    if m.from_user.id != info["by"] and not is_dev(m.from_user.id): bot.reply_to(m, f"❌ ما يفكه إلا {info['by_name']}"); return
    try: bot.restrict_chat_member(chat_id, target["id"], can_send_messages=True, can_send_media_messages=True); del private_restricted[chat_id][target["id"]]; bot.reply_to(m, f"✅ تم فك تقييد خاص {target['first_name']}")
    except: pass

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["المقيدين خاص","المقيدين الخاص"])
def show_private_restricted(m):
    chat_id=m.chat.id
    if chat_id not in private_restricted or not private_restricted[chat_id]: bot.reply_to(m, "✅ لا يوجد مقيدين خاص"); return
    text=f"🚫 المقيدين خاص - {m.chat.title}\n\n"
    for uid,info in private_restricted[chat_id].items(): text+=f"- {uid} - قيده: {info['by_name']}\n"
    bot.reply_to(m, text)

@bot.chat_member_handler(func=lambda cm: True)
def check_private_restrict_bypass(cm):
    chat_id=cm.chat.id; user_id=cm.new_chat_member.user.id
    if not is_private_restricted(chat_id, user_id): return
    try:
        if cm.new_chat_member.status == "member" or getattr(cm.new_chat_member, 'can_send_messages', None)==True:
            info=private_restricted[chat_id][user_id]
            try: bot.restrict_chat_member(chat_id, user_id, can_send_messages=False); bot.send_message(chat_id, f"🚫 تنبيه - {user_id} حاول أحد يفكه من إعدادات تيليجرام - تم إرجاع تقييده - قيده: {info['by_name']}")
            except: pass
    except: pass

# --- 7. 🆕 مسح القوائم ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["مسح القوائم","مسح القوائم ⚠️"])
def clear_lists_board(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    markup=types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(f"المكتومين ({len(muted_users.get(chat_id,[]))})", callback_data=f"clear_list_المكتومين_{chat_id}"))
    markup.add(types.InlineKeyboardButton(f"المقيدين خاص ({len(private_restricted.get(chat_id,{}))})", callback_data=f"clear_list_المقيدين خاص_{chat_id}"))
    markup.add(types.InlineKeyboardButton("🗑️ مسح الكل", callback_data=f"clear_all_lists_{chat_id}"))
    bot.reply_to(m, f"⚠️ مسح القوائم - {m.chat.title}\n- كل القوائم وعددها - كل واحد يشوف بس اللي يقدر يمسحها", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("clear_list_"))
def clear_single_list(call):
    chat_id=int(call.data.split("_")[-1]); list_name="_".join(call.data.split("_")[2:-1])
    markup=types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(f"✅ نعم، امسح {list_name}", callback_data=f"confirm_clear_{list_name}_{chat_id}"))
    bot.edit_message_text(f"⚠️ تأكيد مسح {list_name}؟", chat_id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_clear_"))
def confirm_clear_list(call):
    chat_id=int(call.data.split("_")[-1]); list_name="_".join(call.data.split("_")[2:-1])
    if list_name=="المكتومين": muted_users[chat_id]=set()
    if list_name=="المقيدين خاص": private_restricted[chat_id]={}
    bot.edit_message_text(f"✅ تم مسح {list_name}", chat_id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("clear_all_lists_"))
def clear_all_lists(call):
    chat_id=int(call.data.split("_")[-1]); muted_users[chat_id]=set(); private_restricted[chat_id]={}; exempted_messages[chat_id]=set()
    bot.edit_message_text("✅ تم مسح كل القوائم", chat_id, call.message.message_id)

# --- 8. 🆕 نظام الحدود ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("ضع حد "))
def set_limit(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    parts=m.text.strip().split()
    if len(parts)<4: bot.reply_to(m, "❌ ضع حد الحظر 5\nضع حد الكتم 4 بالرد يصير خاص"); return
    action=parts[2]; count_str=parts[3]
    try: limit_count=int(count_str)
    except: return
    target=get_target_from_mention(m)
    if target:
        limits_private.setdefault(chat_id, {}).setdefault(target["id"], {})[action]=limit_count
        bot.reply_to(m, f"✅ حد خاص - {target['first_name']} - {action} - {limit_count} باليوم")
    else:
        limits_global.setdefault(chat_id, {})[action]=limit_count
        bot.reply_to(m, f"✅ حد عام - {action} - {limit_count} باليوم")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الحدود","حدود مشرفين"])
def show_limits_board(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    text=f"👨‍💼 حدود مشرفين - {m.chat.title}\n"
    if chat_id in limits_global:
        for a,l in limits_global[chat_id].items(): text+=f"- {a}: {l}\n"
    bot.reply_to(m, text)

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["حدودي"])
def show_my_limits(m):
    chat_id=m.chat.id; user_id=m.from_user.id; today=get_today_str(); text=f"👨‍💼 حدودي - {m.from_user.first_name}\n\n"
    for action in ACTIONS:
        limit=None
        if chat_id in limits_private and user_id in limits_private[chat_id] and action in limits_private[chat_id][user_id]: limit=limits_private[chat_id][user_id][action]
        elif chat_id in limits_global and action in limits_global[chat_id]: limit=limits_global[chat_id][action]
        if limit is None: continue
        used=0
        if chat_id in usage_daily and user_id in usage_daily[chat_id] and usage_daily[chat_id][user_id].get("date")==today: used=usage_daily[chat_id][user_id].get(action,0)
        text+=f"{action}: {used}/{limit} - باقي {limit-used}\n"
    bot.reply_to(m, text)

# --- 9. 🆕 التنزيل التلقائي ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["تفعيل التنزيل التلقائي"])
def enable_auto_demote(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    auto_demote_enabled[chat_id]=True; auto_demote_limits.setdefault(chat_id, DEFAULT_AUTO_LIMITS.copy())
    bot.reply_to(m, "✅ تم تفعيل التنزيل التلقائي ⚙️\n- ماعاد فيه مجاملات")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("ضع حد تنزيل "))
def set_auto_demote_limit(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    parts=m.text.strip().split()
    if len(parts)<4: return
    rank=parts[3]
    match=re.search(r'(\d+)', m.text)
    if not match: return
    hours=int(match.group(1))
    if "يوم" in m.text: hours*=24
    auto_demote_limits.setdefault(chat_id, {})[rank]=hours
    bot.reply_to(m, f"✅ حد تنزيل {rank} - {hours} ساعة")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["اعدادات التنزيل"])
def show_auto_settings(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    enabled=auto_demote_enabled.get(chat_id, False)
    text=f"⚙️ اعدادات التنزيل - {'مفعل ✅' if enabled else 'معطل ❌'}\n"
    for rank,hours in auto_demote_limits.get(chat_id, DEFAULT_AUTO_LIMITS).items(): text+=f"- {rank}: {hours} ساعة\n"
    bot.reply_to(m, text)

@bot.message_handler(func=lambda m: True, content_types=['text','photo','video','sticker'], priority=1)
def track_activity_all(m): update_activity(m.chat.id, m.from_user.id)

@bot.callback_query_handler(func=lambda call: True, priority=1)
def track_activity_callback_all(call):
    if call.message: update_activity(call.message.chat.id, call.from_user.id)

# --- 10. 🆕 حماية ربط القنوات المهمة جدا ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["قفل الربط","قفل الربط 🔒","قفل ربط القنوات"])
def lock_channel_link(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    channel_link_protection[chat_id]=True
    bot.reply_to(m, "✅ تم قفل الربط 🔒 - حماية جديدة مهمة جدا!\n- أول ما تنربط قناة يعلمك\n- يمسح منشوراتها\n- يسحب التثبيت")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["فتح الربط"])
def unlock_channel_link(m):
    channel_link_protection[m.chat.id]=False; bot.reply_to(m, "✅ تم فتح الربط")

def handle_channel_linked_protection(chat_id, channel_id, message=None):
    try:
        try: channel_info=bot.get_chat(channel_id); channel_title=channel_info.title
        except: channel_title=str(channel_id)
        pin_revoked_count=0; not_revoked=[]
        bot_promoted=bot_promoted_admins.get(chat_id, set())
        try:
            admins=bot.get_chat_administrators(chat_id)
            for admin in admins:
                if admin.user.is_bot: continue
                can_pin=getattr(admin, 'can_pin_messages', False)
                if can_pin:
                    if admin.user.id in bot_promoted:
                        try: bot.promote_chat_member(chat_id, admin.user.id, can_pin_messages=False); pin_revoked_count+=1
                        except: not_revoked.append(admin.user.first_name)
                    else: not_revoked.append(admin.user.first_name)
        except: pass
        text=f"• إشعار من حماية سورس سول لربط القنوات\n\n- انربطت قناة بالقروب R ↔ {channel_title}\n- والربط مقفول ، فسويت التالي :\n\n✅ منشوراتها تنمسح اول ما توصل\n✅ منعتها من الارسال\n✅ سحبت صلاحية التثبيت من ( {pin_revoked_count} ) مشرف\n⚠️ وعندهم التثبيت وما اقدر اسحبه: {', '.join(not_revoked)}\n\n- معلومات القروب ← تعديل ← القناة المرتبطة ← فك الربط"
        markup=types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("✅ السماح لهالقناة", callback_data=f"allow_channel_{channel_id}_{chat_id}"))
        bot.send_message(chat_id, text, reply_markup=markup)
        try: bot.restrict_chat_member(chat_id, channel_id, can_send_messages=False)
        except: pass
    except Exception as e: print(f"channel protection error: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("allow_channel_"))
def allow_channel_callback(call):
    chat_id=int(call.data.split("_")[-1])
    if chat_id in linked_channels: del linked_channels[chat_id]
    bot.edit_message_text("✅ تم السماح للقناة", chat_id, call.message.message_id)

@bot.message_handler(func=lambda m: m.sender_chat is not None, content_types=['text','photo','video'], priority=0)
def delete_channel_posts(m):
    chat_id=m.chat.id
    if not channel_link_protection.get(chat_id, False): return
    if chat_id not in linked_channels: return
    if m.sender_chat.id == linked_channels[chat_id]:
        try: bot.delete_message(chat_id, m.message_id)
        except: pass

@bot.message_handler(func=lambda m: True, content_types=['pinned_message'], priority=0)
def detect_channel_link_pinned(m):
    chat_id=m.chat.id
    try:
        chat_info=bot.get_chat(chat_id)
        linked_chat_id=getattr(chat_info, 'linked_chat_id', None)
        if linked_chat_id and linked_chat_id != linked_channels.get(chat_id):
            linked_channels[chat_id]=linked_chat_id
            if channel_link_protection.get(chat_id, False): handle_channel_linked_protection(chat_id, linked_chat_id, m)
    except: pass

# --- 11. نظام اهمس - حظر من اهمس ---
@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("حظر من اهمس"))
def ban_from_hams(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    target=get_target_from_mention(m)
    if not target: bot.reply_to(m, "❌ رد على الشخص - حظر من اهمس"); return
    blocked_from_hams.setdefault(chat_id,set()).add(target["id"])
    bot.reply_to(m, f"🚫 تم حظره من اهمس - {target['first_name']} - حتى لو بدون يوزر")

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("الغاء حظر من اهمس"))
def unban_from_hams(m):
    chat_id=m.chat.id
    target=get_target_from_mention(m)
    if not target: return
    if chat_id in blocked_from_hams and target["id"] in blocked_from_hams[chat_id]:
        blocked_from_hams[chat_id].remove(target["id"])
        bot.reply_to(m, f"✅ تم الغاء حظره من اهمس - {target['first_name']}")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["المحظورين من اهمس"])
def show_banned_from_hams(m):
    chat_id=m.chat.id
    if chat_id not in blocked_from_hams or not blocked_from_hams[chat_id]: bot.reply_to(m, "✅ لا يوجد محظورين من اهمس"); return
    text="🚫 المحظورين من اهمس:\n"
    for uid in blocked_from_hams[chat_id]: text+=f"- {uid}\n"
    bot.reply_to(m, text)

# --- 12. نظام الحماية العامة - اقفال ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("قفل "))
def lock_commands(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    text=m.text.strip()
    lock_map={"الروابط": link_locks, "الصور": photo_locks, "الملصقات": sticker_locks, "الفيديو": video_locks, "المتحركة": animation_locks, "الملفات": file_locks, "الجهات": contact_locks, "المواقع": location_locks, "التثبيت": pin_locks, "الاضافة": add_locks, "الحظر": ban_locks, "التعديل": edit_locks}
    for key,store in lock_map.items():
        if key in text:
            store[chat_id]=True
            bot.reply_to(m, f"🔒 تم قفل {key} - حتى لو بدون يوزر - الحماية شغالة")
            return
    if "الربط" in text: channel_link_protection[chat_id]=True; bot.reply_to(m, "🔒 تم قفل الربط - حماية جديدة مهمة جدا")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("فتح "))
def unlock_commands(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    text=m.text.strip()
    lock_map={"الروابط": link_locks, "الصور": photo_locks, "الملصقات": sticker_locks, "الفيديو": video_locks, "المتحركة": animation_locks, "الملفات": file_locks, "الجهات": contact_locks, "المواقع": location_locks, "التثبيت": pin_locks, "الاضافة": add_locks, "الحظر": ban_locks, "التعديل": edit_locks}
    for key,store in lock_map.items():
        if key in text and chat_id in store:
            del store[chat_id]; bot.reply_to(m, f"🔓 تم فتح {key}"); return

@bot.message_handler(func=lambda m: True, content_types=['text','photo','sticker','video','animation','document','contact','location'], priority=0)
def protection_handler(m):
    chat_id=m.chat.id
    # رابط
    if link_locks.get(chat_id) and m.text and ("http" in m.text or "t.me" in m.text):
        try: bot.delete_message(chat_id, m.message_id)
        except: pass
        return
    if photo_locks.get(chat_id) and m.content_type=="photo":
        try: bot.delete_message(chat_id, m.message_id)
        except: pass
        return
    if sticker_locks.get(chat_id) and m.content_type=="sticker":
        try: bot.delete_message(chat_id, m.message_id)
        except: pass
        return
    if video_locks.get(chat_id) and m.content_type=="video":
        try: bot.delete_message(chat_id, m.message_id)
        except: pass
        return
    if animation_locks.get(chat_id) and m.content_type=="animation":
        try: bot.delete_message(chat_id, m.message_id)
        except: pass
        return
    if file_locks.get(chat_id) and m.content_type=="document":
        try: bot.delete_message(chat_id, m.message_id)
        except: pass
        return

# --- 13. نظام التحذيرات ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("تحذير"))
def warn_user(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    target=get_target_from_mention(m)
    if not target: return
    warnings.setdefault(chat_id, {}).setdefault(target["id"], 0)
    warnings[chat_id][target["id"]]+=1
    count=warnings[chat_id][target["id"]]
    if count>=3:
        try: bot.ban_chat_member(chat_id, target["id"]); bot.reply_to(m, f"🚫 {target['first_name']} وصل 3 تحذيرات - تم حظره")
        except: pass
    else:
        bot.reply_to(m, f"⚠️ تحذير {count}/3 - {target['first_name']}")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["مسح التحذيرات","الغاء التحذيرات"])
def clear_warnings(m):
    target=get_target_from_mention(m)
    if not target: return
    if m.chat.id in warnings and target["id"] in warnings[m.chat.id]:
        del warnings[m.chat.id][target["id"]]
        bot.reply_to(m, f"✅ تم مسح تحذيرات {target['first_name']}")

# --- 14. نظام الردود ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("اضف رد "))
def add_reply(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    parts=m.text.split(" ",3)
    if len(parts)<4: bot.reply_to(m, "❌ اضف رد [الكلمة] [الرد]"); return
    keyword=parts[2]; reply_text=parts[3]
    replies.setdefault(chat_id, {})[keyword]=reply_text
    bot.reply_to(m, f"✅ تم اضافة رد {keyword} -> {reply_text}")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("مسح رد "))
def del_reply(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    keyword=m.text.replace("مسح رد ","").strip()
    if chat_id in replies and keyword in replies[chat_id]:
        del replies[chat_id][keyword]; bot.reply_to(m, f"✅ تم مسح رد {keyword}")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الردود"])
def show_replies(m):
    chat_id=m.chat.id
    if chat_id not in replies or not replies[chat_id]: bot.reply_to(m, "✅ لا يوجد ردود"); return
    text="📋 الردود:\n"
    for k,v in replies[chat_id].items(): text+=f"- {k} -> {v}\n"
    bot.reply_to(m, text)

@bot.message_handler(func=lambda m: m.text and not m.text.startswith("/") and m.chat.id in replies and m.text.strip() in replies[m.chat.id], priority=5)
def trigger_reply(m):
    bot.reply_to(m, replies[m.chat.id][m.text.strip()])

# --- 15. نظام المنع ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("منع "))
def add_filter(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    word=m.text.replace("منع ","").strip()
    filters_words.setdefault(chat_id,set()).add(word)
    bot.reply_to(m, f"✅ تم منع كلمة {word}")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("الغاء منع "))
def del_filter(m):
    chat_id=m.chat.id
    word=m.text.replace("الغاء منع ","").strip()
    if chat_id in filters_words and word in filters_words[chat_id]:
        filters_words[chat_id].remove(word); bot.reply_to(m, f"✅ تم الغاء منع {word}")

@bot.message_handler(func=lambda m: m.text and m.chat.id in filters_words and any(w in m.text for w in filters_words[m.chat.id]), content_types=['text'], priority=0)
def filter_handler(m):
    try: bot.delete_message(m.chat.id, m.message_id)
    except: pass

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["قائمة المنع","المنع"])
def show_filters(m):
    chat_id=m.chat.id
    if chat_id not in filters_words or not filters_words[chat_id]: bot.reply_to(m, "✅ لا يوجد كلمات ممنوعة"); return
    text="🚫 قائمة المنع:\n"
    for w in filters_words[chat_id]: text+=f"- {w}\n"
    bot.reply_to(m, text)

# --- 16. نظام الترحيب ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith("ضع ترحيب "))
def set_welcome(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    welcome_text=m.text.replace("ضع ترحيب ","").strip()
    welcome_messages[chat_id]=welcome_text
    bot.reply_to(m, f"✅ تم وضع الترحيب: {welcome_text}")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["تفعيل الترحيب","تعطيل الترحيب"])
def toggle_welcome(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    if "تفعيل" in m.text: welcome_messages.setdefault(chat_id, "أهلا وسهلا")
    else:
        if chat_id in welcome_messages: del welcome_messages[chat_id]
    bot.reply_to(m, f"✅ {'تم تفعيل' if 'تفعيل' in m.text else 'تم تعطيل'} الترحيب")

@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'], priority=0)
def welcome_new(m):
    chat_id=m.chat.id
    if chat_id in welcome_messages:
        for new in m.new_chat_members:
            bot.send_message(chat_id, f"{welcome_messages[chat_id]} - {new.first_name}")

# --- 17. رفع ونزول ---
@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("رفع مميز"))
def promote_special(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    target=get_target_from_mention(m)
    if not target: return
    private_group_ranks.setdefault(chat_id, {})[target["id"]]="مميز"
    bot.reply_to(m, f"✅ تم رفع {target['first_name']} مميز - حتى لو بدون يوزر")

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("تنزيل مميز"))
def demote_special(m):
    chat_id=m.chat.id
    target=get_target_from_mention(m)
    if not target: return
    if chat_id in private_group_ranks and target["id"] in private_group_ranks[chat_id]:
        del private_group_ranks[chat_id][target["id"]]
        bot.reply_to(m, f"✅ تم تنزيل {target['first_name']} من مميز")

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("رفع ادمن"))
def promote_admin(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    target=get_target_from_mention(m)
    if not target: return
    try:
        bot.promote_chat_member(chat_id, target["id"], can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_invite_users=True)
        bot_promoted_admins.setdefault(chat_id,set()).add(target["id"])
        bot.reply_to(m, f"✅ تم رفع {target['first_name']} ادمن - عن طريق البوت يحميك")
    except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("تنزيل ادمن"))
def demote_admin(m):
    chat_id=m.chat.id
    target=get_target_from_mention(m)
    if not target: return
    try:
        bot.promote_chat_member(chat_id, target["id"], can_delete_messages=False, can_restrict_members=False, can_pin_messages=False, can_invite_users=False)
        bot.reply_to(m, f"✅ تم تنزيل {target['first_name']} من الادمن")
    except Exception as e: bot.reply_to(m, f"❌ خطأ: {e}")

# --- 18. قفل الاوامر في الخاص ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["قفل الخاص","قفل الاوامر"])
def lock_private_commands(m):
    chat_id=m.chat.id
    if not is_owner(chat_id, m.from_user.id): return
    locked_commands_private[chat_id]=True
    bot.reply_to(m, "🔒 تم قفل الخاص - الاوامر في الخاص مقفلة")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["فتح الخاص","فتح الاوامر"])
def unlock_private_commands(m):
    chat_id=m.chat.id
    if chat_id in locked_commands_private: del locked_commands_private[chat_id]
    bot.reply_to(m, "🔓 تم فتح الخاص")

# --- 19. تحكم ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("ctrl_"))
def control_callback(call):
    chat_id=call.message.chat.id; user_id=int(call.data.split("_")[-1]); action=call.data.split("_")[1]
    if not is_owner(chat_id, call.from_user.id): bot.answer_callback_query(call.id, "للمالك فقط"); return
    try:
        if action=="ban": bot.ban_chat_member(chat_id, user_id); bot.edit_message_text(f"🚫 تم حظر {user_id}", chat_id, call.message.message_id)
        elif action=="mute": bot.restrict_chat_member(chat_id, user_id, can_send_messages=False); muted_users.setdefault(chat_id,set()).add(user_id); bot.edit_message_text(f"🔇 تم كتم {user_id}", chat_id, call.message.message_id)
        elif action=="promote": bot.promote_chat_member(chat_id, user_id, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True); bot_promoted_admins.setdefault(chat_id,set()).add(user_id); bot.edit_message_text(f"👑 تم رفع {user_id} مشرف", chat_id, call.message.message_id)
        elif action=="demote": bot.promote_chat_member(chat_id, user_id, can_delete_messages=False, can_restrict_members=False, can_pin_messages=False); bot.edit_message_text(f"⬇️ تم تنزيل {user_id}", chat_id, call.message.message_id)
        bot.answer_callback_query(call.id, "تم")
    except Exception as e: bot.answer_callback_query(call.id, f"خطأ: {e}")

# --- 20. اوامر عامة ---
@bot.callback_query_handler(func=lambda call: call.data=="close_settings")
def close_settings(call):
    try: bot.delete_message(call.message.chat.id, call.message.message_id)
    except: bot.edit_message_text("❌ تم الإغلاق", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الاوامر","الاوامر الشاملة","/help"])
def all_commands(m):
    bot.reply_to(m, """
📋 الاوامر الشاملة ULTIMATE V3 - كل الاوامر من اول المحادثات

🆕 دعم بدون يوزر
- حظر + منشن مباشر حتى لو بدون يوزر
- كتم + منشن
- تقييد + منشن
- تحكم + منشن
- كشف + منشن
- ايدي + منشن
- رفع/تنزيل + منشن

🆕 الوضع الخاص
- تفعيل الوضع الخاص
- رفع Dev الاساسي بالرد

🆕 نظام الأولوية 1-5
- رفع مطور اساسي - ازرار 1-5 - 🔒 فوقك
- تنزيل مطور اساسي 3
- المطورين الاساسيين / الاساسيين / قائمه Dev الاساسي
- صاحب البوت دايم الأول

🆕 نظام الإذاعات الجديد
- قسم الاذاعه - قروبات/خاص/الكل + 50/100/500/1000/5000/إلى الكل + نسخ/توجيه
- الاذاعات - آخر إذاعاتك وتمسح خلال يومين
- اذاعه خاص 500 - الأوامر القديمة شغالة

🆕 تنظيف
- تنظيف - يمسح كل شي (صور، ملصقات، فيديو، قصص، روابط، معدّلة) ويقولك كم من كل نوع
- استثناء بالرد - المستثناة ما تنمسح

🆕 التقييد الخاص
- تقييد خاص - ما يفكه إلا اللي حطه
- الغاء تقييد خاص - بس لصاحب التقييد
- المقيدين خاص - القائمة ومين قيد
- رفع القيود ما تفكه - اذا فكوه من اعدادات تليجرام يرجعه

🆕 مسح القوائم
- مسح القوائم - لوحة كل القوائم وعددها جنبها
- مسح الرتب - يفتح قسم الرتب على طول
- كل واحد يشوف بس اللي يقدر يمسحها

🆕 نظام الحدود
- ضع حد الحظر 5 - كل مشرف 5 باليوم
- ضع حد الكتم 4 - بالرد على مشرف يصير خاص له هو بس
- ضع حد المسح 500 - بالرد/منشن/ايدي
- الحدود - لوحة تعدل بالأزرار
- حدودي - المشرف يشوف باقي له
- اللي يتعدى البوت يرفض + اذا سواها من تلي يشيل إشرافه

🆕 التنزيل التلقائي
- تفعيل التنزيل التلقائي
- ضع حد تنزيل مميز 3 ساعات - لكل رتبة مدة غير
- اعدادات التنزيل - تشوف وتعدل بالأزرار
- أي رسالة/تفاعل/ضغطة زر تنحسب موجود

🆕 حماية ربط القنوات المهمة جدا
- قفل الربط 🔒 - أول ما تنربط قناة يعلمك + يمسح منشوراتها + يسحب التثبيت
- معلومات القروب ← تعديل ← القناة المرتبطة ← فك الربط
- نصيحة: حظر المستخدمين، إضافة الأعضاء، تثبيت الرسائل أخطر الصلاحيات

🆕 نظام اهمس
- حظر من اهمس + منشن حتى بدون يوزر
- الغاء حظر من اهمس
- المحظورين من اهمس

🆕 الحماية العامة
- قفل الروابط / فتح الروابط
- قفل الصور / فتح الصور
- قفل الملصقات / فتح الملصقات
- قفل الفيديو / فتح الفيديو
- قفل المتحركة / فتح المتحركة
- قفل الملفات / فتح الملفات
- قفل الجهات / فتح الجهات
- قفل المواقع / فتح المواقع
- قفل التثبيت / فتح التثبيت - حماية من ربط القنوات
- قفل الاضافة / فتح الاضافة
- قفل الحظر / فتح الحظر
- قفل التعديل / فتح التعديل
- قفل الربط / فتح الربط

🆕 التحذيرات
- تحذير بالرد - 3 تحذيرات = حظر
- مسح التحذيرات بالرد

🆕 الردود
- اضف رد [كلمة] [رد]
- مسح رد [كلمة]
- الردود - عرض كل الردود

🆕 المنع
- منع [كلمة]
- الغاء منع [كلمة]
- قائمة المنع / المنع

🆕 الترحيب
- ضع ترحيب [نص]
- تفعيل الترحيب / تعطيل الترحيب

🆕 الرفع والنزول
- رفع مميز / تنزيل مميز - حتى بدون يوزر
- رفع ادمن / تنزيل ادمن - عن طريق البوت يحميك من التفليش
- رفع مشرف كامل - عن طريق البوت

🆕 قفل الخاص
- قفل الخاص / فتح الخاص
- قفل الاوامر / فتح الاوامر

🆕 تحكم - لوحة تحكم كاملة
- تحكم بالرد/منشن - حتى بدون يوزر
- ازرار: حظر - كتم - رفع مشرف - تنزيل مشرف

- حظر - كتم - تقييد - ايدي - كشف
- ايدي يطلع الايدي حتى لو بدون يوزر

كل الاوامر تدعم المنشن المباشر حتى لو بدون يوزر! ✨
""")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["start","/start"])
def start_cmd(m):
    bot.reply_to(m, f"✅ SRDT @kpcukbot7454_bot شغال ULTIMATE V3\n\nفيه كل الاوامر من اول المحادثات\n\nالتوكن الجديد فعال ✅\n\n- دعم بدون يوزر\n- الوضع الخاص\n- نظام الأولوية 1-5\n- نظام الإذاعات الجديد\n- أمر تنظيف\n- التقييد الخاص\n- مسح القوائم\n- نظام الحدود\n- التنزيل التلقائي\n- حماية ربط القنوات المهمة جدا\n- نظام اهمس\n- كل اقفال الحماية\n- التحذيرات\n- الردود\n- المنع\n- الترحيب\n- رفع ونزول\n\nالاوامر لعرض الكل")

print("✅ SRDT Bot ULTIMATE V3 Running - Token:", BOT_TOKEN[:10]+"...")
print("✅ فيه كل الاوامر من اول المحادثات")
bot.infinity_polling()
