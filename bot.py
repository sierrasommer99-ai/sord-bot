import os, asyncio, threading, time, json, random
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
user_messages = defaultdict(list)

RANKS_FILE = "ranks.json"
STATS_FILE = "stats.json"
CUSTOM_FILE = "custom_commands.json"
MEDIA_FILE = "media_log.json"

for f in [RANKS_FILE, STATS_FILE, CUSTOM_FILE, MEDIA_FILE]:
    if not os.path.exists(f):
        with open(f, "w") as fp:
            json.dump({}, fp)

def load(f):
    try:
        with open(f, "r") as fp:
            return json.load(fp)
    except:
        return {}
def save(f, data):
    try:
        with open(f, "w") as fp:
            json.dump(data, fp)
    except: pass

RANKS = load(RANKS_FILE)
STATS = load(STATS_FILE)
CUSTOM = load(CUSTOM_FILE)
MEDIA_LOG = load(MEDIA_FILE)

def get_ranks(cid):
    cid = str(cid)
    if cid not in RANKS:
        RANKS[cid] = {"dev2": [], "dev": [], "myth_badge": [], "myth": [], "dev_asasi": []}
    return RANKS[cid]

def get_stats(cid):
    cid = str(cid)
    if cid not in STATS:
        STATS[cid] = {}
    return STATS[cid]

def get_custom(cid):
    cid = str(cid)
    if cid not in CUSTOM:
        CUSTOM[cid] = {}
    return CUSTOM[cid]

def get_media_log(cid):
    cid = str(cid)
    if cid not in MEDIA_LOG:
        MEDIA_LOG[cid] = []
    return MEDIA_LOG[cid]

def get_rank_name(cid, uid):
    r = get_ranks(cid)
    if uid in r["dev_asasi"]: return "Dev² 🎖️"
    if uid in r["dev2"]: return "Dev² 🎖️"
    if uid in r["dev"]: return "Dev 🎖️"
    if uid in r["myth_badge"]: return "Myth 🎖️"
    if uid in r["myth"]: return "Myth"
    return "عضو"

PORN_WORDS = ["كس", "زب", "نيك", "متناك", "شرموط", "قحبة", "xnxx", "porn", "sex", "xxx", "سكس", "طيز", "كسمك", "منيوك", "عيري", "مص", "لحس"]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SORD Full Ultimate Running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(('0.0.0.0', port), Handler)
    httpd.serve_forever()

async def is_admin(update: Update):
    try:
        m = await update.effective_chat.get_member(update.effective_user.id)
        return m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
       
