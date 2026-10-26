import os, asyncio, threading, time, json, random
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
user_messages = defaultdict(list)

for f in ["ranks.json","stats.json","custom.json","media.json"]:
    if not os.path.exists(f):
        with open(f,"w") as fp: json.dump({},fp)

def load(f):
    try:
        with open(f,"r") as fp: return json.load(fp)
    except: return {}
def save(f,d):
    try:
        with open(f,"w") as fp: json.dump(d,fp)
    except: pass

RANKS=load("ranks.json"); STATS=load("stats.json"); CUSTOM=load("custom.json"); MEDIA=load("media.json")

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS: RANKS[cid]={"dev2":[],"dev":[],"myth_b":[],"myth":[],"asasi":[]}
    return RANKS[cid]

def get_rank(cid,uid):
    r=get_r(cid)
    if uid in r["asasi"] or uid in r["dev2"]: return "Dev² 🎖️"
    if uid in r["dev"]: return "Dev 🎖️"
    if uid in r["myth_b"]: return "Myth 🎖️"
    if uid in r["myth"]: return "Myth"
    return "عضو"

PORN=["كس","زب","نيك","xnxx","porn","xxx","سكس"]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"SORD LIVE")

def run_server():
    port=int(os.environ.get("PORT",10000))
    HTTPServer(('0.0.0.0',port),H).serve_forever()

async def is_admin(u):
    try:
        m=await u.effective_chat.get_member(u.effective_user.id)
        return m.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]
    except: return False

async def start(update,context):
    cid=str(update.effective_chat.id); uid=update.effective_user.id; r=get_r(cid)
    if update.effective_user.username=="ADJkex":
        if uid not in r["asasi"]: r["asasi"].append(uid)
        if uid not in r["dev2"]: r["dev2"].append(uid)
        save("ranks.json",RANKS)
    txt="""• أهلًا بك عزيزي أنا اسمي سورد

━━━━━━━━━━━━━━━
حرفيا أفضل بوت!
━━━━━━━━━━━━━━━
🎖️ الرتب: Dev² 🎖️ / Dev 🎖️ / Myth 🎖️ / Myth
━━━━━━━━━━━━━━━
- المطور ↫ راكان @ADJkex"""
    kb=[[InlineKeyboardButton("➕ اضفني لقروبك",url=f"https://t.me/{context.bot.username}?startgroup=true")],[InlineKeyboardButton("👨‍💻 ADJkex",url="https://t.me/ADJkex")]]
    await update.message.reply_text(txt,reply_markup=InlineKeyboardMarkup(kb))

