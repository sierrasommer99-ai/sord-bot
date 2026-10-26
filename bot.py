import os, threading, json
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN=os.getenv('BOT_TOKEN','').strip()

def load(f):
    try:
        return json.load(open(f,encoding='utf-8'))
    except:
        return {}
def save(f,d):
    json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

for fp in ['locks.json','ranks.json','custom.json','stats.json','data.json','bans.json','msgs.json']:
    if not os.path.exists(fp):
        save(fp,{})

LOCKS=load('locks.json')
RANKS=load('ranks.json')
CUSTOM=load('custom.json')
STATS=load('stats.json')
DATA=load('data.json')
BANS=load('bans.json')
MSGS=load('msgs.json')

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS:
        RANKS[cid]={'asasi':[],'dev2':[],'dev':[],'myth':[]}
    return RANKS[cid]

def get_rank_text(uid,cid):
    r=get_r(cid)
    uid=int(uid)
    if uid in r['asasi']:
        return 'Dev الاساسي'
    if uid in r['dev2']:
        return 'Dev²'
    if uid in r['dev']:
        return 'Dev'
    if uid in r['myth']:
        return 'Myth'
    return 'عضو'

def is_ranked(uid,cid):
    return get_rank_text(uid,cid)!='عضو'

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'SORD REPLY FIX LIVE')

def run_server():
    p=int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()

def kb_main():
    b=[]
    b.append([InlineKeyboardButton('القفل والفتح',callback_data='ml')])
    b.append([InlineKeyboardButton('التفعيل والتعطيل',callback_data='mt')])
    b.append([InlineKeyboardButton('ادارة القروب',callback_data='ma')])
    b.append([InlineKeyboardButton('التسلية والخدمية',callback_data='mf')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

def kb_promote(uid):
    b=[]
    b.append([InlineKeyboardButton('رفع بكامل الصلاحيات',callback_data=f'pa_{uid}')])
    b.append([InlineKeyboardButton('تنزيل من الاشراف',callback_data=f'dm_{uid}')])
    b.append([InlineKeyboardButton('التحكم',callback_data=f'ct_{uid}')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

def kb_control(uid,cid):
    cnt=STATS.get(cid,{}).get(str(uid),0)
    b=[]
    b.append([InlineKeyboardButton(f'رسائله {cnt}',callback_data=f'n_{uid}')])
    b.append([InlineKeyboardButton('مسح رسائله',callback_data=f'mr_{uid}')])
    b.append([InlineKeyboardButton('حظره من الالعاب',callback_data=f'bg_{uid}')])
    b.append([InlineKeyboardButton('حظره من الهمس',callback_data=f'bh_{uid}')])
    b.append([InlineKeyboardButton('حظر',callback_data=f'ban_{uid}')])
    b.append([InlineKeyboardButton('كتم',callback_data=f'mute_{
