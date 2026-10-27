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
    b.append([InlineKeyboardButton('كتم',callback_data=f'mute_{uid}')])
    b.append([InlineKeyboardButton('صلاحياته',callback_data=f'pr_{uid}')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

async def start_cmd(u,c):
    await u.message.reply_text('هلا SORD شغال',reply_markup=kb_main())

async def on_cb(u,c):
    q=u.callback_query
    await q.answer()
    d=q.data
    cid=str(u.effective_chat.id)
    if d=='close':
        try: await q.message.delete()
        except: pass
        return
    if d=='back_main':
        await q.edit_message_text('الاوامر',reply_markup=kb_main())
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
    if d.startswith('ct_'):
        uid=d.split('_')[-1]
        await q.edit_message_text(f'التحكم {uid}',reply_markup=kb_control(uid,cid))
        return
    if d.startswith('pr_'):
        uid=d.split('_')[-1]
        await q.edit_message_text('لوحة الاشراف',reply_markup=kb_promote(int(uid)))
        return
    await q.answer('تم')

async def handle_all(u,c):
    if not u.message:
        return
    msg=u.message
    txt=(msg.text or msg.caption or '').strip()
    cid=str(u.effective_chat.id)
    uid=msg.from_user.id
    name=msg.from_user.first_name

    if cid not in STATS:
        STATS[cid]={}
    STATS[cid][str(uid)]=STATS[cid].get(str(uid),0)+1
    save('stats.json',STATS)

    if 'A_TOOLS' in txt or 'To use this bot' in txt:
        if not is_ranked(uid,cid):
            try: await msg.delete()
            except: pass
            return

    if cid in CUSTOM and txt in CUSTOM[cid]:
        await msg.reply_text(CUSTOM[cid][txt])
        return

    if txt=='بوت':
        await msg.reply_text(f'نعم يا {name}؟ @ADJkex')
        return
    if txt.startswith('/start'):
        await msg.reply_text('هلا SORD شغال',reply_markup=kb_main())
        return
    if txt=='استغفرالله' or txt=='استغفر الله':
        await msg.reply_text('استغفرالله العظيم واتوب اليه 🙏')
        return
    if txt=='رتبتي':
        rank=get_rank_text(uid,cid)
        cnt=STATS.get(cid,{}).get(str(uid),0)
        await msg.reply_text(f'رتبتك => {rank}\nرسائلك => {cnt}')
        return
    if txt.startswith('رتبته'):
        target=None
        if msg.reply_to_message:
            target=msg.reply_to_message.from_user
        if target:
            rank=get_rank_text(target.id,cid)
            cnt=STATS.get(cid,{}).get(str(target.id),0)
            await msg.reply_text(f'رتبته => {rank}\nرسائله => {cnt}')
        else:
            rank=get_rank_text(uid,cid)
            await msg.reply_text(f'رتبتك => {rank}')
        return
    if txt=='التفاعل' or txt=='تفاعلي':
        cnt=STATS.get(cid,{}).get(str(uid),0)
        await msg.reply_text(f'تفاعلك {cnt} رسالة')
        return
    if txt=='صلاحياته' or txt.startswith('صلاحياته'):
        target=None
        if msg.reply_to_message:
            target=msg.reply_to_message.from_user
        if not target:
            await msg.reply_text('رد على الشخص')
            return
        await msg.reply_text(f'صلاحيات {target.first_name}',reply_markup=kb_control(str(target.id),cid))
        return
    if txt.startswith('رفع Dev'):
        target=None
        if msg.reply_to_message:
            target=msg.reply_to_message.from_user
        if not target:
            await msg.reply_text('رد على الشخص')
            return
        r=get_r(cid)
        if target.id not in r['dev']:
            r['dev'].append(target.id)
        save('ranks.json',RANKS)
        await msg.reply_text(f'تم رفعه Dev {target.first_name}')
        return
    if txt.startswith('رفع مشرف'):
        target=None
        if msg.reply_to_message:
            target=msg.reply_to_message.from_user
        if not target:
            await msg.reply_text('رد على الشخص لرفعه مشرف')
            return
        await msg.reply_text(f'تم رفعه مشرف {target.first_name}',reply_markup=kb_promote(target.id))
        return
    if txt.startswith('التحكم'):
        target=None
        if msg.reply_to_message:
            target=msg.reply_to_message.from_user
        if not target:
            await msg.reply_text('رد على الشخص')
            return
        await msg.reply_text(f'التحكم {target.first_name}',reply_markup=kb_control(str(target.id),cid))
        return
    if txt.startswith('قفل التعديل'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['edit']=True
        save('locks.json',LOCKS)
        await msg.reply_text(f'بواسطة {name}\nتم قفل التعديل')
        return
    if txt.startswith('فتح التعديل'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['edit']=False
        save('locks.json',LOCKS)
        await msg.reply_text(f'بواسطة {name}\nتم فتح التعديل')
        return
    if txt.startswith('قفل الاباحي') or txt.startswith('قفل الصور'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['porn']=True
        LOCKS[cid]['photo']=True
        save('locks.json',LOCKS)
        await msg.reply_text('تم قفل الاباحي والصور')
        return
    if txt.startswith('فتح الاباحي') or txt.startswith('فتح الصور'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['porn']=False
        LOCKS[cid]['photo']=False
        save('locks.json',LOCKS)
        await msg.reply_text('تم فتح الاباحي')
        return
    if txt in ['الاوامر','اوامر']:
        await msg.reply_text('قائمة الاوامر',reply_markup=kb_main())
        return
    if txt.startswith('المطور'):
        await msg.reply_text('Developer @ADJkex - SORD بدون اشتراك اجباري')
        return

async def handle_photo(u,c):
    msg=u.message
    cid=str(u.effective_chat.id)
    uid=msg.from_user.id
    if cid not in LOCKS:
        LOCKS[cid]={}
    if LOCKS[cid].get('photo',True) or LOCKS[cid].get('porn',True):
        if not is_ranked(uid,cid):
            try: await msg.delete()
            except: pass

async def anti_edit(u,c):
    if not u.edited_message:
        return
    cid=str(u.effective_chat.id)
    if cid not in LOCKS:
        return
    if LOCKS[cid].get('edit')!=True:
        return
    try:
        await u.edited_message.delete()
        n=u.edited_message.from_user.first_name
        await c.bot.send_message(cid,f'{n} عدل - بتعدل ثاني مره بيجي المطور يلعن امك')
    except: pass

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
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,lambda u,c: handle_all(u,c)))
    app.add_handler(MessageHandler(filters.TEXT,handle_all))
    app.add_handler(MessageHandler(filters.PHOTO,handle_photo))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE,anti_edit))
    print('SORD REPLY LIVE')
    app.run_polling()
