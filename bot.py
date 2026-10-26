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

for fp in ['locks.json','ranks.json','custom.json','stats.json','data.json','bans.json']:
    if not os.path.exists(fp):
        save(fp,{})

LOCKS=load('locks.json')
RANKS=load('ranks.json')
CUSTOM=load('custom.json')
STATS=load('stats.json')
DATA=load('data.json')
BANS=load('bans.json')

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS:
        RANKS[cid]={'asasi':[],'dev2':[],'dev':[],'myth':[]}
    return RANKS[cid]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'SORD PROMOTE LIVE')

def run_server():
    p=int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()

def kb_main():
    b=[]
    b.append([InlineKeyboardButton('القفل والفتح',callback_data='menu_lock')])
    b.append([InlineKeyboardButton('التفعيل والتعطيل',callback_data='menu_toggle')])
    b.append([InlineKeyboardButton('ادارة القروب',callback_data='menu_admin')])
    b.append([InlineKeyboardButton('التسلية والخدمية',callback_data='menu_fun')])
    b.append([InlineKeyboardButton('الاعدادات',callback_data='menu_settings')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

def kb_promote(uid):
    b=[]
    b.append([InlineKeyboardButton('رفع بكامل الصلاحيات',callback_data=f'prom_all_{uid}')])
    b.append([InlineKeyboardButton('تغيير المعلومات : لا',callback_data=f'pinfo_{uid}')])
    b.append([InlineKeyboardButton('حذف الرسائل : نعم',callback_data=f'pdel_{uid}')])
    b.append([InlineKeyboardButton('حظر وتقييد : نعم',callback
