import os,json,threading,re,time,random
os.environ['PYTHONIOENCODING']='utf-8'
os.environ['PYTHONUTF8']='1'
from http.server import HTTPServer,BaseHTTPRequestHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,ChatPermissions
from telegram.ext import ApplicationBuilder,CommandHandler,CallbackQueryHandler,MessageHandler,filters

TOKEN=os.getenv('BOT_TOKEN','').strip() or os.getenv('TOKEN','').strip() or "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"

def ld(f):
 try:
  return json.load(open(f,encoding='utf-8'))
 except:
  return {}
def sv(f,d):
 json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

# FILES - مع enable و ranks_new + كل الملفات القديمة
for fp in ['locks.json','toggles.json','custom.json','top.json','ranks.json','muted.json','warnings.json','violations.json','private_mode.json','enable.json','ranks_new.json','limits.json','limits_usage.json','auto_download.json','last_seen.json','dev_list.json','pending_dev.json','private_restrict.json','dev_main.json','malik.json','admin_perms.json','music_queue.json','music_state.json','music_loop.json','channel_links.json','custom.json']:
 if not os.path.exists(fp):
  sv(fp,{})

LOCKS=ld('locks.json')
if not LOCKS:
 LOCKS={}
TOGGLES=ld('toggles.json')
PRIVATE_MODE=ld('private_mode.json')
if not PRIVATE_MODE:
 PRIVATE_MODE={}
TOP=ld('top.json')
RANKS=ld('ranks.json')
MUTED=ld('muted.json')
WARNINGS=ld('warnings.json')
VIOLATIONS=ld('violations.json')
ENABLE=ld('enable.json')
if not ENABLE:
 ENABLE={}
RANKS_NEW=ld('ranks_new.json')
if not RANKS_NEW:
 RANKS_NEW={}
CUSTOM=ld('custom.json')
if not CUSTOM:
 CUSTOM={}
ADMIN_PERMS=ld('admin_perms.json')
if not ADMIN_PERMS:
 ADMIN_PERMS={}
MUSIC_QUEUE={}
MUSIC_STATE={}
MUSIC_LOOP={}
CHANNEL_LINKS={}

def is_enabled(cid):
 cid=str(cid)
 if cid in ENABLE and ENABLE[cid].get('disabled', False):
  return False
 return True

def set_lock(cid, name, val):
 cid=str(cid)
 if cid not in LOCKS:
  LOCKS[cid]={}
 LOCKS[cid][name]=val
 sv('locks.json',LOCKS)

def is_locked(cid,name):
 return LOCKS.get(str(cid),{}).get(name,False)

def get_r_new(cid):
 cid=str(cid)
 if cid not in RANKS_NEW:
  RANKS_NEW[cid]={'eqama':[]}
 if 'eqama' not in RANKS_NEW[cid]:
  RANKS_NEW[cid]['eqama']=[]
 return RANKS_NEW[cid]

def save_r_new():
 sv('ranks_new.json',RANKS_NEW)

def is_owner(user):
 if not user:
  return False
 if user.username=='afiwd':
  return True
 return False

# ---------- نظام القفل 6 صفحات مثل داركنس ----------
LOCKS_PAGES = {
1: ['تعديل المعلومات','الاستفتاءات','الرسائل الغنية','الاضافه','التعديل العادي','المتحركه','الاغاني','البوتات','القنوات','الشارحه'],
2: ['الجهات','الملصقات المميزة','الملفات','التفاعلات المميزة','التعديل','تعديل الميديا','الفارسيه','الانجليزيه','التوجيه','الالعاب'],
3: ['التاك','القيف اواي','الاعلانات','الانلاين','الانلاين للكل','الايرانيين','الدخول','الجمثون','الكيبورد','الدخول بدون طلب'],
4: ['الروابط','اللغات','المواقع','الربط','الماركداون','التثبيت','الوسائط المشفرة','الوسائط','الردود الخارجيه','الأرقام'],
5: ['الاكواد','الصور','الروسي','الاقتباسات','التكرار','السب','الكلايش','التفليش','الملصقات','التشويش'],
6: ['الاشعارات','القصص','التقليد','الدردشه','المعرفات','السيلفي','الفيديو','الصوت','الانتهاكات']
}

def get_lock_text(cid, name):
 locked = LOCKS.get(str(cid),{}).get(name, False)
 if locked:
  return f"🔵 -{name}"
 else:
  return f"🟢 -{name}"

