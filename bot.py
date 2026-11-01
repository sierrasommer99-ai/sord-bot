import os,json,threading
from http.server import HTTPServer,BaseHTTPRequestHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler
from telegram.ext import CallbackQueryHandler,MessageHandler,filters

# TOKEN
TOKEN=os.getenv('BOT_TOKEN','').strip()

# LOAD/SAVE
def ld(f):
 try:
  return json.load(open(f,encoding='utf-8'))
 except:
  return {}

def sv(f,d):
 json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

# FILES
for fp in ['locks.json','toggles.json','custom.json','top.json','ranks.json']:
 if not os.path.exists(fp):
  sv(fp,{})

LOCKS=ld('locks.json')
TOGGLES=ld('toggles.json')
TOP=ld('top.json')
RANKS=ld('ranks.json')
WAITING={}

# RANKS
ALL_RANKS=[
'Dev','Dev2','MY','M',
'مالك المجموعه','مالك اساسي','مالك',
'منشئ اساسي','منشئ','مدير','ادمن','مميز'
]

# LOCKS P1
LOCKS_P1=[
'تعديل المعلومات',
'الاستفتاءات',
'الرسائل الغبيه',
'الاضافه',
'التعديل العادي',
'المتحركه',
'الاغاني',
'البوتات',
'القنوات',
'الشارحه',
'الجهات',
'الملصقات المميزه',
'الملفات',
'التفاعلات المميزه',
'التعديل',
'تعديل الميديا',
'الفارسيه',
'الانجليزيه',
'الالعاب',
'التوجيه'
]

# LOCKS P2
LOCKS_P2=[
'القيف اوي',
'التاك',
'الاعلانات',
'الاونلاين',
'التثبيت للكل',
'الابراج',
'الجنون',
'الدخول',
'الدخول بدون طلب',
'الكرتون',
'اللغات',
'الروابط',
'الرابط',
'المواقع',
'التنبيه',
'الماركداون',
'الوسائط',
'الوسائط المشفره',
'الارقام',
'الردود الخارجيه'
]

ALL_LOCKS=LOCKS_P1+LOCKS_P2

# SERVER
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  self.end_headers()
  self.wfile.write(b'SORD LIAM FULL 500 LINES')

def run():
 HTTPServer(
  ('0.0.0.0',int(os.getenv('PORT','10000'))),
  H
 ).serve_forever()

# KEYBOARDS
def kb_start():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('اضفني لقروبك',url='https://t.me/BOT?startgroup=true')],
  [InlineKeyboardButton('About SORD',callback_data='about')]
 ])

def kb_main():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('اوامر القروبات',callback_data='cmd_groups'),
   InlineKeyboardButton('اوامر التشغيل',callback_data='cmd_play')],
  [InlineKeyboardButton('اوامر القنوات',callback_data='cmd_channels'),
   InlineKeyboardButton('تكرار وتقديم وسر',callback_data='cmd_loop')],
  [InlineKeyboardButton('اوامر المطورين',callback_data='cmd_dev')],
  [InlineKeyboardButton('اغلاق',callback_data='close')]
 ])

def kb_groups():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('القفل والفتح',callback_data='lockpanel'),
   InlineKeyboardButton('التفعيل والتعطيل',callback_data='onoff')],
  [InlineKeyboardButton('التسلية والخدمية',callback_data='fun'),
   InlineKeyboardButton('ادارة القروب',callback_data='manage')],
  [InlineKeyboardButton('اوامر Dev',callback_data='dev'),
   InlineKeyboardButton('الاعدادات',callback_data='sets')],
  [InlineKeyboardButton('اغلاق',callback_data='close')]
 ])