async def all_msg(update,context):
    if not update.message: return
    cid=str(update.effective_chat.id); uid=update.effective_user.id; msg=update.message; text=(msg.text or "").strip()
    
    if cid not in STATS: STATS[cid]={}
    su=str(uid)
    if su not in STATS[cid]: STATS[cid][su]={"c":0,"n":msg.from_user.first_name}
    STATS[cid][su]["c"]+=1; STATS[cid][su]["n"]=msg.from_user.first_name; save("stats.json",STATS)
    
    if msg.photo or msg.video or msg.sticker or msg.animation:
        if cid not in MEDIA: MEDIA[cid]=[]
        MEDIA[cid].append(msg.message_id)
        if len(MEDIA[cid])>500: MEDIA[cid]=MEDIA[cid][-500:]
        save("media.json",MEDIA)

    if msg.new_chat_members:
        for mem in msg.new_chat_members:
            if mem.is_bot and mem.username!=context.bot.username:
                try: await context.bot.ban_chat_member(cid,mem.id); await msg.reply_text(f"🚫 طرد البوت {mem.first_name}")
                except: pass

    if text in ["رتبتي","رتبته"]:
        if msg.reply_to_message: await msg.reply_text(f"رتبته => {get_rank(cid,msg.reply_to_message.from_user.id)}")
        else: await msg.reply_text(f"رتبتك => {get_rank(cid,uid)}")
        return
    if text=="الرتب":
        r=get_r(cid); await msg.reply_text(f"Dev² 🎖️: {len(r['dev2'])}\nDev 🎖️: {len(r['dev'])}\nMyth 🎖️: {len(r['myth_b'])}\nMyth: {len(r['myth'])}"); return
    if text in ["توب","توب المتفاعلين","تفاعل"]:
        if cid not in STATS: await msg.reply_text("لا يوجد"); return
        top=sorted(STATS[cid].items(),key=lambda x:x[1]["c"],reverse=True)[:10]
        t="🏆 توب المتفاعلين:\n\n"
        for i,(k,v) in enumerate(top,1): t+=f"{i}. {v['n']} - {v['c']}\n"
        await msg.reply_text(t); return
    if text=="الالعاب":
        kb=[[InlineKeyboardButton("✊ حجر",callback_data="rps_rock"),InlineKeyboardButton("✋ ورقة",callback_data="rps_paper"),InlineKeyboardButton("✌️ مقص",callback_data="rps_scissors")],[InlineKeyboardButton("🎲 حظ",callback_data="luck")]]
        await msg.reply_text("🎮 العاب سورد:",reply_markup=InlineKeyboardMarkup(kb)); return
    if text.startswith("اضف امر"):
        name=text.replace("اضف امر","",1).strip().lower()
        if not name or not msg.reply_to_message: await msg.reply_text("رد على رسالة واكتب اضف امر + الاسم"); return
        if cid not in CUSTOM: CUSTOM[cid]={}
        CUSTOM[cid][name]=msg.reply_to_message.text or ""; save("custom.json",CUSTOM); await msg.reply_text(f"تم اضافة امر {name}"); return
    if text.startswith("حذف امر"):
        name=text.replace("حذف امر","",1).strip().lower()
        if cid in CUSTOM and name in CUSTOM[cid]: del CUSTOM[cid][name]; save("custom.json",CUSTOM); await msg.reply_text(f"تم حذف {name}"); return
    if text=="الاوامر":
        if cid not in CUSTOM or not CUSTOM[cid]: await msg.reply_text("لا يوجد"); return
        t="📜 الاوامر:\n"
        for k in CUSTOM[cid]:
            if not k.startswith("wh_"): t+=f"- {k}\n"
        await msg.reply_text(t); return

    if msg.reply_to_message and ("رفع" in text or "تنزيل" in text) and ("Dev" in text or "ديف" in text or "Myth" in text or "ميث" in text):
        r=get_r(cid); target=msg.reply_to_message.from_user; rk=None
        if "Dev²" in text or "dev2" in text.lower() or "ديف 2" in text: rk="dev2"
        elif "Myth 🎖️" in text: rk="myth_b"
        elif "Myth" in text or "ميث" in text: rk="myth"
        elif "Dev" in text or "ديف" in text: rk="dev"
        if rk:
            if "رفع" in text:
                if target.id not in r[rk]: r[rk].append(target.id); save("ranks.json",RANKS); await msg.reply_text(f"تم رفع {target.first_name} => {rk}")
            else:
                if target.id in r[rk]: r[rk].remove(target.id); save("ranks.json",RANKS); await msg.reply_text(f"تم تنزيل {target.first_name}")
            return

    if text.startswith("رفع مشرف") and msg.reply_to_message:
        r=get_r(cid)
        if uid not in r["asasi"] and uid not in r["dev2"] and uid not in r["dev"] and msg.from_user.username!="ADJkex":
            await msg.reply_text("❌ بس المطور Dev² 🎖️ / Dev 🎖️ يقدر يرفع مشرف من البوت")
            return
        try:
            await context.bot.promote_chat_member(cid,msg.reply_to_message.from_user.id,can_delete_messages=True,can_restrict_members=True,can_pin_messages=True,can_promote_members=True,can_manage_chat=True,can_manage_video_chats=True,is_anonymous=False)
            await msg.reply_text(f"✅ تم رفع {msg.reply_to_message.from_user.first_name} مشرف بكل الصلاحيات\nبواسطة المطور {msg.from_user.first_name}\n🔥 الحين يقدر يتحكم كامل")
        except Exception as e: await msg.reply_text(f"خطأ: {e}")
        return

    if text.startswith("تنزيل مشرف") and msg.reply_to_message:
        r=get_r(cid)
        if uid not in r["asasi"] and uid not in r["dev2"] and uid not in r["dev"] and msg.from_user.username!="ADJkex":
            await msg.reply_text("❌ بس المطور يقدر ينزل مشرف")
            return
        try:
            await context.bot.promote_chat_member(cid,msg.reply_to_message.from_user.id,can_delete_messages=False,can_restrict_members=False,can_pin_messages=False,can_promote_members=False,can_manage_chat=False,is_anonymous=False)
            await msg.reply_text(f"✅ تم تنزيل {msg.reply_to_message.from_user.first_name}")
        except: pass
        return

    if text.startswith("كتم") and msg.reply_to_message:
        if not await is_admin(update): return
        try: await context.bot.restrict_chat_member(cid,msg.reply_to_message.from_user.id,permissions=None,until_date=int(time.time()+3600)); await msg.reply_text("🔇 تم كتمه")
        except: pass
        return
    if text.startswith("حظر") and msg.reply_to_message:
        if not await is_admin(update): return
        try: await context.bot.ban_chat_member(cid,msg.reply_to_message.from_user.id); await msg.reply_text("🚫 تم الحظر")
        except: pass
        return
    if text.startswith("تثبيت") and msg.reply_to_message:
        if not await is_admin(update): return
        try: await context.bot.pin_chat_message(cid,msg.reply_to_message.message_id); await msg.reply_text("📌 تم التثبيت")
        except: pass
        return
    if text in ["الغاء التثبيت","الغاء تثبيت"]:
        if not await is_admin(update): return
        try:
            if msg.reply_to_message: await context.bot.unpin_chat_message(cid,msg.reply_to_message.message_id)
            else: await context.bot.unpin_all_chat_messages(cid)
            await msg.reply_text("تم الغاء التثبيت")
        except: pass
        return
    if text=="مسح" and msg.reply_to_message:
        if not await is_admin(update): return
        try: await context.bot.delete_message(cid,msg.reply_to_message.message_id); await msg.delete()
        except: pass
        return
    if text=="تنظيف":
        if not await is_admin(update): return
        cnt=0
        if cid in MEDIA:
            for mid in MEDIA[cid][-100:]:
                try: await context.bot.delete_message(cid,mid); cnt+=1
                except: pass
            MEDIA[cid]=[]; save("media.json",MEDIA)
        await msg.reply_text(f"🧹 تم تنظيف {cnt} رسالة"); return
    if text.startswith("همسه"):
        if not msg.reply_to_message: await msg.reply_text("رد على شخص واكتب: همسه + كلامك"); return
        hm=text.replace("همسه","",1).strip()
        if not hm: await msg.reply_text("اكتب الهمسه!"); return
        try: await msg.delete()
        except: pass
        if cid not in CUSTOM: CUSTOM[cid]={}
        key=f"wh_{msg.reply_to_message.from_user.id}_{int(time.time())}"
        CUSTOM[cid][key]=hm; save("custom.json",CUSTOM)
        kb=[[InlineKeyboardButton("👁️ عرض الهمسه",callback_data=f"wh_{msg.reply_to_message.from_user.id}")]]
        await context.bot.send_message(cid,f"🔒 عندك همسه من {msg.from_user.first_name} الى {msg.reply_to_message.from_user.first_name}",reply_markup=InlineKeyboardMarkup(kb))
        return
    if cid in CUSTOM and text.lower() in CUSTOM[cid]:
        if not text.lower().startswith("wh_"): await msg.reply_text(CUSTOM[cid][text.lower()]); return

    if await is_admin(update): return
    r=get_r(cid)
    if uid in r["asasi"] or uid in r["dev2"] or uid in r["dev"] or uid in r["myth_b"] or uid in r["myth"]: return
    low=text.lower()
    for bad in PORN:
        if bad in low:
            try:
                await msg.delete()
                if msg.photo or msg.video: await context.bot.ban_chat_member(cid,uid)
            except: pass
            return
    if any(x in low for x in ["http://","https://","t.me/","www."]):
        try: await msg.delete(); return
        except: pass
    if msg.forward_from or msg.forward_from_chat:
        try: await msg.delete(); return
        except: pass
    now=time.time(); user_messages[uid].append(now); user_messages[uid]=[t for t in user_messages[uid] if now-t<7]
    if len(user_messages[uid])>4:
        try: await update.effective_chat.restrict_chat_member(uid,permissions=None,until_date=int(now+300)); user_messages[uid]=[]
        except: pass