def kb_lock_page(cid, page):
 page = max(1, min(6, page))
 locks = LOCKS_PAGES.get(page, [])
 kb = []
 kb.append([InlineKeyboardButton('• فتح الكل',callback_data=f'openall_{page}'), InlineKeyboardButton('• قفل الكل',callback_data=f'closeall_{page}')])
 for i in range(0, len(locks), 2):
  row = []
  for j in range(2):
   if i+j < len(locks):
    name = locks[i+j]
    row.append(InlineKeyboardButton(get_lock_text(cid, name), callback_data=f'lock_{name}'))
  kb.append(row)
 if page==1:
  kb.append([InlineKeyboardButton('• الصفحة التالية',callback_data='lockpage_2')])
 elif page==6:
  kb.append([InlineKeyboardButton('• الصفحة السابقة',callback_data='lockpage_5')])
 else:
  kb.append([InlineKeyboardButton('• الصفحة السابقة',callback_data=f'lockpage_{page-1}'), InlineKeyboardButton('• الصفحة التالية',callback_data=f'lockpage_{page+1}')])
 kb.append([InlineKeyboardButton('• اخفاء',callback_data='close')])
 kb.append([InlineKeyboardButton('• العودة للقائمة الرئيسية',callback_data='cmd_groups')])
 kb.append([InlineKeyboardButton(f'{page} / 6',callback_data='noop'), InlineKeyboardButton('• رجوع',callback_data='cmd_groups')])
 return InlineKeyboardMarkup(kb)

def kb_lock_p1():
 return kb_lock_page('0',1)

LOCK_PANEL_TEXT = '''القفل والفتح
—————————
• تقفل وتفتح انواع الرسائل والمحتوى في القروب
• الصفحة {page} من 6

• اضغط على الامر عشان يطلع شرحه'''

GAMES_DATA = {
 'كت تويت': {'desc': 'يطلع لك تويتات جاهزة', 'play': 'اكتب كت تويت', 'players': '1', 'win': 'تسلية'},
 'اذكار': {'desc': 'يطلع لك ذكر', 'play': 'اكتب اذكار', 'players': '1', 'win': 'اجر'},
 'حظ': {'desc': 'يطلع لك نسبة حظك', 'play': 'اكتب حظ', 'players': '1', 'win': 'حظك'},
 'العقاب': {'desc': 'لعبة العقاب - اللي يخسر يتعاقب', 'play': 'اكتب العقاب', 'players': '2+', 'win': 'تهرب من العقاب'},
 'الحكم': {'desc': 'لعبة الحكم - تحكم على اللي يخسر', 'play': 'اكتب الحكم', 'players': '2+', 'win': 'تحكم على غيرك'},
 'الكرسي': {'desc': 'لعبة الكرسي - اسئلة جريئة', 'play': 'اكتب الكرسي', 'players': '2+', 'win': 'تجاوب بصراحة'},
 'اسئلة': {'desc': 'اسئلة متنوعة ومحيرة', 'play': 'اكتب اسئلة', 'players': '1+', 'win': 'تجاوب صح'},
 'لعبني': {'desc': 'لعبة لعبني - البوت يلعبك', 'play': 'اكتب لعبني', 'players': '1 ضد البوت', 'win': 'تفوز على البوت'},
 'حجر ورقة مقص': {'desc': 'لعبة حجر ورقة مقص', 'play': 'اكتب حجر', 'players': '1 ضد البوت', 'win': 'تفوز على البوت'},
 'نسبة الحب': {'desc': 'يحسب نسبة الحب بينك وبين شخص', 'play': 'اكتب نسبة الحب + منشن', 'players': '2', 'win': 'الحب'},
}

def get_game_text(name):
 g = GAMES_DATA.get(name)
 if not g:
  return f"لعبة {name}\nالشرح : تسلية\nطريقة اللعب : اكتب {name}\nعدد اللاعبين : 1\nطريقة الفوز : تسلية"
 return f"🎮 {name}\n\nالشرح : {g['desc']}\nطريقة اللعب : {g['play']}\nعدد اللاعبين : {g['players']}\nطريقة الفوز : {g['win']}"

