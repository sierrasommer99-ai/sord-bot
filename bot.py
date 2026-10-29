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
    b.append([InlineKeyboardButton('م1 حماية',callback_data='m1')])
    b.append([InlineKeyboardButton('م2 رفع',callback_data='m2')])
    b.append([InlineKeyboardButton('م3 حظر',callback_data='m3')])
    b.append([InlineKeyboardButton('م6 اعضاء',callback_data='m6')])
    b.append([InlineKeyboardButton('الاعدادات',callback_data='sets')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)
def kb_prom(uid):
    b=[]
    b.append([InlineKeyboardButton('بكامل الصلاحيات',callback_data=f'pa_{uid}')])
    b.append([InlineKeyboardButton('تنزيله',callback_data=f'dm_{uid}')])
    b.append([InlineKeyboardButton('التحكم',callback_data=f'ct_{uid}')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)
async def cmd_start(u,c):
    await u.message.reply_text('سترونق - SORD @ADJkex',reply_markup=kb_menu())
async def cb_all(u,c):
    q=u.callback_query; await q.answer(); d=q.data; cid=str(u.effective_chat.id)
    if d=='close':
        try: await q.message.delete()
        except: pass
        return
    if d=='m1': await q.edit_message_text('م1: قفل الروابط - المعرف - التاك - الصور - الفيديو - البوتات - التعديل - الاباحي - الكل',reply_markup=kb_menu()); return
    if d=='m2': await q.edit_message_text('م2: رفع مالك - منشئ - مدير - ادمن - مميز - مطور - Dev',reply_markup=kb_menu()); return
    if d=='m3': await q.edit_message_text('م3: كتم - حظر - تقيد - طرد',reply_markup=kb_menu()); return
    if d=='m6': await q.edit_message_text('م6: ايدي - رتبتي - تفاعلي - كشف',reply_markup=kb_menu()); return
    if d=='sets':
        out='الاعدادات:\n'
        for k,v in LOCKS.get(cid,{}).items(): out+=f'{k}:{"مقفل" if v else "مفتوح"}\n'
        await q.edit_message_text(out,reply_markup=kb_menu()); return
    if d.startswith('pa_'):
        uid=int(d.split('_')[1])
        try: await c.bot.promote_chat_member(cid,uid,can_change_info=True,can_delete_messages=True,can_invite_users=True,can_restrict_members=True,can_pin_messages=True,can_promote_members=True); await q.edit_message_text('تم رفعه')
        except Exception as e: await q.answer(str(e),show_alert=True)
        return
    if d.startswith('dm_'):
        uid=int(d.split('_')[1])
        try: await c.bot.promote_chat_member(cid,uid,can_change_info=False,can_delete_messages=False,can_invite_users=False,can_restrict_members=False,can_pin_messages=False,can_promote_members=False); await q.edit_message_text('تم تنزيله')
        except: pass
        return
async def text_all(u,c):
    if not u.message: return
    msg=u.message; txt=(msg.text or '').strip(); cid=str(u.effective_chat.id); uid=msg.from_user.id; name=msg.from_user.first_name; low=txt.lower()
    if cid not in STATS: STATS[cid]={}
    STATS[cid][str(uid)]=STATS[cid].get(str(uid),0)+1; save
