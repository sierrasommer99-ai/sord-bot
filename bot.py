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

BOT_TOKEN = os.getenv('BOT_TOKEN','').strip()
user_messages = defaultdict(list)
pending_lock = {}
pending_add = {}
fastest_game = {}

for f in ['ranks.json','stats.json','custom.json','media.json','locks.json','muted.json']:
    if not os.path.exists(f):
        with open(f,'w') as fp:
            json.dump({},fp)

def load(f):
    try:
        with open(f,'r') as fp:
            return json.load(fp)
    except:
        return {}

def save(f,d):
    try:
        with open(f,'w') as fp:
            json.dump(d,fp)
    except:
        pass

RANKS=load('ranks.json')
STATS=load('stats.json')
CUSTOM=load('custom.json')
MEDIA=load('media.json')
LOCKS=load('locks.json')
MUTED=load('muted.json')

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS:
        RANKS[cid]={'dev2':[],'dev':[],'myth_b':[],'myth':[],'my':[],'m':[],'asasi':[]}
    return RANKS[cid]

RANK_LEVEL = {'member':0