WAITING={}
ALL_RANKS=['Dev','Dev2','MY','M','Extra','مالك اساسي','مالك','منشئ اساسي','منشئ','مدير','ادمن','مميز']
LOCKS_P1=['تعديل المعلومات','الاستفتاءات','الرسائل الغبيه','الاضافه','التعديل العادي','المتحركه','الاغاني','البوتات','القنوات','الشارحه','الجهات','الملصقات المميزه','الملفات','التفاعلات المميزه','التعديل','تعديل الميديا','الفارسيه','الانجليزيه','الالعاب','التوجيه']
LOCKS_P2=['الاباحي','القيف اوي','التاك','الاعلانات','الاونلاين','التثبيت للكل','الابراج','الجنون','الدخول','الدخول بدون طلب','الكرتون','اللغات','الروابط','الرابط','المواقع','التنبيه','الماركداون','الوسائط','الوسائط المشفره','الارقام','الردود الخارجيه']
ALL_LOCKS=LOCKS_P1+LOCKS_P2

class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  self.end_headers()
  self.wfile.write(b'SORD BOT RUNNING')
 def log_message(self,*a,**k):
  return

def run():
 try:
  port=int(os.getenv('PORT','10000'))
  HTTPServer(('0.0.0.0',port),H).serve_forever()
 except Exception as e:
  print(f"HTTP ERROR {e}")

def kb_groups():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• ادارة القروب •',callback_data='manage'), InlineKeyboardButton('• التسلية والخدمية •',callback_data='fun')],
  [InlineKeyboardButton('• اوامر Dev •',callback_data='dev')],
  [InlineKeyboardButton('• الإعدادات •',callback_data='sets')],
  [InlineKeyboardButton('• اغلاق •',callback_data='close')]
 ])

def kb_commands():
 return kb_groups()

def kb_games():
 kb=[]
 for name in GAMES_DATA:
  kb.append([InlineKeyboardButton(name,callback_data=f'game_{name}')])
 kb.append([InlineKeyboardButton('• اغلاق •',callback_data='close')])
 return InlineKeyboardMarkup(kb)

def kb_violation(vid):
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• إلغاء الإنذار', callback_data=f'v_{vid}_unwarn'), InlineKeyboardButton('• الرسالة سليمة', callback_data=f'v_{vid}_safe')],
  [InlineKeyboardButton('• تفاصيل المخالفة', callback_data=f'v_{vid}_detail')]
 ])

def kb_limits_main(cid):
 return InlineKeyboardMarkup([[InlineKeyboardButton('• اغلاق •',callback_data='close')]])

def limits_text(cid):
 return 'الحدود'

def kb_auto_main(cid):
 return InlineKeyboardMarkup([[InlineKeyboardButton('• اغلاق •',callback_data='close')]])

def text_auto_main(cid):
 return 'التنزيل التلقائي'

def get_auto(cid):
 return {'enabled':True}

AUTO_DOWNLOAD={}
AWAMER_TEXT='قائمة الاوامر - سورد'

async def start(u,c):
 if u.effective_chat.type=='private':
  await u.message.reply_text('هلا عزيزي انا سورد - اقوى واسرع بوت حماية وتشغيل ميوزك', reply_markup=kb_groups())
 else:
  await u.message.reply_text('قائمة الاوامر - سورد\nاختر القسم', reply_markup=kb_groups())

