import os, asyncio, threading, time, json
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv('BOT_TOKEN','').strip()

LOCKS_FILE='locks.json'
RANKS_FILE='ranks.json'
if not os.path.exists(LOCKS_FILE):
    open(LOCKS_FILE,'w').write('{}')
if not os.path.exists(RANKS_FILE):
    open(RANKS_FILE,'w').write('{}')

def load(f):
    try:
        return json.load(open(f,'r'))
    except:
        return {}
def save(f,d):
    json.dump(d, open(f,'w'))

LOCKS=load(LOCKS_FILE)
RANKS=load(RANKS_FILE)

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS:
        RANKS[cid]={'asasi':[],'dev2':[],'dev':[]}
    return RANKS[cid]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_server():
    p=int(os.environ.get
