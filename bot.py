import os
import threading
import json
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

for fp in ['locks.json','ranks.json','data.json','stats.json','custom.json','bans.json']:
    if not os.path.exists(fp):
        save(fp,{})

LOCKS=load('locks.json')
RANKS=load('ranks.json')
CUSTOM=load('custom.json')
STATS=load('stats.json')
DATA=load('data.json')

def get_r(cid):
    cid=str(cid)
    if cid not in RANKS:
        RANKS[cid]={'asasi':[],'dev2':[],'dev':[],'myth':[],'games':[],'hms':[]}
    return RANKS[cid]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'SORD V5 FULL LIVE')

def run_server():
    p=int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()

def kb_main():
    b=[]
    b.append([InlineKeyboardButton('القفل والفتح',callback_data='menu_lock')])
    b.append([InlineKeyboardButton('التفعيل والتعطيل',callback_data='menu_toggle')])
    b.append([InlineKeyboardButton('ادارة القروب',callback_data='menu_admin')])
    b.append([InlineKeyboardButton('التسلية والخدمية',callback_data='menu_fun')])
    b.append([InlineKeyboardButton('اوامر Dev',callback_data='menu_dev')])
    b.append([InlineKeyboardButton('الاعدادات',callback_data='menu_settings')])
    b.append([InlineKeyboardButton('اغلاق',callback_data='close')])
    return InlineKeyboardMarkup(b)

def kb_fun():
    b=[]
    b.append([InlineKeyboardButton('الخدمات',callback_data='show_services')])
    b.append([InlineKeyboardButton('المحتوى',callback_data='show_content')])
    b.append([InlineKeyboardButton('رتب التسلية',callback_data='fun_rank')])
    b.append([InlineKeyboardButton('التسلية',callback_data='fun_games')])
    b.append([InlineKeyboardButton('رجوع',callback_data='back_main')])
    return InlineKeyboardMarkup(b)

def kb_services():
    b=[]
    b.append([InlineKeyboardButton('اذان',callback_data='s_azan')])
    b.append([InlineKeyboardButton('الطقس',callback_data='s_weather')])
    b.append([InlineKeyboardButton('التاريخ',callback_data='s_date')])
    b.append([InlineKeyboardButton('الوقت',callback_data='s_time')])
    b.append([InlineKeyboardButton('معنى',callback_data='s_mean')])
    b.append([InlineKeyboardButton('ترجم',callback_data='s_tr')])
    b.append([InlineKeyboardButton('العمر',callback_data='s_age')])
    b.append([InlineKeyboardButton('زخرفه',callback_data='s_zakh')])
    b.append([InlineKeyboardButton('وش يقول',callback_data='s_say')])
    b.append([InlineKeyboardButton('العملات',callback_data='s_cur')])
    b.append([InlineKeyboardButton('رجوع',callback_data='fun_back')])
    b.append([InlineKeyboardButton('القائمة',callback_data='back_main')])
    return InlineKeyboardMarkup(b)

def kb_content():
    b=[]
    b.append([InlineKeyboardButton('قرآن',callback_data='c_quran')])
    b.append([InlineKeyboardButton('اغاني',callback_data='c_song')])
    b.append([InlineKeyboardButton('شعر',callback_data='c_poem')])
    b.append([InlineKeyboardButton('الختمه',callback_data='c_khat')])
    b.append([InlineKeyboardButton('اقتباس',callback_data='c_quote')])
    b.append([InlineKeyboardButton('حكمه',callback_data='c_hik')])
    b.append([InlineKeyboardButton('رساله',callback_data='c_msg')])
    b.append([InlineKeyboardButton('عبارات',callback_data='c_ph')])
    b.append([InlineKeyboardButton('قيفات بنات',callback_data='c_girls')])
    b.append([InlineKeyboardButton('كتب',callback_data='c_book')])
    b.append([InlineKeyboardButton('رجوع',callback_data='fun_back')])
    return InlineKeyboardMarkup(b)