async def cb(u,c):
 q=u.callback_query
 await q.answer()
 d=q.data
 cid=str(u.effective_chat.id)
 if d=='close':
  try: await q.message.delete()
  except: await q.edit_message_text('CLOSED BY : Liam')
  return
 if d=='manage':
  txt='''اوامر ادارة القروب:

• رفع مالك / تنزيل مالك
• رفع منشئ / تنزيل منشئ
• رفع مدير / تنزيل مدير
• رفع ادمن / تنزيل ادمن
• رفع مميز / تنزيل مميز
• رفع مشرف / تنزيل مشرف (بصلاحيات محددة مثل الصورة) ⭐
  ❌ تغيير معلومات المجموعة
  ✅ حذف الرسائل
  ✅ حظر المستخدمين
  ✅ اضافة اعضاء
  ✅ تثبيت الرسائل
  ✅ ادارة القصص
  ✅ ادارة المحادثات المرئية
  ❌ البقاء متخفيا
  ✅ اضافة مشرفين جدد
• رفع اقامة / الاقامة الرئيسية / تنزيل اقامة 👑
• تنزيل الكل / تنزيل تلقائي ⬇️
• الاقامات / عرض الاقامات
• رتبتي / رتبته (بالرد)
• المتفاعلين 📊
• المالك / المطور - نفس السكرين
• قفل البوتات / فتح البوتات 🤖
• قفل التعديل / فتح التعديل ✏️
• قفل الاباحي / فتح الاباحي (بس اللي فيه كلمة اباحية)'''
  await q.edit_message_text(txt, reply_markup=kb_groups())
  return
 if d=='fun':
  await q.edit_message_text('التسلية والخدمية:\n\nكتم / الغاء كتم\nحظر / الغاء الحظر\nتقيد / طرد\nالالعاب / حظ / كت تويت / اذكار', reply_markup=kb_groups())
  return
 if d=='dev':
  await q.edit_message_text('اوامر Dev:\n\nتفعيل / تعطيل البوت\nتفعيل الوضع الخاص / تعطيل الوضع الخاص\nقفل / فتح + اسم القفل\nالاعدادات', reply_markup=kb_groups())
  return
 if d=='sets':
  out='الاعدادات:\n'
  cur=LOCKS.get(cid,{})
  for k,v in cur.items():
   out+=f'{k}: {"🔒" if v else "🔓"}\n'
  out+=f"\nحالة البوت: {'مفعل ✅' if is_enabled(cid) else 'معطل ❌'}"
  await q.edit_message_text(out, reply_markup=kb_groups())
  return
 if d.startswith('lock_'):
  name=d.replace('lock_','')
  cur=LOCKS.get(cid,{}).get(name,False)
  set_lock(cid,name,not cur)
  await q.edit_message_text(f'تم {"قفل" if not cur else "فتح"} {name}', reply_markup=kb_lock_page(cid,1))
  return