def kb_lock_p1():
 b=[]
 b.append([
  InlineKeyboardButton('فتح الكل',callback_data='openall'),
  InlineKeyboardButton('قفل الكل',callback_data='closeall')
 ])
 for i in range(0,len(LOCKS_P1),2):
  b.append([
   InlineKeyboardButton(LOCKS_P1[i]+' -',callback_data=f'l_{LOCKS_P1[i]}'),
   InlineKeyboardButton(LOCKS_P1[i+1]+' -',callback_data=f'l_{LOCKS_P1[i+1]}')
  ])
 b.append([InlineKeyboardButton('الصفحة التالية',callback_data='page2')])
 b.append([
  InlineKeyboardButton('اغلاق',callback_data='close'),
  InlineKeyboardButton('الرئيسية',callback_data='cmd_groups')
 ])
 return InlineKeyboardMarkup(b)

def kb_lock_p2():
 b=[]
 b.append([
  InlineKeyboardButton('فتح الكل',callback_data='openall'),
  InlineKeyboardButton('قفل الكل',callback_data='closeall')
 ])
 for i in range(0,len(LOCKS_P2),2):
  b.append([
   InlineKeyboardButton(LOCKS_P2[i]+' -',callback_data=f'l_{LOCKS_P2[i]}'),
   InlineKeyboardButton(LOCKS_P2[i+1]+' -',callback_data=f'l_{LOCKS_P2[i+1]}')
  ])
 b.append([InlineKeyboardButton('الصفحة السابقة',callback_data='page1')])
 b.append([
  InlineKeyboardButton('اغلاق',callback_data='close'),
  InlineKeyboardButton('الرئيسية',callback_data='cmd_groups')
 ])
 return InlineKeyboardMarkup(b)

def kb_games():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('العاب جماعية',callback_data='g_group'),
   InlineKeyboardButton('العاب ادوار',callback_data='g_roles')],
  [InlineKeyboardButton('كلمات وحروف',callback_data='g_words'),
   InlineKeyboardButton('تحدي واستنتاج',callback_data='g_chal')],
  [InlineKeyboardButton('اسئلة ومعلومات',callback_data='g_q'),
   InlineKeyboardButton('صور وتخمين',callback_data='g_pic')],
  [InlineKeyboardButton('مقالات وسرعة',callback_data='g_fast'),
   InlineKeyboardButton('تسلية القروب',callback_data='g_fun')],
  [InlineKeyboardButton('حظ وقرعة',callback_data='g_luck'),
   InlineKeyboardButton('عوائل وتيناس',callback_data='g_fam')],
  [InlineKeyboardButton('مسابقات وقلابات',callback_data='g_race'),
   InlineKeyboardButton('احصائياتي',callback_data='g_me')],
  [InlineKeyboardButton('توب الادمين',callback_data='g_topadmin'),
   InlineKeyboardButton('توب المتفاعلين',callback_data='g_top')],
  [InlineKeyboardButton('اغلاق',callback_data='close')]
 ])

def kb_back():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('رجوع',callback_data='cmd_main'),
   InlineKeyboardButton('اغلاق',callback_data='close')]
 ])

# START
async def start(u,c):
 if u.effective_chat.type=='private':
  text="هلا عزيزي انا سورد\n\n"
  text+="اقوى واسرع بوت حماية وتشغيل ميوزك\n"
  text+="والعديد من المميزات الاخرى\n\n"
  text+="اذا رفعتني مشرف بتفعل تلقائيا\n"
  text+="اضغط الاعدادات وضبط اعداداتي\n\n"
  text+="مافيني اي مطور ومسؤول غير Liam\n\n"
  text+="حساب مطوري - Liam"
  await u.message.reply_text(text,reply_markup=kb_start())
 else:
  await u.message.reply_text(
   'قائمة الاوامر - سورد\nاختر القسم',
   reply_markup=kb_groups()
  )

