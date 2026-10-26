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

def kb_services():
    b=[]
    b.append([InlineKeyboardButton('اذان',callback_data='svc_azan')])
    b.append([InlineKeyboardButton('الطقس',callback_data='svc_weather')])
    b.append([InlineKeyboardButton('التاريخ',callback_data='svc_date')])
    b.append([InlineKeyboardButton('الوقت',callback_data='svc_time')])
    b.append([InlineKeyboardButton('معنى',callback_data='svc_mean')])
    b.append([InlineKeyboardButton('ترجم',callback_data='svc_tr')])
    b.append([InlineKeyboardButton('العمر',callback_data='svc_age')])
    b.append([InlineKeyboardButton('زخرفه',callback_data='svc_zakh')])
    b.append([InlineKeyboardButton('وش يقول',callback_data='svc_say')])
    b.append([InlineKeyboardButton('العملات',callback_data='svc_cur')])
    b.append([InlineKeyboardButton('1 / 2',callback_data='svc_p1')])
    b.append([InlineKeyboardButton('التالي',callback_data='svc_next')])
    b.append([InlineKeyboardButton('رجوع',callback_data='fun_back')])
    b.append([InlineKeyboardButton('القائمة',callback_data='back_main')])
    return InlineKeyboardMarkup(b)

def kb_content():
    b=[]
    b.append([InlineKeyboardButton('قرآن',callback_data='cnt_quran')])
    b.append([InlineKeyboardButton('اغاني',callback_data='cnt_song')])
    b.append([InlineKeyboardButton('شعر',callback_data='cnt_poem')])
    b.append([InlineKeyboardButton('الختمه',callback_data='cnt_khat')])
    b.append([InlineKeyboardButton('اقتباس',callback_data='cnt_quote')])
    b.append([InlineKeyboardButton('حكمه',callback_data='cnt_hik')])
    b.append([InlineKeyboardButton('رساله',callback_data='cnt_msg')])
    b.append([InlineKeyboardButton('عبارات',callback_data='cnt_ph')])
    b.append([InlineKeyboardButton('قيفات بنات',callback_data='cnt_girls')])
    b.append([InlineKeyboardButton('كتب',callback_data='cnt_book')])
    b.append([InlineKeyboardButton('رجوع',callback_data='fun_back')])
    b.append([InlineKeyboardButton('القائمة',callback_data='back_main')])
    return InlineKeyboardMarkup(b)

def kb_lock():
    b=[]
    b.append([InlineKeyboardButton('قفل الاستفتاءات',callback_data='lock_poll')])
    b.append([InlineKeyboardButton('قفل تعديل المعلو',callback_data='lock_info')])
    b.append([InlineKeyboardButton('قفل الاضافه',callback_data='lock_add')])
    b.append([InlineKeyboardButton('قفل الرسائل الغنية',callback_data='lock_rich')])
    b.append([InlineKeyboardButton('قفل المتحركه',callback_data='lock_gif')])
    b.append([InlineKeyboardButton('قفل التعديل العادي',callback_data='lock_edit')])
    b.append([InlineKeyboardButton('قفل البوتات',callback_data='lock_bots')])
    b.append([InlineKeyboardButton('قفل الاغاني',callback_data='lock_music')])
    b.append([InlineKeyboardButton('قفل الشارحه',callback_data='lock_fwd')])
    b.append([InlineKeyboardButton('قفل القنوات',callback_data='lock_chan')])
    b.append([InlineKeyboardButton('رجوع',callback_data='back_settings')])
    return InlineKeyboardMarkup(b)

async def cmd_awamer(update,context):
    await update.message.reply_text('قائمة الاوامر',reply_markup=kb_main())

async def on_cb(update,context):
    q=update.callback_query
    await q.answer()
    d=q.data
    if d=='close':
        try:
            await q.message.delete()
        except:
            pass
        return
    if d=='back_main':
        await q.edit_message_text('قائمة الاوامر',reply_markup=kb_main())
        return

async def handle_text(update,context):
    if not update.message:
        return
    msg=update.message
    txt=(msg.text or '').strip()
    cid=str(update.effective_chat.id)
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
    app.add_handler(CommandHandler('start',cmd_awamer))
    app.add_handler(CallbackQueryHandler(on_cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_text))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE,anti_edit))
    print('RUNNING V5 FIXED')
    app.run_polling()
