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
        RANKS[cid] = {'dev':[],'myth':[]}
    return RANKS[cid]

def rank_of(uid,cid):
    r = get_r(cid)
    uid = int(uid)
    if uid in r['dev']:
        return 'Dev'
    if uid in r['myth']:
        return 'Myth'
    return 'عضو'

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'SORD CLEAN LIVE')

def run_http():
    p = int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()

def kb_menu():
    b = []
    b.append([InlineKeyboardButton('الاوامر',callback_data='a')])
    b.append([InlineKeyboardButton('قفل التعديل',callback_data='lock_edit')])
    b.append([InlineKeyboardButton('فتح التعديل',callback_data='open_edit')])
    b.append([InlineKeyboardButton('قفل الاباحي',callback_data='lock_porn')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

def kb_promote(uid):
    b = []
    b.append([InlineKeyboardButton('رفع بكامل الصلاحيات',callback_data=f'prom_{uid}')])
    b.append([InlineKeyboardButton('تنزيل من الاشراف',callback_data=f'dem_{uid}')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

async def cmd_start(u,c):
    await u.message.reply_text('هلا - سورد شغال بدون قنوات',reply_markup=kb_menu())

async def cb(u,c):
    q = u.callback_query
    await q.answer()
    d = q.data
    cid = str(u.effective_chat.id)
    if d == 'close':
        try:
            await q.message.delete()
        except:
            pass
        return
    if d == 'a':
        await q.edit_message_text('الاوامر: رتبتي, رتبته بالرد, رفع Dev بالرد, رفع مشرف بالرد, قفل التعديل, فتح التعديل, قفل الاباحي',reply_markup=kb_menu())
        return
    if d == 'lock_edit':
        if cid not in LOCKS:
            LOCKS[cid] = {}
        LOCKS[cid]['edit'] = True
        save('locks.json',LOCKS)
        await q.answer('تم قفل التعديل',show_alert=True)
        return
    if d == 'open_edit':
        if cid not in LOCKS:
            LOCKS[cid] = {}
        LOCKS[cid]['edit'] = False
        save('locks.json',LOCKS)
        await q.answer('تم فتح التعديل',show_alert=True)
        return
    if d == 'lock_porn':
        if cid not in LOCKS:
            LOCKS[cid] = {}
        LOCKS[cid]['porn'] = True
        LOCKS[cid]['photo'] = True
        save('locks.json',LOCKS)
        await q.answer('تم قفل الاباحي',show_alert=True)
        return
    if d.startswith('prom_'):
        uid = int(d.split('_')[1])
        try:
            await c.bot.promote_chat_member(cid,uid,can_change_info=True,can_delete_messages=True,can_invite_users=True,can_restrict_members=True,can_pin_messages=True)
            await q.edit_message_text('تم رفعه مشرف')
        except Exception as e:
            await q.answer(str(e),show_alert=True)
        return
    if d.startswith('dem_'):
        uid = int(d.split('_')[1])
        try:
            await c.bot.promote_chat_member(cid,uid,can_change_info=False,can_delete_messages=False,can_invite_users=False,can_restrict_members=False,can_pin_messages=False)
            await q.edit_message_text('تم تنزيله من الاشراف')
        except:
            pass
        return

async def text_handler(u,c):
    if not u.message:
        return
    msg = u.message
    txt = (msg.text or '').strip()
    cid = str(u.effective_chat.id)
    uid = msg.from_user.id
    name = msg.from_user.first_name

    if cid not in STATS:
        STATS[cid] = {}
    STATS[cid][str(uid)] = STATS[cid].get(str(uid),0) + 1
    save('stats.json',STATS)

    if 'A_TOOLS' in txt:
        try:
            await msg.delete()
        except:
            pass
        return

    if txt == '/start' or txt == 'الاوامر' or txt == 'اوامر':
        await msg.reply_text('الاوامر شغالة',reply_markup=kb_menu())
        return
    if txt == 'بوت':
        await msg.reply_text('نعم؟')
        return
    if txt == 'رتبتي':
        r = rank_of(uid,cid)
        cnt = STATS[cid].get(str(uid),0)
        await msg.reply_text(f'رتبتك => {r}\nرسائلك {cnt}')
        return
    if txt.startswith('رتبته'):
        target = None
        if msg.reply_to_message:
            target = msg.reply_to_message.from_user
        if target:
            r = rank_of(target.id,cid)
            await msg.reply_text(f'رتبته => {r}')
        return
    if txt.startswith('رفع Dev'):
        target = None
        if msg.reply_to_message:
            target = msg.reply_to_message.from_user
        if not target:
            await msg.reply_text('رد على الشخص')
            return
        r = get_r(cid)
        if target.id not in r['dev']:
            r['dev'].append(target.id)
        save('ranks.json',RANKS)
        await msg.reply_text(f'تم رفعه Dev - {target.first_name}')
        return
    if txt.startswith('رفع مشرف'):
        target = None
        if msg.reply_to_message:
            target = msg.reply_to_message.from_user
        if not target:
            await msg.reply_text('رد على الشخص')
            return
        await msg.reply_text(f'رفع مشرف {target.first_name}',reply_markup=kb_promote(target.id))
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
    if txt == 'قفل الاباحي' or txt == 'قفل الصور':
        if cid not in LOCKS:
            LOCKS[cid] = {}
        LOCKS[cid]['porn'] = True
        LOCKS[cid]['photo'] = True
        save('locks.json',LOCKS)
        await msg.reply_text('تم قفل الاباحي - الصور تنمسح')
        return
    if txt == 'فتح الاباحي' or txt == 'فتح الصور':
        if cid not in LOCKS:
            LOCKS[cid] = {}
        LOCKS[cid]['porn'] = False
        LOCKS[cid]['photo'] = False
        save('locks.json',LOCKS)
        await msg.reply_text('تم فتح الاباحي')
        return
    if txt == 'المطور':
        await msg.reply_text('@ADJkex')
        return

async def photo_handler(u,c):
    msg = u.message
    cid = str(u.effective_chat.id)
    if cid not in LOCKS:
        LOCKS[cid] = {}
    if LOCKS[cid].get('photo',True):
        try:
            await msg.delete()
        except:
            pass

async def edit_handler(u,c):
    if not u.edited_message:
        return
    cid = str(u.effective_chat.id)
    if cid not in LOCKS:
        return
    if LOCKS[cid].get('edit') != True:
        return
    try:
        await u.edited_message.delete()
        n = u.edited_message.from_user.first_name
        await c.bot.send_message(cid,f'{n} - بتعدل ثاني مره بيجي المطور يلعن امك')
    except:
        pass

async def new_member(u,c):
    msg = u.message
    cid = str(u.effective_chat.id)
    for user in msg.new_chat_members:
        if user.is_bot:
            if user.id == c.bot.id:
                continue
            try:
                await c.bot.ban_chat_member(cid,user.id)
                await msg.reply_text(f'منع البوتات - طرد {user.first_name}')
            except:
                pass

if __name__ == '__main__':
    if not TOKEN:
        raise RuntimeError('BOT_TOKEN missing')
    import asyncio
    threading.Thread(target=run_http,daemon=True).start()
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except:
        pass
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',cmd_start))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,new_member))
    app.add_handler(MessageHandler(filters.TEXT,text_handler))
    app.add_handler(MessageHandler(filters.PHOTO,photo_handler))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE,edit_handler))
    print('SORD CLEAN FINAL LIVE')
    app.run_polling()
