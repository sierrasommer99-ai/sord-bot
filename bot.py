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

for fp in ['locks.json','ranks.json']:
    if not os.path.exists(fp):
        save(fp,{})

LOCKS=load('locks.json')

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_server():
    p=int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()

def kb_promote(uid):
    b=[]
    b.append([InlineKeyboardButton('رفع بكامل الصلاحيات',callback_data=f'pa_{uid}')])
    b.append([InlineKeyboardButton('تنزيل من الاشراف',callback_data=f'dm_{uid}')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

async def start_cmd(u,c):
    await u.message.reply_text('SORD LIVE',reply_markup=kb_promote(0))

async def on_cb(u,c):
    q=u.callback_query
    await q.answer()
    d=q.data
    cid=str(u.effective_chat.id)
    if d=='close':
        try: await q.message.delete()
        except: pass
        return
    if d.startswith('pa_'):
        uid=int(d.split('_')[-1])
        try:
            await c.bot.promote_chat_member(cid,uid,can_change_info=True,can_delete_messages=True,can_invite_users=True,can_restrict_members=True,can_pin_messages=True)
            await q.edit_message_text('تم رفعه مشرف',reply_markup=kb_promote(uid))
        except Exception as e:
            await q.answer(f'{e}',show_alert=True)
        return
    if d.startswith('dm_'):
        uid=int(d.split('_')[-1])
        try:
            await c.bot.promote_chat_member(cid,uid,can_change_info=False,can_delete_messages=False,can_invite_users=False,can_restrict_members=False,can_pin_messages=False)
            await q.edit_message_text('تم تنزيله من الاشراف')
        except Exception as e:
            await q.answer(f'{e}',show_alert=True)
        return
    await q.answer('تم')

async def handle_text(u,c):
    if not u.message:
        return
    msg=u.message
    txt=(msg.text or '').strip()
    cid=str(u.effective_chat.id)
    if txt.startswith('رفع مشرف'):
        t=None
        if msg.reply_to_message:
            t=msg.reply_to_message.from_user
        if not t:
            await msg.reply_text('رد على الشخص')
            return
        await msg.reply_text(f'تم رفعه مشرف {t.first_name}',reply_markup=kb_promote(t.id))
        return
    if txt.startswith('قفل التعديل'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['edit']=True
        save('locks.json',LOCKS)
        await msg.reply_text('تم قفل التعديل')
        return
    if txt.startswith('فتح التعديل'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['edit']=False
        save('locks.json',LOCKS)
        await msg.reply_text('تم فتح التعديل')
        return

if __name__=='__main__':
    if not TOKEN:
        raise RuntimeError('TOKEN missing')
    import asyncio
    threading.Thread(target=run_server,daemon=True).start()
    try:
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except: pass
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_cmd))
    app.add_handler(CallbackQueryHandler(on_cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_text))
    print('LIVE')
    app.run_polling()