def kb_lock():
    b=[]
    b.append([InlineKeyboardButton('قفل الاستفتاءات',callback_data='l_poll')])
    b.append([InlineKeyboardButton('قفل تعديل المعلو',callback_data='l_info')])
    b.append([InlineKeyboardButton('قفل الاضافه',callback_data='l_add')])
    b.append([InlineKeyboardButton('قفل الرسائل الغنية',callback_data='l_rich')])
    b.append([InlineKeyboardButton('قفل المتحركه',callback_data='l_gif')])
    b.append([InlineKeyboardButton('قفل التعديل العادي',callback_data='l_edit')])
    b.append([InlineKeyboardButton('قفل البوتات',callback_data='l_bots')])
    b.append([InlineKeyboardButton('قفل الاغاني',callback_data='l_music')])
    b.append([InlineKeyboardButton('قفل الشارحه',callback_data='l_fwd')])
    b.append([InlineKeyboardButton('قفل القنوات',callback_data='l_chan')])
    b.append([InlineKeyboardButton('رجوع',callback_data='back_settings')])
    return InlineKeyboardMarkup(b)

def kb_toggle():
    b=[]
    b.append([InlineKeyboardButton('تفعيل اكتموه',callback_data='t_kt')])
    b.append([InlineKeyboardButton('تفعيل اسباب المش',callback_data='t_asbab')])
    b.append([InlineKeyboardButton('تفعيل ثنائي اليوم',callback_data='t_day')])
    b.append([InlineKeyboardButton('تفعيل امسح',callback_data='t_erase')])
    b.append([InlineKeyboardButton('تفعيل زواج',callback_data='t_zwaj')])
    b.append([InlineKeyboardButton('تفعيل التحذير',callback_data='t_warn')])
    b.append([InlineKeyboardButton('تفعيل الحظر',callback_data='t_ban')])
    b.append([InlineKeyboardButton('تفعيل الخدميه',callback_data='t_khd')])
    b.append([InlineKeyboardButton('تفعيل البنك',callback_data='t_bank')])
    b.append([InlineKeyboardButton('تفعيل نبذه',callback_data='t_bio')])
    b.append([InlineKeyboardButton('رجوع',callback_data='back_settings')])
    return InlineKeyboardMarkup(b)

async def start_cmd(update,context):
    await update.message.reply_text('SORD LIVE - الاوامر',reply_markup=kb_main())

async def on_cb(update,context):
    q=update.callback_query
    await q.answer()
    d=q.data
    cid=str(update.effective_chat.id)
    if d=='close':
        try:
            await q.message.delete()
        except:
            pass
        return
    if d=='back_main':
        await q.edit_message_text('قائمة الاوامر\nاختر القسم',reply_markup=kb_main())
        return
    if d=='menu_fun':
        await q.edit_message_text('التسلية والخدمية',reply_markup=kb_fun())
        return
    if d=='show_services':
        await q.edit_message_text('الخدمات\nالصفحة 1 من 2',reply_markup=kb_services())
        return
    if d=='show_content':
        await q.edit_message_text('المحتوى\nالصفحة 1 من 2',reply_markup=kb_content())
        return
    if d=='fun_back':
        await q.edit_message_text('التسلية والخدمية',reply_markup=kb_fun())
        return
    if d=='menu_settings' or d=='back_settings':
        await q.edit_message_text('اعدادات القروب',reply_markup=kb_main())
        return
    if d=='menu_lock':
        await q.edit_message_text('القفل والفتح\nالصفحة 1 من 6',reply_markup=kb_lock())
        return
    if d=='menu_toggle':
        await q.edit_message_text('التفعيل والتعطيل\nالصفحة 1 من 7',reply_markup=kb_toggle())
        return
    if d=='l_edit':
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['edit']=not LOCKS[cid].get('edit',False)
        save('locks.json',LOCKS)
        s='مقفل' if LOCKS[cid]['edit'] else 'مفتوح'
        await q.answer(f'التعديل {s}',show_alert=True)
        return
    await q.answer('تم',show_alert=False)

