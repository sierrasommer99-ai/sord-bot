import os, asyncio, threading, time, json, random
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
user_messages = defaultdict(list)

# ملفات الحفظ
FILES = ["ranks.json", "stats.json", "custom.json", "media.json"]
for f in FILES:
    if not os.path.exists(f):
        with open(f, "w") as fp: json.dump({}, fp)

def load(f):
    try:
        with open(f, "r") as fp: return json.load(fp)
    except: return {}
def save(f, d):
    try:
        with open(f, "w") as fp: json.dump(d, fp)
    except: pass

RANKS = load("ranks.json")
STATS = load("stats.json")
CUSTOM = load("custom.json")
MEDIA = load("media.json")

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS: RANKS[cid]={"dev2":[],"dev":[],"myth_b":[],"myth":[],"asasi":[]}
    return RANKS[cid]
def get_rank(cid, uid):
    r=get_r(cid)
    if uid in r["asasi"] or uid in r["dev2"]: return "Dev² 🎖️"
    if uid in r["dev"]: return "Dev 🎖️"
    if uid in r["myth_b"]: return "Myth 🎖️"
    if uid in r["myth"]: return "Myth"
    return "عضو"

PORN = ["كس","زب","نيك","xnxx","porn","xxx","سكس","طيز","كسمك"]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"SORD V100 LIVE")

def run_server():
    port=int(os.environ.get("PORT",10000))
    HTTPServer(('0.0.0.0', port), H).serve_forever()

async def is_admin(u):
    try:
        m=await u.effective_chat.get_member(u.effective_user.id)
        return m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except: return False

async def start(update, context):
    cid=str(update.effective_chat.id); uid=update.effective_user.id
    r=get_r(cid)
    if update.effective_user.username=="ADJkex":
        if uid not in r["asasi"]: r["asasi"].append(uid)
        if uid not in r["dev2"]: r["dev2"].append(uid)
        save("ranks.json", RANKS)
    txt="""• أهلًا بك عزيزي أنا اسمي سورد

━━━━━━━━━━━━━━━
حرفيا أفضل بوت!
━━━━━━━━━━━━━━━
🎖️ الرتب المتاحة:
• Dev² 🎖️
• Dev 🎖️
• Myth 🎖️
• Myth
━━━━━━━━━━━━━━━
🛡️ الحماية الكاملة شغالة
━━━━━━━━━━━━━━━
- المطور ↫ راكان @ADJkex"""
    kb=[[InlineKeyboardButton("➕ اضفني لقروبك", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("👨‍💻 ADJkex", url="https://t.me/ADJkex")]]
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))

async def all_msg(update, context):
    if not update.message: return
    cid=str(update.effective_chat.id); uid=update.effective_user.id
    msg=update.message; text=(msg.text or "").strip()
    
    # احصائيات
    if cid not in STATS: STATS[cid]={}
    su=str(uid)
    if su not in STATS[cid]: STATS[cid][su]={"c":0,"n":msg.from_user