async def txt(u,c):
 m=u.message
 if not m: return
 cid=m.chat.id
 cid_s=str(cid)
 t=(m.text or '').strip()
 low=t.lower()
 uid=m.from_user.id
 uid_s=str(uid)

 # فلتر اباحي نصي
 bad_words=['اباحي','سكس','porn','xxx','sex','نيك','كس','زب','طيز','مص','قحبه','قحبة','xnxx','pornhub','xvideos','شرموط','قحاب','كسمك']
 low_check=low
 found=None
 for w in bad_words:
  if w in low_check:
   found=w
   break
 if found:
  if is_locked(cid_s,'الاباحي') or is_locked(cid_s,'الاباحه'):
   try: await m.delete()
   except: pass
   WARNINGS.setdefault(cid_s,{})
   WARNINGS[cid_s][uid_s]=WARNINGS[cid_s].get(uid_s,0)+1
   sv('warnings.json',WARNINGS)
   warns=WARNINGS[cid_s][uid_s]
   vid=str(int(time.time()*1000))[-6:]
   VIOLATIONS[vid]={'user_id':uid_s,'text':t[:200],'word':found,'chat':cid_s,'time':time.time()}
   sv('violations.json',VIOLATIONS)
   conf=random.randint(95,99)
   text=f"• تم رصد محتوى مخالف وحذفه\n• العضو ↤ {uid_s}\n• نسبة التأكد ↤ %{conf}\n• الإنذارات ↤ ({warns}/3)\n• ينتهي الإنذار خلال ↤ 06:00:00"
   try: await c.bot.send_message(chat_id=m.chat.id, text=text, reply_markup=kb_violation(vid))
   except: pass
   return

 TOP.setdefault(cid_s,{})
 TOP[cid_s][uid_s]=TOP[cid_s].get(uid_s,0)+1
 sv('top.json',TOP)

 if not is_enabled(cid_s):
  if t in ['تفعيل','تفعيل البوت','فعل البوت','تفعيل البوتات']:
   ENABLE[cid_s]={'disabled':False}
   sv('enable.json',ENABLE)
   await m.reply_text('تم تفعيل البوت ✅')
   return
  else: return

 if t in ['تعطيل','تعطيل البوت','عطل البوت','تعطيل البوتات']:
  ENABLE[cid_s]={'disabled':True}
  sv('enable.json',ENABLE)
  await m.reply_text('تم تعطيل البوت ❌\nارسل تفعيل لتشغيله')
  return
 if t in ['تفعيل','تفعيل البوت','فعل البوت','تفعيل البوتات']:
  ENABLE[cid_s]={'disabled':False}
  sv('enable.json',ENABLE)
  await m.reply_text('تم تفعيل البوت ✅')
  return

 if t in ['تفعيل الوضع الخاص','تفعيل الخاص']:
  PRIVATE_MODE[cid_s]=True
  sv('private_mode.json',PRIVATE_MODE)
  await m.reply_text('✅ تم تفعيل الوضع الخاص')
  return
 if t in ['تعطيل الوضع الخاص','تعطيل الخاص']:
  PRIVATE_MODE[cid_s]=False
  sv('private_mode.json',PRIVATE_MODE)
  await m.reply_text('❌ تم تعطيل الوضع الخاص')
  return

 if t in ['الاوامر','اوامر','قائمة الاوامر','سورد']:
  await m.reply_text(AWAMER_TEXT, reply_markup=kb_groups())
  return

 if t in ['الرتب','الرتبي']:
  await m.reply_text('الرتب المتاحة :\nDev\nMY\nM\nمالك\nمنشئ\nمدير\nادمن\nمميز\nالاقامة الرئيسية 👑\nمشرف ⭐')
  return

 # ========= المطور - نفس السكرين =========
 if t in ['المطور','SORD','Liam','ليام','المطورين','مطور']:
  try:
   owner_user = await c.get_users('afiwd')
   owner_id = owner_user.id
   owner_name = owner_user.first_name
   username = f"@{owner_user.username}" if owner_user.username else str(owner_id)
   bio_link = f"https://t.me/{owner_user.username}" if owner_user.username else f"tg://user?id={owner_id}"
   try:
    chat = await c.get_chat(cid)
    group_name = chat.title or "- darkness"
   except:
    group_name = "- darkness"
   photo_id = None
   try:
    async for p in c.get_chat_photos(owner_id, limit=1):
     photo_id = p.file_id
     break
   except: pass
   caption = f"Owner Group ↦ {group_name}\n————————————\nUSE ↦ {username}\nBio ↦ {bio_link}\n————————————"
   kb = InlineKeyboardMarkup([[InlineKeyboardButton(f"{owner_name}", url=f"tg://user?id={owner_id}")],[InlineKeyboardButton("• اغلاق •",callback_data="close")]])
   if photo_id:
    await m.reply_photo(photo_id, caption=caption, reply_markup=kb)
   else:
    await m.reply_text(caption, reply_markup=kb)
  except:
   await m.reply_text(f"Owner Group ↦ - darkness\n————————————\nUSE ↦ @afiwd\nBio ↦ https://t.me/afiwd\n————————————")
  return

 if t in ['المالك','مالك','اونر','owner']:
  try:
   target_user = m.reply_to_message.from_user if m.reply_to_message and m.reply_to_message.from_user else m.from_user
   try:
    chat = await c.get_chat(cid)
    group_name = chat.title or "- darkness"
   except:
    group_name = "- darkness"
   username = f"@{target_user.username}" if target_user.username else target_user.first_name
   bio = f"https://t.me/{target_user.username}" if target_user.username else f"tg://user?id={target_user.id}"
   photo_id = None
   try:
    async for p in c.get_chat_photos(target_user.id, limit=1):
     photo_id = p.file_id
     break
   except: pass
   caption = f"Owner Group ↦ {group_name}\n————————————\nUSE ↦ {username}\nBio ↦ {bio}\n————————————"
   kb = InlineKeyboardMarkup([[InlineKeyboardButton(f"{target_user.first_name}", url=f"tg://user?id={target_user.id}")]])
   if photo_id:
    await m.reply_photo(photo_id, caption=caption, reply_markup=kb)
   else:
    await m.reply_text(caption, reply_markup=kb)
  except:
   await m.reply_text("Owner Group ↦ - darkness\n————————————\nUSE ↦ 27\nBio ↦ https://t.me/iu56v\n————————————")
  return

 # ========= رفع مشرف - بصلاحيات محددة مثل الصورة =========
 if t.startswith('رفع مشرف') or t=='رفع مشرف':
  target=None
  if m.reply_to_message and m.reply_to_message.from_user:
   target=m.reply_to_message.from_user
  else:
   mm=re.search(r'(\d{5,20})', t)
   if mm:
    try: target=await c.get_users(int(mm.group(1)))
    except: pass
  if not target:
   await m.reply_text('⌯ رد على الشخص اللي تبي ترفعه مشرف\n⌯ او اكتب: رفع مشرف بالرد')
   return
  try:
   await c.bot.promote_chat_member(
    chat_id=cid,
    user_id=target.id,
    can_change_info=False,
    can_delete_messages=True,
    can_restrict_members=True,
    can_invite_users=True,
    can_pin_messages=True,
    can_promote_members=True,
    is_anonymous=False,
    can_manage_video_chats=True,
    can_manage_chat=True,
   )
   await m.reply_text(
    f'⌯ المستخدم {target.first_name}\n'
    f'⌯ تم رفعه مشرف بالصلاحيات المحددة ⭐\n\n'
    f'❌ تغيير معلومات المجموعة\n'
    f'✅ حذف الرسائل\n'
    f'✅ حظر المستخدمين\n'
    f'✅ اضافة أعضاء\n'
    f'✅ تثبيت الرسائل\n'
    f'✅ إدارة القصص\n'
    f'✅ إدارة المحادثات المرئية\n'
    f'❌ البقاء متخفياً\n'
    f'✅ إضافة مشرفين جدد'
   )
  except Exception as e:
   await m.reply_text(f'ما قدرت ارفعه مشرف - ارفعني مشرف مع رفع المشرفين\n{e}')
  return

 if t.startswith('تنزيل مشرف') or t=='تنزيل مشرف':
  target=None
  if m.reply_to_message and m.reply_to_message.from_user:
   target=m.reply_to_message.from_user
  if not target:
   await m.reply_text('رد على الشخص اللي تبي تنزله من الاشراف')
   return
  try:
   await c.bot.promote_chat_member(cid, target.id,
    can_change_info=False, can_delete_messages=False, can_invite_users=False,
    can_restrict_members=False, can_pin_messages=False, can_promote_members=False, is_anonymous=False)
   await m.reply_text(f'⌯ تم تنزيل {target.first_name} من الاشراف ⬇️')
  except Exception as e:
   await m.reply_text(f'ما قدرت انزله\n{e}')
  return

 # ========= الاقامة الرئيسية =========
 if t.startswith('رفع اقامة') or t in ['رفع اقامة','رفع الاقامة','رفع الاقامة الرئيسية','رفع الاقامه']:
  target=None
  if m.reply_to_message and m.reply_to_message.from_user:
   target=m.reply_to_message.from_user
  if not target:
   await m.reply_text('⌯ رد على الشخص اللي تبي ترفعه اقامة رئيسية')
   return
  r=get_r_new(cid_s)
  if target.id not in r['eqama']:
   r['eqama'].append(target.id)
   sv('ranks_new.json',RANKS_NEW)
  await m.reply_text(f'⌯ المستخدم {target.first_name}\n⌯ تم رفعه الاقامة الرئيسية 👑')
  return

 if t.startswith('تنزيل اقامة') or t in ['تنزيل اقامة','تنزيل الاقامة']:
  target=None
  if m.reply_to_message and m.reply_to_message.from_user:
   target=m.reply_to_message.from_user
  if not target:
   await m.reply_text('رد على الشخص اللي تبي تنزله من الاقامة')
   return
  r=get_r_new(cid_s)
  if target.id in r['eqama']:
   r['eqama'].remove(target.id)
   sv('ranks_new.json',RANKS_NEW)
   await m.reply_text(f'⌯ تم تنزيل {target.first_name} من الاقامة الرئيسية')
  else:
   await m.reply_text(f'⌯ {target.first_name} مو اقامة رئيسية')
  return

 if t in ['الاقامات','الاقامة الرئيسية','عرض الاقامات']:
  r=get_r_new(cid_s)
  lst=r['eqama']
  if not lst:
   await m.reply_text('⌯ لا يوجد اقامات رئيسية حالياً')
   return
  txt='👑 قائمة الاقامات الرئيسية:\n\n'
  for i,uid in enumerate(lst,1):
   try:
    uo=await c.get_users(uid)
    name=uo.first_name
   except:
    name=str(uid)
   txt+=f'{i}. {name} - {uid}\n'
  await m.reply_text(txt)
  return

 if t in ['تنزيل الكل','تنزيل تلقائي','تنزيل كل الرتب']:
  if not m.reply_to_message or not m.reply_to_message.from_user:
   await m.reply_text('⌯ رد على الشخص اللي تبي تنزل كل رتبة')
   return
  target=m.reply_to_message.from_user
  if cid_s in RANKS and str(target.id) in RANKS[cid_s]:
   del RANKS[cid_s][str(target.id)]
   sv('ranks.json',RANKS)
  r=get_r_new(cid_s)
  if target.id in r['eqama']:
   r['eqama'].remove(target.id)
   sv('ranks_new.json',RANKS_NEW)
  try:
   await c.bot.promote_chat_member(cid, target.id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False, is_anonymous=False)
  except: pass
  await m.reply_text(f'⌯ تم تنزيل {target.first_name} من كل الرتب + تنزيل مشرف تلقائي ⬇️')
  return

 if t in ['قفل البوتات','قفل البوت']:
  set_lock(cid_s,'البوتات',True)
  set_lock(cid_s,'bot',True)
  await m.reply_text('✅ تم قفل البوتات\n• اي بوت يدخل بينطرد تلقائي 🤖🔒')
  return
 if t in ['فتح البوتات','فتح البوت']:
  set_lock(cid_s,'البوتات',False)
  set_lock(cid_s,'bot',False)
  await m.reply_text('❌ تم فتح البوتات')
  return

 if t in ['قفل التعديل','قفل التعديل العادي']:
  set_lock(cid_s,'التعديل',True)
  set_lock(cid_s,'التعديل العادي',True)
  await m.reply_text('✅ تم قفل التعديل\n• اي واحد يعدل رسالته بتنمسح')
  return
 if t in ['فتح التعديل','فتح التعديل العادي']:
  set_lock(cid_s,'التعديل',False)
  set_lock(cid_s,'التعديل العادي',False)
  await m.reply_text('❌ تم فتح التعديل')
  return

 if t in ['قفل الاباحي','قفل الاباحه']:
  set_lock(cid_s,'الاباحي',True)
  await m.reply_text('✅ تم قفل الاباحي\n• الصور اللي فيها كلمة اباحية بس تنحذف')
  return
 if t in ['فتح الاباحي','فتح الاباحه']:
  set_lock(cid_s,'الاباحي',False)
  await m.reply_text('❌ تم فتح الاباحي')
  return

 if t in ['المتفاعلين','متفاعلين','توب متفاعلين','توب المتفاعلين']:
  top_data = TOP.get(cid_s, {})
  if not top_data:
   await m.reply_text('مافي تفاعل بعد')
   return
  sorted_users = sorted(top_data.items(), key=lambda x: x[1], reverse=True)[:15]
  text = '📊 المتفاعلين:\n\n'
  for i, (uid, count) in enumerate(sorted_users, 1):
   try:
    user = await c.get_users(int(uid))
    name = user.first_name
   except:
    name = f"ID {uid}"
   text += f'{i}. {name} - {count} رسالة\n'
  await m.reply_text(text)
  return

 if t in ['رتبتي','رتبته']:
  target = m.reply_to_message.from_user if m.reply_to_message else m.from_user
  tid = str(target.id)
  msgs = TOP.get(cid_s,{}).get(tid,0)
  rank_name = RANKS.get(cid_s,{}).get(tid, 'Member')
  if target.id in get_r_new(cid_s)['eqama']:
   rank_name='الاقامة الرئيسية 👑'
  await m.reply_text(f'🎖️ {rank_name} ← رتبتك =\n☂️ - {rank_name} - {msgs} رسالة')
  return

 if t in ['كتم','كتمه','اسكت','اسكته']:
  if not m.reply_to_message:
   await m.reply_text('رد على رسالة الشخص واكتب كتم')
   return
  target = m.reply_to_message.from_user
  tid = str(target.id)
  MUTED.setdefault(cid_s,{})
  MUTED[cid_s][tid]=True
  sv('muted.json',MUTED)
  await m.reply_text(f'تم كتم {target.first_name}')
  return

 if t in ['الغاء كتم','فك كتم']:
  if not m.reply_to_message:
   await m.reply_text('رد على رسالة الشخص واكتب الغاء كتم')
   return
  target = m.reply_to_message.from_user
  tid = str(target.id)
  MUTED.setdefault(cid_s,{})
  MUTED[cid_s].pop(tid,None)
  sv('muted.json',MUTED)
  await m.reply_text(f'تم الغاء كتم {target.first_name}')
  return

 if t.startswith('قفل') and len(t)>3:
  name=t.replace('قفل','').strip()
  if name in ['البوتات','البوت','الاباحي','التعديل','التعديل العادي','الرتب','امر']:
   return
  LOCKS.setdefault(cid_s,{})
  LOCKS[cid_s][name]=True
  sv('locks.json',LOCKS)
  await m.reply_text(f'تم قفل {name}')
  return

 if t.startswith('فتح') and len(t)>3:
  name=t.replace('فتح','').strip()
  if name in ['البوتات','البوت','الاباحي','التعديل','التعديل العادي']:
   return
  LOCKS.setdefault(cid_s,{})
  LOCKS[cid_s][name]=False
  sv('locks.json',LOCKS)
  await m.reply_text(f'تم فتح {name}')
  return

 if t in GAMES_DATA or t in ['حظ','كت تويت','اذكار']:
  if t=='حظ':
   await m.reply_text(f"حظك اليوم {random.randint(1,100)}% 🎲")
  elif t=='كت تويت':
   await m.reply_text(random.choice(['الحياة حلوة','لا تنتظر احد','خلك قوي']))
  elif t=='اذكار':
   await m.reply_text(random.choice(['سبحان الله','الحمدلله','لا اله الا الله']))
  else:
   await m.reply_text(get_game_text(t))
  return

 if t=='الالعاب':
  await m.reply_text('🎮 مركز الالعاب', reply_markup=kb_games())
  return

 if t=='الاعدادات':
  out='الاعدادات:\n'
  cur=LOCKS.get(cid_s,{})
  for k,v in cur.items():
   out+=f'{k}: {"🔒" if v else "🔓"}\n'
  out+=f"\nحالة البوت: {'مفعل ✅' if is_enabled(cid_s) else 'معطل ❌'}"
  await m.reply_text(out, reply_markup=kb_groups())
  return