async def handle_text(update,context):
    if not update.message:
        return
    msg=update.message
    txt=(msg.text or '').strip()
    cid=str(update.effective_chat.id)
    uid=msg.from_user.id
    if cid not in STATS:
        STATS[cid]={}
    STATS[cid][str(uid)]=STATS[cid].get(str(uid),0)+1
    save('stats.json',STATS)

    if cid in CUSTOM and txt in CUSTOM[cid]:
        await msg.reply_text(CUSTOM[cid][txt])
        return

    if txt in ['الاوامر','اوامر']:
        await msg.reply_text('قائمة الاوامر',reply_markup=kb_main())
        return

    if txt.startswith('قفل التعديل'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['edit']=True
        save('locks.json',LOCKS)
        await msg.reply_text(f'بواسطة {msg.from_user.first_name}\nتم قفل التعديل')
        return

    if txt.startswith('فتح التعديل'):
        if cid not in LOCKS:
            LOCKS[cid]={}
        LOCKS[cid]['edit']=False
        save('locks.json',LOCKS)
        await msg.reply_text(f'بواسطة {msg.from_user.first_name}\nتم فتح التعديل')
        return

    if txt.startswith('رتبته') or txt.startswith('رتبتي'):
        r=get_r(cid)
        rank='عضو'
        if uid in r['asasi']:
            rank='Dev الاساسي'
        elif uid in r['dev2']:
            rank='Dev2'
        await msg.reply_text(f'رتبته: {rank}')
        return

    if txt.startswith('اضف امر'):
        parts=txt.split(' ',2)
        if len(parts)>=3:
            name=parts[2]
            DATA['wait_custom']=name
            DATA['wait_cid']=cid
            save('data.json',DATA)
            await msg.reply_text(f'ارسل محتوى الامر {name}')
        return

    if 'wait_custom' in DATA and DATA.get('wait_cid')==cid:
        name=DATA['wait_custom']
        if cid not in CUSTOM:
            CUSTOM[cid]={}
        CUSTOM[cid][name]=txt
        save('custom.json',CUSTOM)
        del DATA['wait_custom']
        del DATA['wait_cid']
        save('data.json',DATA)
        await msg.reply_text(f'تم حفظ الامر باسم {name}')
        return

    if txt.startswith('المطور'):
        await msg.reply_text('Developer Bot -> SORD\nUSE -> @ADJkex')
        return

    if txt.startswith('توب القروبات'):
        tops=sorted(STATS.items(),key=lambda x: sum(x[1].values()),reverse=True)[:10]
        out='توب اكثر 10 قروبات يرسلون رسائل :\n'
        for i,(c,users) in enumerate(tops,1):
            total=sum(users.values())
            out+=f'{i}) {c} : {total}\n'
        await msg.reply_text(out)
        return

    if txt.startswith('الالعاب'):
        await msg.reply_text('مركز الالعاب')
        return

async def anti_edit(update,context):
    if not update.edited_message:
        return
    cid=str(update.effective_chat.id)
    if cid not in LOCKS:
        return
    if LOCKS[cid].get('edit')!=True:
        return
    try:
        await update.edited_message.delete()
        n=update.edited_message.from_user.first_name
        await context.bot.send_message(cid,f'المستخدم {n} قام بالتعديل - بتعدل ثاني مره بيجي المطور يلعن امك')
    except:
        pass

if __name__=='__main__':
    if not TOKEN:
        raise RuntimeError('TOKEN missing')
    import asyncio
    threading.Thread(target=run_server,daemon=True).start()
    try:
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    except:
        pass
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_cmd))
    app.add_handler(CallbackQueryHandler(on_cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_text))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE,anti_edit))
    print('SORD FULL V5 LIVE')
    app.run_polling()
