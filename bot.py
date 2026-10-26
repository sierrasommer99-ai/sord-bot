import os
import asyncio
import threading
import time
import json
import random
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
user_messages = defaultdict(list)
pending_lock = {}
pending_add = {}
fastest_game = {}

for f in ["ranks.json","stats.json","custom.json","media.json","locks.json","muted.json"]:
    if not os.path.exists(f):
        with open(f,"w") as fp:
            json.dump({},fp)

def load(f):
    try:
        with open(f,"r") as fp:
            return json.load(fp)
    except:
        return {}

def save(f,d):
    try:
        with open(f,"w") as fp:
            json.dump(d,fp)
    except:
        pass

RANKS=load("ranks.json")
STATS=load("stats.json")
CUSTOM=load("custom.json")
MEDIA=load("media.json")
LOCKS=load("locks.json")
MUTED=load("muted.json")

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS:
        RANKS[cid]={"dev2":[],"dev":[],"myth_b":[],"myth":[],"my":[],"m":[],"asasi":[]}
    return RANKS[cid]

RANK_LEVEL = {"member":0, "m":1, "my":2, "myth":2, "myth_b":3, "dev":4, "dev2":5, "asasi":6}

def get_rank_key(cid,uid):
    r=get_r(cid)
    if uid in r["asasi"]:
        return "asasi"
    if uid in r["dev2"]:
        return "dev2"
    if uid in r["dev"]:
        return "dev"
    if uid in r["myth_b"]:
        return "myth_b"
    if uid in r["myth"]:
        return "myth"
    if uid in r["my"]:
        return "my"
    if uid in r["m"]:
        return "m"
    return "member"

def get_rank_name(cid,uid):
    k=get_rank_key(cid,uid)
    if k=="asasi":
        return "Dev²"
    if k=="dev2":
        return "Dev²"
    if k=="dev":
        return "Dev"
    if k=="myth_b":
        return "Myth"
    if k=="myth":
        return "Myth"
    if k=="my":
        return "MY"
    if k=="m":
        return "M"
    return "عضو"

def can_use(my_rank, target_rank):
    return RANK_LEVEL[my_rank] > RANK_LEVEL[target_rank]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SORD FIXED")

def run_server():
    port=int(os.environ.get("PORT",10000))
    HTTPServer(('0.0.0.0',port),H).serve_forever()

async def is_admin(u):
    try:
        m=await u.effective_chat.get_member(u.effective_user.id)
        return m.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]
    except:
        return False

async def start(update,context):
    cid=str(update.effective_chat.id)
    uid=update.effective_user.id
    r=get_r(cid)
    if update.effective_user.username=="ADJkex":
        if uid not in r["asasi"]:
            r["asasi"].append(uid)
        if uid not in r["dev2"]:
            r["dev2"].append(uid)
        save("ranks.json",RANKS)
    kb=[[InlineKeyboardButton("اضفني لقروبك",url=f"https://t.me/{context.bot.username}?startgroup=true")]]
    await update.message.reply_text("سورد شغال - قفل التعديل / فتح التعديل",reply_markup=InlineKeyboardMarkup(kb))

async def all_msg(update,context):
    if not update.message:
        return
    cid=str(update.effective_chat.id)
    uid=update.effective_user.id
    msg=update.message
    text=(msg.text or "").strip()
    
    if cid not in STATS:
        STATS[cid]={}
    su=str(uid)
    if su not in STATS[cid]:
        STATS[cid][su]={"c":0,"n":msg.from_user.first_name}
    STATS[cid][su]["c"]+=1
    STATS[cid][su]["n"]=msg.from_user.first_name
    save("stats.json",STATS)

    if cid in fastest_game:
        if text == fastest_game[cid]:
            await msg.reply_text(f"اسرع واحد يكتب ( {text} ) - الفائز {msg.from_user.first_name}")
            del fastest_game[cid]
            return

    if msg.video_chat_participants_invited:
        try:
            inviter = msg.from_user.first_name
            for invited in msg.video_chat_participants_invited.users:
                await msg.reply_text(f"المستخدم ذا {inviter} قام بدعوة {invited.first_name} للمكالمة")
        except:
            pass

    if "@all" in text.lower():
        if cid in STATS and STATS[cid]:
            t=text.replace("@all","").strip() + "\n"
            for v in list(STATS[cid].values())[:15]:
                t+=f"{v['n']}, "
            await msg.reply_text(t.rstrip(", "))
            return

    if text.startswith("قفل التعديل"):
        my_rank = get_rank_key(cid,uid)
        if my_rank not in ["asasi","dev2","dev"]:
            await msg.reply_text("هذا الامر يخص Dev")
            return
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]["edit"]=True
        save("locks.json",LOCKS)
        await msg.reply_text(f"المستخدم {msg.from_user.first_name} قام بقفل التعديل - بتعدل ثاني مره بيجي المطور يلعن امك")
        return

    if text.startswith("