async def media_handler(u,c):
 m = u.message
 if not m: return
 cid_s = str(m.chat.id)
 if not is_enabled(cid_s): return
 if LOCKS.get(cid_s,{}).get('الاباحي',False):
  cap = (m.caption or '').lower()
  bad_words = ['اباحي','سكس','porn','xxx','sex','نيك','كس','زب','طيز','مص','قحبه','قحبة','xnxx','pornhub','xvideos']
  found = None
  for w in bad_words:
   if w in cap:
    found = w
    break
  if not found: return
  try: await m.delete()
  except: pass

async def edited(u,c):
 if not u.edited_message: return
 m=u.edited_message
 cid_s=str(m.chat.id)
 if not is_enabled(cid_s): return
 locked = LOCKS.get(cid_s,{}).get('التعديل',False) or LOCKS.get(cid_s,{}).get('التعديل العادي',False)
 if locked:
  try: await m.delete()
  except: pass
  try: await c.bot.send_message(chat_id=m.chat.id, text=f"{m.from_user.first_name} بتعدل بلعن امك")
  except: pass

async def new_m(u,c):
 msg=u.message
 cid_s=str(msg.chat.id)
 if not is_enabled(cid_s): return
 if LOCKS.get(cid_s,{}).get('البوتات',False) or LOCKS.get(cid_s,{}).get('bot',False):
  for user in msg.new_chat_members:
   if user.is_bot and user.id != c.bot.id:
    try:
     await c.bot.ban_chat_member(cid_s, user.id)
     await msg.reply_text(f'تم طرد البوت {user.first_name} - البوتات مقفولة 🤖🔒')
    except: pass

if __name__=='__main__':
 if not TOKEN:
  raise RuntimeError('TOKEN')
 import asyncio
 threading.Thread(target=run,daemon=True).start()
 try:
  loop=asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
 except: pass
 app=ApplicationBuilder().token(TOKEN).build()
 app.add_handler(CommandHandler('start',start))
 app.add_handler(CallbackQueryHandler(cb))
 app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_m))
 app.add_handler(MessageHandler(filters.TEXT & ~filters.UpdateType.EDITED_MESSAGE, txt))
 app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO) & ~filters.UpdateType.EDITED_MESSAGE, media_handler))
 app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, edited))
 print('SORD BOT FINAL 4000 WITH PERMS - رفع مشرف بصلاحيات محددة مثل الصورة')
 app.run_polling(allowed_updates=["message","edited_message","callback_query","chat_member"], drop_pending_updates=True)