# CALLBACK
async def cb(u,c):
 q=u.callback_query
 await q.answer()
 d=q.data
 cid=str(u.effective_chat.id)

 if d=='close':
  try:
   await q.message.delete()
  except:
   await q.edit_message_text('CLOSED BY : Liam')
  return

 if d=='cmd_main':
  await q.edit_message_text(
   'قائمة الاوامر\nاختر القسم',
   reply_markup=kb_main()
  )
  return

 if d=='cmd_groups':
  await q.edit_message_text(
   'قائمة الاوامر\nاختر القسم\nكل امر له شرحه',
   reply_markup=kb_groups()
  )
  return

 if d=='cmd_play':
  await q.edit_message_text(
   'اوامر التشغيل\n\nشغل - تشغيل صوت\n/playforce - تشغيل فورا\n/skip - تخطي\n/queue - قائمة',
   reply_markup=kb_back()
  )
  return

 if d=='cmd_loop':
  await q.edit_message_text(
   'التكرار\n/loop - تكرار\n/shuffle - خلط\n/seek - تقديم',
   reply_markup=kb_back()
  )
  return

 if d=='cmd_channels':
  await q.edit_message_text(
   'اوامر القنوات\nربط القناة',
   reply_markup=kb_back()
  )
  return

 if d=='cmd_dev':
  await q.edit_message_text(
   'اوامر المطورين\nللمطور الاساسي',
   reply_markup=kb_back()
  )
  return

 if d in ['lockpanel','page1']:
  await q.edit_message_text(
   'لوحة القفل والفتح - صفحة 1',
   reply_markup=kb_lock_p1()
  )
  return

 if d=='page2':
  await q.edit_message_text(
   'لوحة القفل والفتح - صفحة 2',
   reply_markup=kb_lock_p2()
  )
  return

 if d=='openall':
  LOCKS.setdefault(cid,{})
  for k in ALL_LOCKS:
   LOCKS[cid][k]=False
  sv('locks.json',LOCKS)
  await q.edit_message_text('تم فتح الكل',reply_markup=kb_lock_p1())
  return

 if d=='closeall':
  LOCKS.setdefault(cid,{})
  for k in ALL_LOCKS:
   LOCKS[cid][k]=True
  sv('locks.json',LOCKS)
  await q.edit_message_text('تم قفل الكل',reply_markup=kb_lock_p1())
  return

 if d.startswith('l_'):
  name=d[2:]
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]=not LOCKS[cid].get(name,False)
  sv('locks.json',LOCKS)
  page=kb_lock_p1() if name in LOCKS_P1 else kb_lock_p2()
  st='تم قفل' if LOCKS[cid][name] else 'تم فتح'
  await q.edit_message_text(f'{st} {name}',reply_markup=page)
  return

 if d.startswith('g_'):
  if d=='g_top':
   await q.edit_message_text(
    'توب 20\n1) ديف\n2) RORY\n... 20) Enzo',
    reply_markup=kb_games()
   )
   return
  await q.edit_message_text(
   'مركز الالعاب\nاختر التصنيف',
   reply_markup=kb_games()
  )
  return

 if d=='about':
  await q.edit_message_text(
   'SORD - سورد\nالمطور : Liam',
   reply_markup=kb_back()
  )
  return

