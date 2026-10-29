import os, json, threading
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

for fp in ['locks.json','ranks.json','stats.json']:
    if not os.path.exists(fp):
        save(fp,{})

LOCKS = load('locks.json')
RANKS = load('ranks.json')
STATS = load('stats.json')

def get_r(cid):
    cid = str(cid)
    if cid not in RANKS:
        RANKS[cid] = {}
        RANKS[cid]['dev'] = []
        RANKS[cid]['myth'] = []
    return RANKS[cid]

def rank_of(uid,cid):
    r = get_r(cid)
    uid = int(uid)
    if uid in r['dev']:
        return 'Dev'
    return 'عضو'

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_http():
    p = int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()

async def cmd_start(u,c):
    await u.message.reply_text('سورد شغال بدون قناة')

async def text_all(u,c):
    if not u.message:
        return
    msg = u.message
    txt = (msg.text or '').strip()
    cid = str(u.effective_chat.id)
    uid = msg.from_user.id

    if txt == '/start':
        await msg.reply_text('هلا سورد شغال')
        return
    if txt == 'رتبتي':
        r = rank_of(uid,cid)
        await msg.reply_text(f'رتبتك => {r}')
        return
    if txt == 'قفل التعديل':
        if cid not in LOCKS:
            LOCKS[cid] = {}
        LOCKS[cid]['edit'] = True
        save('locks.json',LOCKS)
        await msg.reply_text('تم قفل التعديل')
        return
    if txt == 'فتح التعديل':
        if cid not in LOCKS:
            LOCKS[cid] = {}
        LOCKS[cid]['edit'] = False
        save('locks.json',LOCKS)
        await msg.reply_text('تم فتح التعديل')
        return

if __name__ == '__main__':
    import asyncio
    threading.Thread(target=run_http,daemon=True).start()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except:
        pass
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',cmd_start))
    app.add_handler(MessageHandler(filters.TEXT,text_all))
    print('SORD LIVE')
    app.run_polling()