async def anti_edit(update,context):
    if not update.edited_message: return
    if update.effective_chat.type=="private": return
    cid=str(update.effective_chat.id); uid=update.edited_message.from_user.id if update.edited_message.from_user else 0; r=get_r(cid)
    if uid in r["asasi"] or uid in r["dev2"]: return
    try: await update.edited_message.delete(); await context.bot.send_message(cid,f"تعدل مره ثانيه بلعن امك يا {update.edited_message.from_user.first_name}")
    except: pass

async def buttons(update,context):
    q=update.callback_query; await q.answer(); data=q.data; cid=str(update.effective_chat.id)
    if data.startswith("wh_"):
        tid=int(data.split("_")[1])
        if q.from_user.id!=tid: await q.answer("مو لك الهمسه!",show_alert=True); return
        if cid in CUSTOM:
            for k,v in CUSTOM[cid].items():
                if k.startswith(f"wh_{tid}"): await q.answer(v,show_alert=True); return
        await q.answer("الهمسه راحت",show_alert=True); return
    if data.startswith("rps_"):
        u=data.replace("rps_",""); b=random.choice(["rock","paper","scissors"]); nm={"rock":"حجر","paper":"ورقة","scissors":"مقص"}
        if u==b: res="تعادل!"
        elif (u=="rock" and b=="scissors") or (u=="paper" and b=="rock") or (u=="scissors" and b=="paper"): res="فزت! 🔥"
        else: res="خسرت! 😂"
        await q.edit_message_text(f"انت: {nm[u]} | البوت: {nm[b]}\n{res}"); return
    if data=="luck": await q.edit_message_text(random.choice(["حظك نار 🔥🔥","حظك حلو 🎉","انتبه 😐"])); return

if __name__=="__main__":
    if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN missing")
    threading.Thread(target=run_server,daemon=True).start()
    try: loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop)
    except: pass
    app=ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,all_msg))
    app.add_handler(MessageHandler(filters.ALL & ~filters.UpdateType.EDITED_MESSAGE,all_msg))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE,anti_edit))
    app.add_handler(CallbackQueryHandler(buttons))
    print("SORD FULL RUNNING")
    app.run_polling()