# TEXT
async def txt(u,c):
 if not u.message:
  return
 m=u.message
 t=(m.text or '').strip()
 cid=str(u.effective_chat.id)
 uid=str(m.from_user.id)

 if 'A_TOOLS' in t:
  return

 TOP.setdefault(cid,{})
 TOP[cid][uid]=TOP[cid].get(uid,0)+1
 sv('top.json',TOP)

 if cid in WAITING:
  if WAITING[cid].get('step')=='old_del':
   WAITING[cid]={'step':'confirm_del','old':t}
   await m.reply_text(f'الامر القديم : ( {t} )')
   return
  if WAITING[cid].get('step')=='confirm_del' and t=='الغاء':
   old=WAITING[cid]['old']
   del WAITING[cid]
   await m.reply_text(f'تم ازالة الامر .. ( {old} )')
   return

 if t in ['الاوامر','اوامر','قائمة الاوامر']:
  await m.reply_text('قائمة الاوامر',reply_markup=kb_main())
  return

 if t.startswith('قفل امر'):
  rank=t.replace('قفل امر','').strip()
  await m.reply_text(f'سيتم وضع الامر {rank} للرتبة')
  return

 if t in ['الرتب','الرتبي']:
  await m.reply_text(
   'الرتب المتاحة :\nDev\nDev2\nMY\nM\nمالك\nمنشئ\nمدير\nادمن\nمميز'
  )
  return

 if t=='قفل الرتب':
  await m.reply_text('ارسل الرتبة الان :\nDev\nMY\nM\nمالك\nمنشئ\nمدير\nادمن')
  return

 if t in ['المطور','SORD','Liam','ليام']:
  await m.reply_text('SORD - سورد\nالمطور : Liam')
  return

 if t.startswith('اهمس'):
  await m.reply_text('طريقة اهمس\nرد على رسالة واكتب اهمس')
  return

 if t=='تعطيل الالعاب':
  TOGGLES.setdefault(cid,{})['العاب']=False
  sv('toggles.json',TOGGLES)
  await m.reply_text(f'تم تعطيل الالعاب')
  return

 if t=='تفعيل الالعاب':
  TOGGLES.setdefault(cid,{})['العاب']=True
  sv('toggles.json',TOGGLES)
  await m.reply_text(f'تم تفعيل الالعاب')
  return

 if t in ['مسح امر','حذف امر']:
  WAITING[cid]={'step':'old_del'}
  await m.reply_text('ارسل الامر القديم')
  return

 if t=='الغاء':
  await m.reply_text('تم ازالة الامر .. ( الغاء )')
  return

 if t=='حظر':
  await m.reply_text('طريقة حظر\nرد + حظر')
  return

 # قفل وفتح نصي
 if t.startswith('قفل') and len(t)>3:
  name=t.replace('قفل','').strip()
  if name in ['الرتب','امر']:
   return
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]=True
  sv('locks.json',LOCKS)
  await m.reply_text(f'تم قفل {name}')
  return

 if t.startswith('فتح') and len(t)>3:
  name=t.replace('فتح','').strip()
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]=False
  sv('locks.json',LOCKS)
  await m.reply_text(f'تم فتح {name}')
  return

 if t=='الالعاب':
  await m.reply_text('مركز الالعاب',reply_markup=kb_games())
  return

 if t in ['توب المتفاعلين','توب']:
  await m.reply_text('توب 20\n1) ديف\n2) RORY...')
  return

 if t=='القفل والفتح':
  await m.reply_text('لوحة القفل',reply_markup=kb_lock_p1())
  return

# قفل التعديل - الميزة الجديدة
async def edited(u,c):
 if not u.edited_message:
  return
 m=u.edited_message
 cid=str(m.chat.id)
 # لو قفل التعديل مفعل
 if LOCKS.get(cid,{}).get('التعديل',False):
  try:
   await m.delete()
  except:
   pass
  try:
   await c.bot.send_message(
    chat_id=m.chat.id,
    text="لو تعدل بلعن امك"
   )
  except:
   pass

# تشغيل
if __name__=='__main__':
 if not TOKEN:
  raise RuntimeError('TOKEN')

 import asyncio
 threading.Thread(target=run,daemon=True).start()

 try:
  loop=asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
 except:
  pass

 app=ApplicationBuilder().token(TOKEN).build()
 app.add_handler(CommandHandler('start',start))
 app.add_handler(CallbackQueryHandler(cb))
 app.add_handler(MessageHandler(
  filters.TEXT & ~filters.UpdateType.EDITED_MESSAGE,
  txt
 ))
 app.add_handler(MessageHandler(
  filters.UpdateType.EDITED_MESSAGE,
  edited
 ))
 print('SORD LIAM FULL 300 LINES LIVE')
 app.run_polling()
