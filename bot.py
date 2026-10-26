import os
import asyncio
import threading
import json
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

TOKEN = os.getenv('BOT_TOKEN','').strip()

LOCKS_FILE='locks.json'
RANKS_FILE='ranks.json'

if not os.path.exists(LOCKS_FILE):
    open(LOCKS_FILE,'w').write('{}')
if not os.path.exists(RANKS_FILE):
    open(RANKS_FILE,'w').write('{}')

def load(f):
    try:
        return json.load(open(f))
    except:
        return {}

def save(f,d):
    json.dump(d, open(f,'w'))

LOCKS=load(LOCKS_FILE)
RANKS=load(RANKS_FILE)

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS:
        RANKS[cid]={'asasi':[],'dev2':[]}
    return RANKS[cid]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_server():
    port = 10000
    env_port = os.getenv('PORT')
    if env_port:
        port = int(env_port)
    httpd = HTTPServer(('0.0.0.0',port),H)
    httpd.serve_forever()

async def start(update,context):
    cid=str(update.effective_chat.id)
    uid=update.effective_user.id
    r=get_r(cid)
    if update.effective_user.username=='ADJkex':
        if uid not in r['asasi']:
            r['asasi'].append(uid)
        if uid not in r['dev2']:
            r['dev2'].append(uid
