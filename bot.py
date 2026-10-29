import os, json, threading, random
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN = os.getenv('BOT_TOKEN','').strip()

def load(f):
    try:
        return json.load(open(f,encoding='utf-8'))
    except:
        return {}
def save(f,d):
    json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

for fp in ['locks.json','ranks.json','stats.json','custom.json','data.json','bans.json']:
    if not os.path.exists(fp):
        save(fp,{})

LOCKS = load('locks.json')
RANKS = load('ranks.json')
STATS = load('stats.json')
CUSTOM = load('custom.json')
DATA = load('data.json')
BANS = load('bans.json')

PORN_WORDS = ['xnxx','porn','sex','xxx','كس','طيز','زب','نيك','سكس','ممحون','شرموطة','اباحي']
DRUG_WORDS = ['حشيش','مخدرات','كبتاجون','ترامادول','كوكايين','هيروين','حبوب','ليريكا','شبو']

def contains(words, txt):
    if not txt:
        return False
    t = txt.lower()
    for w in words:
        if w in t:
            return True
    return False

def get_r(cid):
    cid = str(cid)
    if cid not in RANKS:
        RANKS[cid] = {'asasi':[],'dev2':[],'dev':[],'myth':[]}
    return RANKS[cid]

def rank_of(uid,cid):
    r = get_r(cid)
    uid = int(uid)
    if uid in r['asasi']:
        return 'Dev الاساسي'
    if uid in r['dev2']:
        return 'Dev²'
    if
