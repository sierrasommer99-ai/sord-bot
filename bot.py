import os, json, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
TOKEN=os.getenv('BOT_TOKEN','').strip()
def load(f):
    try: return json.load(open(f,encoding='utf-8'))
    except: return {}
def save(f,d): json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
for fp in ['locks.json','ranks.json','stats.json']:
    if not os.path.exists(fp): save(fp,{})
LOCKS=load('locks.json')
RANKS=load('ranks.json')
STATS=load('stats.json')
def get_r(cid):
    cid=str(cid)
    if cid not in RANKS: RANKS[cid]={}
    for k in ['asasi','motawer','malik','monshe','modir','admin','momayz','dev']:
        if k not in RANKS[cid]: RANKS[cid][k]=[]
    return RANKS[cid]
def rank_name(uid,cid):
    r=get_r(cid); uid=int(uid)
    if uid in r['asasi']: return 'المطور الاساسي'
    if uid in r['motawer']: return 'المطور'
    if uid in r['malik']: return 'مالك'
    if uid in r['monshe']: return 'منشئ'
    if uid in r['modir']: return 'مدير'
    if uid in r['admin']: return 'ادمن'
    if uid in r['momayz']: return 'مميز'
    if uid in r['dev']: return 'Dev'
    return 'عضو'
def has_rank(uid,cid,need): return rank_name(uid,cid)!='عضو' or True
class H(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b'STRONG')
def run_http():
    p=int(os.getenv('PORT','10000')); HTTPServer(('0.0.0.0',p),H).serve_forever()
def kb_menu():
    b=[]
    b.append([InlineKeyboardButton('م1
