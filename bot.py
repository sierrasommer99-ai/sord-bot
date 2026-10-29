import os,json,threading
from http.server import HTTPServer,BaseHTTPRequestHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,ChatPermissions
from telegram.ext import ApplicationBuilder,CommandHandler,CallbackQueryHandler,MessageHandler,filters
TOKEN=os.getenv('BOT_TOKEN','').strip()
def load(f):
    try: return json.load(open(f,encoding='utf-8'))
    except: return {}
def save(f,d):
    json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
for fp in ['locks.json','ranks.json','stats.json']:
    import os as _os
    if not _os.path.exists(fp): save(fp,{})
LOCKS=load('locks.json')
RANKS=load('ranks.json')
STATS=load('stats.json')
def get_r(cid):
    cid=str(cid)
    if cid not in RANKS: RANKS[cid]={}
    for k in ['asasi','motawer','malik','monshe','modir','admin','momayz','dev']:
        if k not in RANKS[cid]: RANKS[cid][k]=[]
    return RANKS[cid]
def rn(uid,cid):
    r=get_r(cid); uid=int(uid)
    if uid in r['asasi']: return 'اساسي'
    if uid in r['motawer']: return 'مطور'
    if uid in r['malik']: return 'مالك'
    if uid in r['monshe']: return 'منشئ'
    if uid in r['modir']: return 'مدير'
    if uid in r['admin']: return 'ادمن'
    if uid in r['momayz']: return 'مميز'
    if uid in r['dev']: return 'Dev'
    return 'عضو'
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
def run_http():
    p=int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()
def kb_menu():
    b=[]
    t='م1 حماية'
    d='m1'
    b.append([InlineKeyboardButton(t,callback_data=d)])
    t='م2 رفع'
    d='m2'
    b.append([InlineKeyboardButton(t,callback_data=d)])
    t='م3 حظر'
    d='m3'
    b.append([InlineKeyboardButton(t,callback_data=d)])
    t
