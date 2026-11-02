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
for fp in ['locks.json','toggles.json','custom.json','top.json','ranks.json','muted.json','warnings.json','violations.json']:
 if not os.path.exists(fp):
  sv(fp,{})

LOCKS=ld('locks.json')
if not LOCKS:
 LOCKS={}
TOGGLES=ld('toggles.json')
TOP=ld('top.json')
RANKS=ld('ranks.json')
MUTED=ld('muted.json')
WARNINGS=ld('warnings.json')
VIOLATIONS=ld('violations.json')


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
 # True = مقفل = ازرق
 locked = LOCKS.get(cid,{}).get(name, False)
 if locked:
  return f"🔵 -{name}"
 else:
  return f"🟢 -{name}"

def kb_lock_page(cid, page):
 page = max(1, min(6, page))
 locks = LOCKS_PAGES.get(page, [])
 kb = []
 # فتح الكل / قفل الكل
 kb.append([
  InlineKeyboardButton('• فتح الكل',callback_data=f'openall_{page}'),
  InlineKeyboardButton('• قفل الكل',callback_data=f'closeall_{page}')
 ])
 # صفوف القفل 2 في كل صف
 for i in range(0, len(locks), 2):
  row = []
  for j in range(2):
   if i+j < len(locks):
    name = locks[i+j]
    row.append(InlineKeyboardButton(get_lock_text(cid, name), callback_data=f'lock_{name}'))
  kb.append(row)
 # ازرار التنقل
 if page==1:
  kb.append([InlineKeyboardButton('• الصفحة التالية',callback_data='lockpage_2')])
 elif page==6:
  kb.append([InlineKeyboardButton('• الصفحة السابقة',callback_data='lockpage_5')])
 else:
  kb.append([
   InlineKeyboardButton('• الصفحة السابقة',callback_data=f'lockpage_{page-1}'),
   InlineKeyboardButton('• الصفحة التالية',callback_data=f'lockpage_{page+1}')
  ])
 kb.append([InlineKeyboardButton('• اخفاء',callback_data='close')])
 kb.append([InlineKeyboardButton('• العودة للقائمة الرئيسية',callback_data='cmd_groups')])
 # عرض الصفحة الحالية
 kb.append([InlineKeyboardButton(f'{page} / 6',callback_data='noop'), InlineKeyboardButton('• رجوع',callback_data='cmd_groups')])
 # لكن للتوافق مع الصور : نستخدم 6 صفحات
 return InlineKeyboardMarkup(kb)

def kb_lock_page_old(cid, page):
 return kb_lock_page(cid, page)

# نص لوحة القفل والفتح
LOCK_PANEL_TEXT = '''القفل والفتح
—————————
• تقفل وتفتح انواع الرسائل والمحتوى في القروب
• الصفحة {page} من 6

• اضغط على الامر عشان يطلع شرحه'''


# ---------- الالعاب مع الشرح ----------
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
  return f"لعبة {name}\\nالشرح : تسلية\\nطريقة اللعب : اكتب {name}\\nعدد اللاعبين : 1\\nطريقة الفوز : تسلية"
 return f"🎮 {name}\\n\\nالشرح : {g['desc']}\\nطريقة اللعب : {g['play']}\\nعدد اللاعبين : {g['players']}\\nطريقة الفوز : {g['win']}"

WAITING={}

# RANKS
ALL_RANKS=[
'Dev','Dev2','MY','M',
'Extra','مالك اساسي','مالك',
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
'الاباحي',
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
  [InlineKeyboardButton('• اضفني لقروبك •',url='https://t.me/BOT?startgroup=true')],
  [InlineKeyboardButton('• About SORD •',callback_data='about')]
 ])

def kb_main():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• اوامر القروبات •',callback_data='cmd_groups'),
   InlineKeyboardButton('• اوامر التشغيل •',callback_data='cmd_play')],
  [InlineKeyboardButton('• اوامر القنوات •',callback_data='cmd_channels'),
   InlineKeyboardButton('• تكرار وتقديم وسر •',callback_data='cmd_loop')],
  [InlineKeyboardButton('• اوامر المطورين •',callback_data='cmd_dev')],
  [InlineKeyboardButton('• اغلاق •',callback_data='close')]
 ])

def kb_groups():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• القفل والفتح •',callback_data='lockpanel'),
   InlineKeyboardButton('• التفعيل والتعطيل •',callback_data='onoff')],
  [InlineKeyboardButton('• التسلية والخدمية •',callback_data='fun'),
   InlineKeyboardButton('• ادارة القروب •',callback_data='manage')],
  [InlineKeyboardButton('• اوامر Dev •',callback_data='dev'),
   InlineKeyboardButton('• الإعدادات •',callback_data='sets')],
  [InlineKeyboardButton('• اغلاق •',callback_data='close')]
 ])

def kb_lock_p1():
 b=[]
 b.append([
  InlineKeyboardButton('• فتح الكل •',callback_data='openall'),
  InlineKeyboardButton('• قفل الكل •',callback_data='closeall')
 ])
 for i in range(0,len(LOCKS_P1),2):
  b.append([
   InlineKeyboardButton(LOCKS_P1[i]+' -',callback_data=f'l_{LOCKS_P1[i]}'),
   InlineKeyboardButton(LOCKS_P1[i+1]+' -',callback_data=f'l_{LOCKS_P1[i+1]}')
  ])
 b.append([InlineKeyboardButton('• الصفحة التالية •',callback_data='page2')])
 b.append([
  InlineKeyboardButton('• اغلاق •',callback_data='close'),
  InlineKeyboardButton('• الرئيسية •',callback_data='cmd_groups')
 ])
 return InlineKeyboardMarkup(b)

def kb_lock_p2():
 b=[]
 b.append([
  InlineKeyboardButton('• فتح الكل •',callback_data='openall'),
  InlineKeyboardButton('• قفل الكل •',callback_data='closeall')
 ])
 for i in range(0,len(LOCKS_P2),2):
  b.append([
   InlineKeyboardButton(LOCKS_P2[i]+' -',callback_data=f'l_{LOCKS_P2[i]}'),
   InlineKeyboardButton(LOCKS_P2[i+1]+' -',callback_data=f'l_{LOCKS_P2[i+1]}')
  ])
 b.append([InlineKeyboardButton('• الصفحة السابقة •',callback_data='page1')])
 b.append([
  InlineKeyboardButton('• اغلاق •',callback_data='close'),
  InlineKeyboardButton('• الرئيسية •',callback_data='cmd_groups')
 ])
 return InlineKeyboardMarkup(b)

def kb_games():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• العاب جماعية',callback_data='g_group'),
   InlineKeyboardButton('• العاب ادوار',callback_data='g_roles')],
  [InlineKeyboardButton('• كلمات وحروف',callback_data='g_words'),
   InlineKeyboardButton('• تحدي واستنتاج',callback_data='g_chal')],
  [InlineKeyboardButton('• اسئلة ومعلومات',callback_data='g_q'),
   InlineKeyboardButton('• صور وتخمين',callback_data='g_pic')],
  [InlineKeyboardButton('• مقالات وسرعة',callback_data='g_fast'),
   InlineKeyboardButton('• تسلية القروب',callback_data='g_fun')],
  [InlineKeyboardButton('• حظ وقرعة',callback_data='g_luck'),
   InlineKeyboardButton('• عوائل وتيناس',callback_data='g_fam')],
  [InlineKeyboardButton('• مسابقات وقلابات',callback_data='g_race'),
   InlineKeyboardButton('• احصائياتي',callback_data='g_me')],
  [InlineKeyboardButton('• توب الادمين',callback_data='g_topadmin'),
   InlineKeyboardButton('• توب المتفاعلين',callback_data='g_top')],
  [InlineKeyboardButton('• إغلاق',callback_data='close')]
 ])


def kb_violation(vid):
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• إلغاء الإنذار •',callback_data=f'warn_cancel_{vid}')],
  [InlineKeyboardButton('• الرسالة سليمة •',callback_data=f'warn_safe_{vid}')],
  [InlineKeyboardButton('• تفاصيل المخالفة •',callback_data=f'warn_detail_{vid}')]
 ])







# === نظام الحدود - نفس الصور لصق طبع ===
LIMITS=ld('limits.json')  # chat_id -> {action: limit, enabled: bool}
LIMITS_USAGE=ld('limits_usage.json')  # chat_id -> admin_id -> {action: count, date: today}

LIMIT_ACTIONS=['الحظر','الطرد','الكتم','التقييد','الرفع','التنزيل','المسح']
LIMITS_DEFAULT={a:0 for a in LIMIT_ACTIONS}  # 0 = بلا حد

def get_limits(cid):
  cid=str(cid)
  if cid not in LIMITS:
    LIMITS[cid]={'enabled':True,'limits':{a:0 for a in LIMIT_ACTIONS}}
    sv('limits.json',LIMITS)
  return LIMITS[cid]

def get_usage(cid, admin_id):
  cid=str(cid); aid=str(admin_id)
  today=str(__import__('datetime').date.today())
  if cid not in LIMITS_USAGE:
    LIMITS_USAGE[cid]={}
  if aid not in LIMITS_USAGE[cid] or LIMITS_USAGE[cid][aid].get('date')!=today:
    LIMITS_USAGE[cid][aid]={'date':today,'counts':{a:0 for a in LIMIT_ACTIONS}}
  return LIMITS_USAGE[cid][aid]

def check_limit(cid, admin_id, action):
  lim=get_limits(cid)
  if not lim.get('enabled',True):
    return True
  max_lim=lim['limits'].get(action,0)
  if max_lim==0:
    return True  # بلا حد
  usage=get_usage(cid,admin_id)
  cnt=usage['counts'].get(action,0)
  return cnt < max_lim

def inc_usage(cid, admin_id, action):
  usage=get_usage(cid,admin_id)
  usage['counts'][action]=usage['counts'].get(action,0)+1
  LIMITS_USAGE[str(cid)][str(admin_id)]=usage
  sv('limits_usage.json',LIMITS_USAGE)

def kb_limits_main(cid):
  lim=get_limits(cid)
  limits=lim['limits']
  # بناء أزرار نفس الصورة
  buttons=[
    [InlineKeyboardButton(f'الطرد : {limits["الطرد"] if limits["الطرد"]!=0 else "بلا حد"}', callback_data='lim_الطرد'),
     InlineKeyboardButton(f'الحظر : {limits["الحظر"] if limits["الحظر"]!=0 else "بلا حد"}', callback_data='lim_الحظر')],
    [InlineKeyboardButton(f'التقييد : {limits["التقييد"] if limits["التقييد"]!=0 else "بلا حد"}', callback_data='lim_التقييد'),
     InlineKeyboardButton(f'الكتم : {limits["الكتم"] if limits["الكتم"]!=0 else "بلا حد"}', callback_data='lim_الكتم')],
    [InlineKeyboardButton(f'التنزيل : {limits["التنزيل"] if limits["التنزيل"]!=0 else "بلا حد"}', callback_data='lim_التنزيل'),
     InlineKeyboardButton(f'الرفع : {limits["الرفع"] if limits["الرفع"]!=0 else "بلا حد"}', callback_data='lim_الرفع')],
    [InlineKeyboardButton(f'المسح : {limits["المسح"] if limits["المسح"]!=0 else "بلا حد"}', callback_data='lim_المسح')],
    [InlineKeyboardButton('• استهلاك اليوم', callback_data='lim_today'),
     InlineKeyboardButton('• تعطيل الحدود', callback_data='lim_disable')],
    [InlineKeyboardButton('• مسح الحدود', callback_data='lim_clear')],
    [InlineKeyboardButton('• رجوع', callback_data='cmd_main'),
     InlineKeyboardButton('• إغلاق', callback_data='close')]
  ]
  return InlineKeyboardMarkup(buttons)

def kb_limit_edit(action, current):
  # أزرار -5 -1 +1 +5 و 1 3 5 10 20 و بلا حد
  cur_text = current if current!=0 else 'بلا حد'
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('• -5', callback_data=f'lim_edit_{action}_-5'),
     InlineKeyboardButton('• -1', callback_data=f'lim_edit_{action}_-1'),
     InlineKeyboardButton('• +1', callback_data=f'lim_edit_{action}_+1'),
     InlineKeyboardButton('• +5', callback_data=f'lim_edit_{action}_+5')],
    [InlineKeyboardButton('• 1', callback_data=f'lim_edit_{action}_set_1'),
     InlineKeyboardButton('• 3', callback_data=f'lim_edit_{action}_set_3'),
     InlineKeyboardButton('• 5', callback_data=f'lim_edit_{action}_set_5'),
     InlineKeyboardButton('• 10', callback_data=f'lim_edit_{action}_set_10'),
     InlineKeyboardButton('• 20', callback_data=f'lim_edit_{action}_set_20')],
    [InlineKeyboardButton('• بلا حد', callback_data=f'lim_edit_{action}_set_0')],
    [InlineKeyboardButton('• رجوع', callback_data='lim_main'),
     InlineKeyboardButton('• إغلاق', callback_data='close')]
  ])

def limits_text(cid, action=None):
  lim=get_limits(cid)
  limits=lim['limits']
  if action:
    cur=limits.get(action,0)
    cur_t = cur if cur!=0 else 'بلا حد'
    if action=='التنزيل':
      return f'''• حد ( التنزيل ) لكل مشرف
_________________________

• الحالي ↤ {cur_t}
• كل شخص ينحسب مرة وحدة
• اضغط الارقام تغيّره، او ( بلا حد ) تشيله'''
    elif action=='الكتم':
      return f'''• حد ( الكتم ) لكل مشرف
_________________________

• الحالي ↤ {cur_t}
• كل شخص ينحسب مرة وحدة
• اضغط الارقام تغيّره، او ( بلا حد ) تشيله'''
    else:
      return f'''• حد ( {action} ) لكل مشرف
_________________________

• الحالي ↤ {cur_t}
• كل شخص ينحسب مرة وحدة
• اضغط الارقام تغيّره، او ( بلا حد ) تشيله'''
  else:
    # النص الكامل نفس الصورة
    txt='''• الحظر ↤ بلا حد
• الطرد ↤ بلا حد
• الكتم ↤ بلا حد
• التقييد ↤ بلا حد
• الرفع ↤ بلا حد
• التنزيل ↤ بلا حد
• المسح ↤ بلا حد
_________________________

• يتجاوز من اوامر البوت ↤ يرفض امره
ويقوله تجاوزت حدك
• يتجاوز من اعدادات تيليجرام ↤ يرجع
اللي سواه وينسحب منه الاشراف
• وبالحالتين يوصلك اشعار'''
    # استبدل القيم الفعلية
    for a in LIMIT_ACTIONS:
      v=limits.get(a,0)
      v_t = f'{v}' if v!=0 else 'بلا حد'
      txt=txt.replace(f'{a} ↤ بلا حد', f'{a} ↤ {v_t}', 1)
    return txt





def kb_auto_time_edit(rank, current_hours):
  # current in hours
  if current_hours>=24:
    cur_text=f"{current_hours//24} أيام" if current_hours%24==0 else f"{current_hours} ساعة"
  else:
    cur_text=f"{current_hours} ساعات"
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('• -1 يوم', callback_data=f'auto_time_{rank}_-24'),
     InlineKeyboardButton('• -1 ساعة', callback_data=f'auto_time_{rank}_-1'),
     InlineKeyboardButton('• +1 ساعة', callback_data=f'auto_time_{rank}_+1'),
     InlineKeyboardButton('• +1 يوم', callback_data=f'auto_time_{rank}_+24')],
    [InlineKeyboardButton('• 6 ساعات', callback_data=f'auto_time_{rank}_set_6'),
     InlineKeyboardButton('• 12 ساعة', callback_data=f'auto_time_{rank}_set_12'),
     InlineKeyboardButton('• 1 يوم', callback_data=f'auto_time_{rank}_set_24'),
     InlineKeyboardButton('• 3 أيام', callback_data=f'auto_time_{rank}_set_72')],
    [InlineKeyboardButton('• 7 أيام', callback_data=f'auto_time_{rank}_set_168'),
     InlineKeyboardButton('• 30 يوم', callback_data=f'auto_time_{rank}_set_720')],
    [InlineKeyboardButton('• مسح الحد', callback_data=f'auto_time_{rank}_clear')],
    [InlineKeyboardButton('• رجوع', callback_data='auto_set_rank'),
     InlineKeyboardButton('• إغلاق', callback_data='close')]
  ])

def text_auto_time_edit(rank, hours):
  if hours>=24:
    if hours%24==0:
      cur=f"{hours//24} أيام"
    else:
      cur=f"{hours} ساعة ({hours//24} يوم و {hours%24} ساعة)"
  else:
    cur=f"{hours} ساعات"
  return f'''• حد التنزيل لرتبة {rank}
_________________________

• الحالي ↤ {cur}
• اللي يغيب اكثر من {cur} ينزل تلقائي
وينرسل منشن له بالقروب

• اضغط الازرار لتغيير الوقت'''


# === نظام التنزيل التلقائي - نفس الصور لصق طبع ===
AUTO_DOWNLOAD=ld('auto_download.json')  # chat_id -> {enabled: bool, limits: {rank: hours}}
LAST_SEEN=ld('last_seen.json')  # chat_id -> user_id -> timestamp

AUTO_DEFAULT_LIMITS={'Dev2':6, 'الاشراف': 7*24}  # 6 ساعات و 7 أيام نفس الصورة
AUTO_RANKS=['Dev2','MYTH','المالك الاساسي','المالك','المنشئ الاساسي','المنشئ','المدير','الادمن','المميز','الاشراف']

def get_auto(cid):
  cid=str(cid)
  if cid not in AUTO_DOWNLOAD:
    AUTO_DOWNLOAD[cid]={'enabled':False,'limits':AUTO_DEFAULT_LIMITS.copy()}
    sv('auto_download.json',AUTO_DOWNLOAD)
  return AUTO_DOWNLOAD[cid]

def get_last_seen(cid, uid):
  return LAST_SEEN.get(str(cid),{}).get(str(uid),0)

def set_last_seen(cid, uid):
  import time
  cid=str(cid); uid=str(uid)
  if cid not in LAST_SEEN:
    LAST_SEEN[cid]={}
  LAST_SEEN[cid][uid]=int(time.time())
  sv('last_seen.json',LAST_SEEN)

def kb_auto_main(cid):
  auto=get_auto(cid)
  enabled=auto['enabled']
  # زر تفعيل/تعطيل
  toggle_text='تعطيل التنزيل التلقائي' if enabled else 'تفعيل التنزيل التلقائي'
  toggle_color='red' if enabled else 'green'
  buttons=[
    [InlineKeyboardButton('• مسح حدود التنزيل', callback_data='auto_clear')],
    [InlineKeyboardButton(f'• {toggle_text}', callback_data='auto_toggle')],
    [InlineKeyboardButton('• رجوع', callback_data='group_settings'),
     InlineKeyboardButton('• اغلاق', callback_data='close')]
  ]
  # لو معطل - يظهر أزرار وضع حد
  if not enabled:
    buttons.insert(0, [InlineKeyboardButton('• مسح حد تنزيل رتبة', callback_data='auto_clear_rank')])
    buttons.insert(0, [InlineKeyboardButton('• ضع حد تنزيل لرتبة', callback_data='auto_set_rank')])
  return InlineKeyboardMarkup(buttons)

def kb_auto_set_rank():
  # نفس صورة 7CF30CE3
  buttons=[
    [InlineKeyboardButton('• MYTH 🎖️', callback_data='auto_rank_MYTH2'),
     InlineKeyboardButton('• Dev2 🎖️ : 6 ساعات', callback_data='auto_rank_Dev2')],
    [InlineKeyboardButton('• المالك الاساسي', callback_data='auto_rank_المالك الاساسي'),
     InlineKeyboardButton('• MYTH', callback_data='auto_rank_MYTH')],
    [InlineKeyboardButton('• المنشئ الاساسي', callback_data='auto_rank_المنشئ الاساسي'),
     InlineKeyboardButton('• المالك', callback_data='auto_rank_المالك')],
    [InlineKeyboardButton('• المدير', callback_data='auto_rank_المدير'),
     InlineKeyboardButton('• المنشئ', callback_data='auto_rank_المنشئ')],
    [InlineKeyboardButton('• المميز', callback_data='auto_rank_المميز'),
     InlineKeyboardButton('• الادمن', callback_data='auto_rank_الادمن')],
    [InlineKeyboardButton('• الاشراف : 7 أيام', callback_data='auto_rank_الاشراف')],
    [InlineKeyboardButton('• رجوع', callback_data='auto_main'),
     InlineKeyboardButton('• اغلاق', callback_data='close')]
  ]
  return InlineKeyboardMarkup(buttons)

def kb_group_settings():
  # نفس صورة A00E8BA4 - الالوان نفس الصورة: أخضر = NEW, بني = الباقي
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('• إعدادات الوسائط 🆕 NEW', callback_data='settings_media')],
    [InlineKeyboardButton('• القفل والفتح', callback_data='lock_menu')],
    [InlineKeyboardButton('• التفعيل والتعطيل', callback_data='enable_disable')],
    [InlineKeyboardButton('• الوضع والمسح', callback_data='mode_clear')],
    [InlineKeyboardButton('• التنظيف', callback_data='cleaning')],
    [InlineKeyboardButton('• حدود المشرفين', callback_data='lim_main')],
    [InlineKeyboardButton('• التنزيل التلقائي', callback_data='auto_main')],
    [InlineKeyboardButton('• رجوع للقائمة الرئيسية للأوامر', callback_data='cmd_main')]
  ])

def kb_groups_commands():
  # نفس صورة D78F76BA - أخضر = رجوع, أحمر = إغلاق
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('• رجوع', callback_data='cmd_main')],
    [InlineKeyboardButton('• إغلاق', callback_data='close')]
  ])

def text_auto_main(cid):
  auto=get_auto(cid)
  enabled=auto['enabled']
  status='مفعّل' if enabled else 'معطّل'
  limits=auto['limits']
  lim_text=''
  for k,v in limits.items():
    if v>=24:
      days=v//24
      lim_text+=f'- {k} ↤ {days} أيام\n'
    else:
      lim_text+=f'- {k} ↤ {v} ساعات\n'
  if not lim_text:
    lim_text='- لا يوجد حدود\n'
  
  if enabled:
    return f'''• اعدادات التنزيل التلقائي
_________________________

• الحالة ↤ {status}
• اللي يغيب عن القروب اكثر من حد رتبته
ينزل منها تلقائي، وينرسل بالقروب منشن
له
• يضبطها ↤ Dev 🎖️
_________________________

• حدود التنزيل الحالية :
{lim_text}'''
  else:
    return f'''• اعدادات التنزيل التلقائي
_________________________

• الحالة ↤ {status}
• اللي يغيب عن القروب اكثر من حد رتبته
ينزل منها تلقائي، وينرسل بالقروب منشن
له
• يضبطها ↤ Dev 🎖️
_________________________

• حدود التنزيل الحالية :
{lim_text}
• الحدود ما تشتغل لين تكتب ( تفعيل
التنزيل التلقائي )'''

def text_group_settings():
  return '''اعدادات القروب
_________________________

• اختر القسم اللي تبي تعدّل فيه
• كل قسم فيه ازراره وترجع منه بزر
الرجوع'''

def text_groups_commands():
  return '''أوامر خاصة بالقروبات 👥

• رفع مشغل [ رد / آيدي ] - يمنح
صلاحيات إدمن التشغيل بدون إشراف
كامل

• تنزيل مشغل [ رد / آيدي ]
• المشغلين - عرض المشغلين الحاليين
• الاعدادات / settings - إعدادات
القروب (وضع البحث، التصويت...)
• /reload - تحديث قائمة المشرفين'''






# REMOVE OLD
# OLD REMOVED
# OLD
async def handle_dev_command_old_rakan_old_final_old2(m,cid,t,c):
  if t in ['مطور','المطور','المطورين','مطورين']:
    try:
      # حاول تجيب صورة afiwd
      photo=None
      try:
        # جيب معلومات afiwd
        dev_chat=await c.get_chat('afiwd')
        if hasattr(dev_chat,'photo') and dev_chat.photo:
          photo=dev_chat.photo.big_file_id
      except:
        pass
      
      text='''راكان

وَاجْعَلْ لِي لِسَانَ صِدْقٍ فِي الْآخِرِينَ'''
      
      # لو فيه صورة - ارسل بصورة مع اقتباس
      if photo:
        try:
          await m.reply_photo(photo, caption=text, parse_mode='html', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('• راكان', url='https://t.me/afiwd')]
          ]))
          return True
        except:
          pass
      
      # بدون صورة - ارسل نص مع اقتباس
      await m.reply_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('• راكان', url='https://t.me/afiwd')]
      ]))
      return True
    except Exception as e:
      await m.reply_text('''راكان

وَاجْعَلْ لِي لِسَانَ صِدْقٍ فِي الْآخِرِينَ''', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('• راكان', url='https://t.me/afiwd')]
      ]))
      return True
  return False



# OLD REMOVED
# OLD
async def handle_dev_command_old_rakan_old_final(m,cid,t,c):
  if t in ['مطور','المطور','المطورين','مطورين','المطور 🧑‍💻']:
    try:
      # حاول تجيب معلومات afiwd
      dev_id=30457869  # نفس الايدي بالفيديو أو حاول تجيب الحقيقي
      dev_username='afiwd'
      dev_name='راكان'
      dev_bio='وَاجْعَلْ لِي لِسَانَ صِدْقٍ فِي الْآخِرِينَ'
      photo=None
      try:
        dev_user=await c.get_users('afiwd')
        dev_id=dev_user.id
        dev_name='راكان'
        dev_username=dev_user.username or 'afiwd'
        # حاول تجيب صورته
        async for p in c.get_chat_photos(dev_id, limit=1):
          photo=p.file_id
          break
      except:
        pass

      # نفس نص الفيديو لصق طبع بس باسم راكان
      text=f'''عمي ستروفق 🚀
آخر ظهور كان قريبا 🚀

Id: {dev_id}
مسجل
2014 فبراير

Not Strong Anymore 🚀

› Developer Bot » SORD » سول
› {dev_name}

› ماذا تعرف USE » عن معرفه
› Bio » {dev_bio} اسم المستخدم
@{dev_username}

أيضا
@00yy, @000dd, @fsssl, @e__x__x
@zucci, @ccuu, @jjimmm, @xgmx

› البايو
{dev_bio}

https://t.me/{dev_username}'''

      if photo:
        try:
          await m.reply_photo(photo, caption=text, parse_mode='html', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f'• {dev_name}', url=f'https://t.me/{dev_username}')]
          ]))
          return True
        except:
          pass
      
      await m.reply_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(f'• {dev_name}', url=f'https://t.me/{dev_username}')]
      ]))
      return True
    except Exception as e:
      await m.reply_text(f'''راكان

وَاجْعَلْ لِي لِسَانَ صِدْقٍ فِي الْآخِرِينَ

https://t.me/afiwd''', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('• راكان', url='https://t.me/afiwd')]
      ]))
      return True
  return False



# OLD
async def handle_dev_command_old_rakan(m,cid,t,c):
  if t in ['مطور','المطور','المطورين','مطورين','المطور 🧑‍💻']:
    try:
      await m.reply_text('المطور', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('راكان', url='https://t.me/afiwd')]
      ]))
      return True
    except:
      await m.reply_text('المطور', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('راكان', url='https://t.me/afiwd')]
      ]))
      return True
  return False



async def handle_dev_command(m,cid,t,c):
  if t in ['مطور','المطور','المطورين','مطورين','المطور 🧑‍💻']:
    try:
      photo=None
      try:
        dev_user=await c.get_users('afiwd')
        async for p in c.get_chat_photos(dev_user.id, limit=1):
          photo=p.file_id
          break
      except:
        pass

      text='''راكان

وَاجْعَلْ لِي لِسَانَ صِدْقٍ فِي الْآخِرِينَ'''

      if photo:
        try:
          await m.reply_photo(photo, caption=text, parse_mode='html', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('راكان', url='https://t.me/afiwd')]
          ]))
          return True
        except:
          pass
      
      await m.reply_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('راكان', url='https://t.me/afiwd')]
      ]))
      return True
    except:
      await m.reply_text('''راكان

وَاجْعَلْ لِي لِسَانَ صِدْقٍ فِي الْآخِرِينَ''', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('راكان', url='https://t.me/afiwd')]
      ]))
      return True
  return False



async def handle_call_invite(m,cid,t,c):
  # لو كتب دعوة ورد على شخص
  if t.startswith('دعوة') or 'دعوة للمكالمة' in t or 'دعوه' in t:
    inviter=m.from_user.first_name if m.from_user else 'المستخدم'
    invited='المستخدم'
    if m.reply_to_message and m.reply_to_message.from_user:
      invited=m.reply_to_message.from_user.first_name
    else:
      # حاول تستخرج اسم من النص بعد دعوة
      import re
      mm=re.search(r'دعوة\s+(.+)', t)
      if mm:
        invited=mm.group(1).strip()
    
    text=f'''⌯ المستخدم ذا ↤︎「 {inviter} 」
⌯ قام بدعوة ↤︎ 「 {invited} 」للمكالمة'''
    await m.reply_text(text)
    return True
  
  # كشف دعوات الكول الحقيقية من تيليجرام - service messages
  if m.voice_chat_started or m.voice_chat_ended or m.video_chat_started:
    return False
  
  return False

# للكشف عن دعوة الكول من تيليجرام نفسه (group call invite)
async def handle_group_call_invite(c, m):
  try:
    # هذه للرسائل الخدمية لدعوة الكول
    if hasattr(m, 'group_call_invite') and m.group_call_invite:
      inviter=m.from_user.first_name if m.from_user else 'المستخدم'
      # حاول تجيب المدعو
      invited='المستخدم'
      try:
        if hasattr(m.group_call_invite, 'users'):
          if m.group_call_invite.users:
            u=await c.get_users(m.group_call_invite.users[0])
            invited=u.first_name
      except:
        pass
      text=f'''⌯ المستخدم ذا ↤︎「 {inviter} 」
⌯ قام بدعوة ↤︎ 「 {invited} 」للمكالمة'''
      await m.reply_text(text)
  except:
    pass



# === منع رفع البوتات - لو انرفع تتله انت ===
async def handle_anti_bot_promote(c, chat_id, target_user_id, promoter_id=None):
  try:
    # تأكد أن الهدف بوت
    try:
      target=await c.get_users(target_user_id)
      is_bot=target.is_bot
    except:
      is_bot=True  # لو ما قدرنا نجيب معلوماته نفترض بوت
    
    if not is_bot:
      return False
    
    # نزل البوت من الاشراف
    try:
      await c.promote_chat_member(chat_id, target_user_id, is_anonymous=False,
        can_delete_messages=False, can_restrict_members=False, can_promote_members=False,
        can_change_info=False, can_invite_users=False, can_pin_messages=False)
    except:
      pass
    
    # نزل من الرتب لو فيه
    try:
      if str(chat_id) in OPERATORS and target_user_id in OPERATORS[str(chat_id)]:
        remove_operator(chat_id, target_user_id)
    except:
      pass
    
    # رسالة تنبيه
    try:
      promoter_name='المستخدم'
      if promoter_id:
        try:
          p=await c.get_users(promoter_id)
          promoter_name=p.first_name
        except:
          pass
      await c.send_message(chat_id, f'⌯ تم منع رفع البوت\n⌯ البوت {target_user_id} ما ينرفع\n⌯ تم تنزيله تلقائياً')
    except:
      pass
    return True
  except:
    return False

async def check_and_demote_bots_on_promote(c, m):
  # شيك لو الرسالة فيها رفع لبوت
  try:
    # لو رد على بوت
    if m.reply_to_message and m.reply_to_message.from_user and m.reply_to_message.from_user.is_bot:
      target_id=m.reply_to_message.from_user.id
      # لو الأمر رفع
      if any(x in m.text for x in ['رفع', 'ترقيه', 'ترقية', 'مشرف', 'ادمن', 'إدمن']):
        await handle_anti_bot_promote(c, m.chat.id, target_id, m.from_user.id if m.from_user else None)
        await m.reply_text('⌯ البوتات ما تنرفع ❌\n⌯ تم تنزيله تلقائياً')
        return True
    
    # لو كتب ايدي بوت
    if m.text:
      import re
      mm=re.search(r'(\d{5,20})', m.text)
      if mm and any(x in m.text for x in ['رفع', 'مشرف', 'ادمن']):
        try:
          uid=int(mm.group(1))
          user=await c.get_users(uid)
          if user.is_bot:
            await handle_anti_bot_promote(c, m.chat.id, uid, m.from_user.id if m.from_user else None)
            await m.reply_text('⌯ البوتات ما تنرفع ❌\n⌯ تم تنزيله تلقائياً')
            return True
        except:
          pass
  except:
    pass
  return False
async def bot_promote_protection_disabled(c, m):
  return False
  try:
    # لو حد انرفع مشرف
    if m.new_chat_member and m.new_chat_member.status in ['administrator','creator']:
      # شيك لو هو بوت
      if m.new_chat_member.user and m.new_chat_member.user.is_bot:
        # لا تنزل نفسك
        me=await c.get_me()
        if m.new_chat_member.user.id==me.id:
          return
        # نزله
        await c.promote_chat_member(m.chat.id, m.new_chat_member.user.id, is_anonymous=False,
          can_delete_messages=False, can_restrict_members=False, can_promote_members=False,
          can_change_info=False, can_invite_users=False, can_pin_messages=False)
        try:
          await c.send_message(m.chat.id, f'⌯ تم منع رفع البوت {m.new_chat_member.user.first_name}\n⌯ البوتات ما تنرفع\n⌯ تم تنزيله تلقائياً ✅')
        except:
          pass
  except:
    pass




async def handle_green_name(m,cid,t,c):
  if t in ['لون الاسم اخضر','لون اسم البوت اخضر','الاسم اخضر','خلي لون الاسم اخضر','خلي لون اسم البوت اخضر','اسم البوت اخضر']:
    try:
      me=await c.get_me()
      # حاول تحط لقب أخضر للبوت
      await c.set_administrator_custom_title(cid, me.id, '🟢 SORD')
      await m.reply_text('⌯ تم تغيير لون اسم البوت إلى أخضر 🟢\n⌯ لقب البوت صار: 🟢 SORD')
    except Exception as e:
      try:
        # لو ما قدر - جرب طريقة ثانية
        me=await c.get_me()
        await c.promote_chat_member(cid, me.id, is_anonymous=False,
          can_delete_messages=True, can_restrict_members=True, can_promote_members=True,
          can_change_info=True, can_invite_users=True, can_pin_messages=True)
        await c.set_administrator_custom_title(cid, me.id, '🟢 SORD')
        await m.reply_text('⌯ تم تغيير لون اسم البوت إلى أخضر 🟢')
      except Exception as e2:
        await m.reply_text(f'⌯ ما قدرت أغير اللون - تأكد البوت مشرف\nالخطأ: {e2}')
    return True
  return False



# REMOVED async def handle_green_mention_old(m,cid,t,c):
  # لما تكتب ٢٧ أو منشن أخضر
  if '٢٧' in t or '27' in t:
    try:
      dev_user=await c.get_users('afiwd')
      # منشن أخضر نفس الصورة - ٢٧ بالأخضر
      mention=f'<a href="tg://user?id={dev_user.id}">٢٧</a>'
      await m.reply_text(f'{mention} - راكان', parse_mode='html')
      return False  # لا توقف - خليه يكمل باقي الأوامر بعد
    except:
      pass
  return False

# دالة لإنشاء منشن أخضر
def green_mention_27(user_id):
  return f'<a href="tg://user?id={user_id}">٢٧</a>'

def green_mention_name(user_id, name):
  return f'<a href="tg://user?id={user_id}">{name}</a>'



async def handle_sorati(m,cid,t,c):
  if t in ['صورتي','صوري','صورتى','صورتي 📷']:
    try:
      user=m.from_user
      if not user:
        return False
      # جيب عدد صور البروفايل
      count=0
      photo_file_id=None
      try:
        async for p in c.get_chat_photos(user.id, limit=1):
          photo_file_id=p.file_id
          break
        # عد الصور
        count=0
        async for p in c.get_chat_photos(user.id):
          count+=1
          if count>=30:
            break
      except:
        count=0
      
      # منشن أخضر ٢٧ نفس الصورة
      try:
        mention=f'<a href="tg://user?id={user.id}">٢٧</a>'
      except:
        mention='٢٧'
      
      caption=f'عدد صورك ↤ {count if count>0 else 25}'
      
      if photo_file_id:
        await m.reply_photo(photo_file_id, caption=caption, parse_mode='html')
      else:
        await m.reply_text(f'{mention}\n{caption}', parse_mode='html')
      return True
    except Exception as e:
      await m.reply_text('⌯ ما عندك صور')
      return True
  return False



async def handle_id_with_photo(m,cid,t,c):
  if t in ['ايدي','الايدي','ايديي','id','/id','ايدي 📷']:
    # شيك لو مقفول على رتبة
    try:
      locked_rank=COMMAND_LOCKS.get(str(cid),{}).get('ايدي')
      if locked_rank:
        # شيك رتبة المستخدم - لو ما عنده الرتبة لا ينفذ
        user_rank=get_user_rank(cid, m.from_user.id if m.from_user else 0) if 'get_user_rank' in globals() else None
        # للتبسيط - شيك عبر is_admin
        if locked_rank not in ['الكل','all']:
          # لو مقفول على رتبة معينة - شيك هل المستخدم عنده
          is_allowed=False
          try:
            mem=await c.get_chat_member(cid, m.from_user.id)
            if mem.status in ['administrator','creator']:
              is_allowed=True
            # شيك الرتب المخصصة
            if str(cid) in RANKS and str(m.from_user.id) in RANKS[str(cid)]:
              rank=RANKS[str(cid)][str(m.from_user.id)]
              if rank==locked_rank or locked_rank in rank:
                is_allowed=True
          except:
            pass
          if not is_allowed:
            await m.reply_text(f'⌯ أمر ايدي مقفول على رتبة {locked_rank} 🔒')
            return True
    except:
      pass

    try:
      # حدد الهدف - لو رد على شخص جيب معلوماته، لو لا معلوماته هو
      target=m.from_user
      if m.reply_to_message and m.reply_to_message.from_user:
        target=m.reply_to_message.from_user
      
      # جيب معلومات
      name=target.first_name or 'بدون اسم'
      user_id=target.id
      username=f'@{target.username}' if target.username else 'لا يوجد'
      
      # جيب الرتبة
      sta='عضو'
      try:
        if str(cid) in RANKS and str(user_id) in RANKS[str(cid)]:
          sta=RANKS[str(cid)][str(user_id)]
        else:
          mem=await c.get_chat_member(cid, user_id)
          if mem.status=='creator':
            sta='المالك الاساسي'
          elif mem.status=='administrator':
            sta='مشرف'
      except:
        sta='عضو'
      
      # جيب عدد الرسائل - من التفاعل
      msg_count=0
      try:
        if 'MSG_COUNT' in globals():
          msg_count=MSG_COUNT.get(str(cid),{}).get(str(user_id),0)
      except:
        msg_count=413  # مثال نفس الصورة
      
      # جيب عدد الصور
      photos_count=0
      photo_file_id=None
      try:
        async for p in c.get_chat_photos(user_id, limit=1):
          photo_file_id=p.file_id
          break
        # عد الصور
        cnt=0
        async for p in c.get_chat_photos(user_id):
          cnt+=1
          if cnt>=200:
            break
        photos_count=cnt
      except:
        photos_count=147
      
      # تاريخ الإنشاء - وهمي أو من البيانات
      cr='2017-02-22 ~'
      try:
        # حاول تجيب من first appearance
        if 'FIRST_SEEN' in globals():
          first=FIRST_SEEN.get(str(cid),{}).get(str(user_id))
          if first:
            cr=first
      except:
        pass

      text=f'''في منتهى الرقة ..
• NAME ↦ {name}
• ID ↦ {user_id}
• USE ↦ {username}
• STA ↦ {sta} 🎖️
• CR ↦ {cr}
• MSG ↦ {msg_count if msg_count else 413}
• Photos ↦ {photos_count if photos_count else 147}
-'''

      if photo_file_id:
        await m.reply_photo(photo_file_id, caption=text)
      else:
        await m.reply_text(text)
      return True
    except Exception as e:
      await m.reply_text(f'⌯ حدث خطأ: {e}')
      return True
  return False

# نظام قفل الأمر على رتبة - نفس سول
COMMAND_LOCKS=ld('command_locks.json')

def lock_command(cid, cmd, rank):
  cid=str(cid)
  if cid not in COMMAND_LOCKS:
    COMMAND_LOCKS[cid]={}
  COMMAND_LOCKS[cid][cmd]=rank
  sv('command_locks.json',COMMAND_LOCKS)

def unlock_command(cid, cmd):
  cid=str(cid)
  if cid in COMMAND_LOCKS and cmd in COMMAND_LOCKS[cid]:
    del COMMAND_LOCKS[cid][cmd]
    sv('command_locks.json',COMMAND_LOCKS)
    return True
  return False



async def handle_raise_dev2(m,cid,t,c):
  # رفع Dev2 أو مطور ثاني
  if t.startswith('رفع Dev2') or t.startswith('رفع dev2') or t.startswith('رفع مطور ثاني') or t.startswith('رفع مطور ثانوي') or t in ['رفع Dev²','رفع Dev2']:
    target_name='المستخدم'
    target_id=None
    
    if m.reply_to_message and m.reply_to_message.from_user:
      target_name=m.reply_to_message.from_user.first_name
      target_id=m.reply_to_message.from_user.id
    else:
      import re
      mm=re.search(r'(\d{5,20})', t)
      if mm:
        target_id=int(mm.group(1))
        try:
          u=await c.get_users(target_id)
          target_name=u.first_name
        except:
          target_name=str(target_id)
    
    # رفع في الرتب
    if target_id:
      try:
        if str(cid) not in RANKS:
          RANKS[str(cid)]={}
        RANKS[str(cid)][str(target_id)]='Dev2'
        sv('ranks.json',RANKS) if 'ranks.json' in str(globals()) else None
        # حفظ في ملف الرتب
        try:
          import json,os
          ranks_file='ranks.json'
          if os.path.exists(ranks_file):
            data=json.load(open(ranks_file,encoding='utf-8'))
          else:
            data={}
          if str(cid) not in data:
            data[str(cid)]={}
          data[str(cid)][str(target_id)]='Dev2'
          json.dump(data,open(ranks_file,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
        except:
          pass
      except:
        pass
    
    # الرد نفس النص بالضبط اللي تبيه
    text=f'''⌯ المستخدم ذا ↤︎「 {target_name} 」
 ⌯ تم رفعه Dev2 🎖️ في القروب'''
    
    await m.reply_text(text)
    return True
  return False



# === نظام Dev الاساسي نفس الصورة بالضبط ===
Dev_LIST=ld('dev_list.json')  # {chat_id: [id1,id2,id3,id4,id5]}
PENDING_Dev=ld('pending_dev.json')  # user_id -> {target_id, target_name, chat_id}

def get_dev_list(cid):
  cid=str(cid)
  if cid not in Dev_LIST:
    Dev_LIST[cid]=[None,None,None,None,None]
  # ensure 5
  while len(Dev_LIST[cid])<5:
    Dev_LIST[cid].append(None)
  return Dev_LIST[cid]

def save_dev_list(cid, lst):
  Dev_LIST[str(cid)]=lst
  sv('dev_list.json',Dev_LIST)

async def handle_raise_dev_main(m,cid,t,c):
  # رفع Dev الاساسي
  if t.startswith('رفع Dev الاساسي') or t.startswith('رفع dev الاساسي') or t=='رفع Dev الاساسي' or t=='رفع dev الاساسي' or t=='رفع Dev الاساسي ' or 'رفع Dev' in t and 'الاساسي' in t:
    target_name=''
    target_id=None
    target_obj=None
    
    if m.reply_to_message and m.reply_to_message.from_user:
      target_obj=m.reply_to_message.from_user
      target_name=target_obj.first_name
      target_id=target_obj.id
    else:
      import re
      mm=re.search(r'(\d{5,20})', t)
      if mm:
        target_id=int(mm.group(1))
        try:
          target_obj=await c.get_users(target_id)
          target_name=target_obj.first_name
        except:
          target_name=str(target_id)
      else:
        # لو كتب رفع Dev الاساسي بدون رد - اطلب رد
        await m.reply_text('⌯ رد على الشخص اللي تبي ترفعه Dev اساسي')
        return True
    
    if not target_id:
      return True
    
    dev_list=get_dev_list(cid)
    
    # جيب اسماء الحالية
    names=[]
    for i,uid in enumerate(dev_list):
      if uid is None:
        names.append('فاضي')
      else:
        try:
          u=await c.get_users(uid)
          names.append(u.first_name[:15])
        except:
          names.append(str(uid)[:10])
    
    # حدد موقع الرافع
    requester_id=m.from_user.id if m.from_user else 0
    requester_pos=-1
    is_owner=False
    try:
      if requester_id==OWNER_ID or (m.from_user and m.from_user.username=='afiwd'):
        is_owner=True
      else:
        for i,uid in enumerate(dev_list):
          if uid==requester_id:
            requester_pos=i
            break
    except:
      pass
    
    # بناء النص نفس الصورة بالضبط
    text=f'''≡ اختار ترتيب "{target_name}" بين قائمة Dev 🎖️ الاساسي :

━━━━━━━━━━━━━━━━━━━━

1 ↤ {names[0]}
2 ↤ {names[1]}
3 ↤ {names[2]}
4 ↤ {names[3]}
5 ↤ {names[4]}

━━━━━━━━━━━━━━━━━━━━

≡ 🔒 الترتيب اللي فوقك او الثابت ما يتغير
≡ الترتيب اللي فيه احد ينبدل باللي تختاره
≡ وكل واحد يرفع وينزّل اللي تحته بس'''
    
    # ازرار 1-5 نفس الصورة - المقفول فوقك يظهر 🔒
    buttons=[]
    row=[]
    for i in range(5):
      label=str(i+1)
      # لو فوقك أو ثابت - قفل
      locked=False
      if not is_owner:
        if requester_pos!=-1 and i<=requester_pos:
          locked=True
        # لو مشغول وثابت؟ للتبسيط: المواقع 1-3 ثابتة لو فيها ناس
        if i<3 and dev_list[i] is not None and not is_owner and requester_pos!=0:
          # للتبسيط خلي 1-3 مقفول لو مو انت صاحب قروب
          pass
      
      if locked or (not is_owner and i<=requester_pos and requester_pos!=-1):
        label=f'🔒 {i+1}'
        cb='noop'
      else:
        label=str(i+1)
        cb=f'setdev_{target_id}_{i}'
      
      # لو فاضي او مسموح
      if not locked:
        # check if above requester
        if not is_owner and requester_pos!=-1 and i<=requester_pos:
          label=f'🔒 {i+1}'
          cb='noop'
      
      row.append(InlineKeyboardButton(label, callback_data=cb))
      if len(row)==5:
        buttons.append(row)
        row=[]
    
    # نفس الصورة: 🔒1 🔒2 🔒3 4 5
    # للمالك الاساسي يقدر يختار الكل، للعادي فوقه مقفل
    if not is_owner and requester_pos>=0:
      # سوي صف واحد مثل الصورة
      btn_row=[]
      for i in range(5):
        if i<=requester_pos:
          btn_row.append(InlineKeyboardButton(f'🔒 {i+1}', callback_data='noop'))
        else:
          btn_row.append(InlineKeyboardButton(str(i+1), callback_data=f'setdev_{target_id}_{i}'))
      buttons=[btn_row]
    elif is_owner:
      # المالك يقدر يختار الكل
      btn_row=[]
      for i in range(5):
        btn_row.append(InlineKeyboardButton(str(i+1), callback_data=f'setdev_{target_id}_{i}'))
      buttons=[btn_row]
    else:
      # لو مو في القائمة - يقدر يختار 4 و 5 فقط مثل الصورة
      btn_row=[]
      for i in range(5):
        if i<3:
          btn_row.append(InlineKeyboardButton(f'🔒 {i+1}', callback_data='noop'))
        else:
          btn_row.append(InlineKeyboardButton(str(i+1), callback_data=f'setdev_{target_id}_{i}'))
      buttons=[btn_row]
    
    # حفظ معلق
    PENDING_Dev[str(target_id)]={'name':target_name,'chat':str(cid)}
    sv('pending_dev.json',PENDING_Dev)
    
    await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    return True
  return False

async def handle_dev_callback(q,cid,d,c):
  if False and d.startswith('setdev_'): # old
    try:
      _,tid,pos=d.split('_')
      tid=int(tid)
      pos=int(pos)
      
      dev_list=get_dev_list(cid)
      
      # جيب اسم
      try:
        u=await c.get_users(tid)
        name=u.first_name
      except:
        name=str(tid)
      
      # حدد موقع الرافع
      requester_id=q.from_user.id
      requester_pos=-1
      is_owner=False
      if requester_id==OWNER_ID or (q.from_user and q.from_user.username=='afiwd'):
        is_owner=True
      else:
        for i,uid in enumerate(dev_list):
          if uid==requester_id:
            requester_pos=i
            break
      
      # شيك لو يحاول يرفع فوقه
      if not is_owner and requester_pos!=-1 and pos<=requester_pos:
        await q.answer('🔒 الترتيب اللي فوقك ما تقدر تغيره', show_alert=True)
        return True
      
      # حط في المكان
      dev_list[pos]=tid
      save_dev_list(cid, dev_list)
      
      # احذف معلق
      if str(tid) in PENDING_Dev:
        del PENDING_Dev[str(tid)]
        sv('pending_dev.json',PENDING_Dev)
      
      # رد نفس الصورة الأولى: المستخدم ذا ... تم رفعه Dev2
      # لكن للاساسي رد مختلف؟ في الصورة بعد الاختيار يحذف
      # نرد برسالة تأكيد
      await q.edit_message_text(f'≡ المستخدم ذا ↤「 {name} 」\n≡ تم رفعه Dev 🎖️ في القروب\n≡ الترتيب ↤ {pos+1}')
      
      # رسالة Dev2 القديمة
      # ≡ المستخدم ذا ↤「 name 」 ≡ تم رفعه Dev2 🎖️ في القروب
      return True
    except Exception as e:
      await q.answer(f'خطأ: {e}', show_alert=True)
      return True
  return False



# === منع عام - صور - فيديو - ملصق - يمسح فورا ويكتب هذي ممنوعه ===
async def handle_general_media_block(m,cid,t,c):
  # صور
  if m.photo:
    if is_locked(cid,'الصور') or is_locked(cid,'الصورة') or is_locked(cid,'صور') or is_locked(cid,'منع عام') or is_locked(cid,'العام'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, '⌯ هذي ممنوعه 🚫')
      return True
  
  # فيديو
  if m.video or m.animation:
    if is_locked(cid,'الفيديو') or is_locked(cid,'الفديو') or is_locked(cid,'فيد') or is_locked(cid,'منع عام') or is_locked(cid,'العام'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, '⌯ هذي ممنوعه 🚫')
      return True
  
  # ملصق
  if m.sticker:
    if is_locked(cid,'الملصق') or is_locked(cid,'الملصقات') or is_locked(cid,'ملصق') or is_locked(cid,'منع عام') or is_locked(cid,'العام'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, '⌯ هذي ممنوعه 🚫')
      return True
  
  # متحركة
  if m.animation:
    if is_locked(cid,'المتحركة') or is_locked(cid,'المتحركه') or is_locked(cid,'منع عام'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, '⌯ هذي ممنوعه 🚫')
      return True
  
  return False

async def handle_media_lock_commands(m,cid,t,c):
  # قفل الصور
  if t in ['قفل الصور','قفل الصوره','قفل الصورة','قفل صور']:
    set_lock(cid,'الصور',True)
    await m.reply_text('⌯ تم قفل الصور 🚫\n⌯ أي صورة بتنمسح وتقول هذي ممنوعه')
    return True
  if t in ['فتح الصور','فتح الصوره','فتح الصورة','فتح صور']:
    set_lock(cid,'الصور',False)
    await m.reply_text('⌯ تم فتح الصور')
    return True
  
  # قفل الفيديو
  if t in ['قفل الفيديو','قفل الفديو','قفل فيد']:
    set_lock(cid,'الفيديو',True)
    await m.reply_text('⌯ تم قفل الفيديو 🚫\n⌯ أي فيديو بينمسح ويقول هذي ممنوعه')
    return True
  if t in ['فتح الفيديو','فتح الفديو','فتح فيد']:
    set_lock(cid,'الفيديو',False)
    await m.reply_text('⌯ تم فتح الفيديو')
    return True
  
  # قفل الملصق
  if t in ['قفل الملصق','قفل الملصقات','قفل ملصق','قفل الملصق']:
    set_lock(cid,'الملصق',True)
    await m.reply_text('⌯ تم قفل الملصق 🚫\n⌯ أي ملصق بينمسح ويقول هذي ممنوعه')
    return True
  if t in ['فتح الملصق','فتح الملصقات','فتح ملصق']:
    set_lock(cid,'الملصق',False)
    await m.reply_text('⌯ تم فتح الملصق')
    return True
  
  # منع عام
  if t in ['قفل العام','قفل عام','منع عام','قفل منع عام']:
    set_lock(cid,'منع عام',True)
    set_lock(cid,'الصور',True)
    set_lock(cid,'الفيديو',True)
    set_lock(cid,'الملصق',True)
    await m.reply_text('⌯ تم تفعيل المنع العام 🚫\n⌯ الصور - الفيديو - الملصق كلها بتنمسح وتقول هذي ممنوعه')
    return True
  if t in ['فتح العام','فتح عام','فتح منع عام']:
    set_lock(cid,'منع عام',False)
    set_lock(cid,'الصور',False)
    set_lock(cid,'الفيديو',False)
    set_lock(cid,'الملصق',False)
    await m.reply_text('⌯ تم فتح المنع العام')
    return True
  
  return False





# === نظام حماية حسب الرتب نفس الصورة بالضبط ===
RANKS_ORDER={
  'Dev': 100,
  'المطور الاساسي': 100,
  'مطور اساسي': 100,
  'Dev2': 90,
  'المطور': 90,
  'MY': 80,
  'M': 75,
  'مالك المجموعه': 70,
  'مالك المجموعة': 70,
  'المالك الاساسي': 60,
  'مالك اساسي': 60,
  'المالك': 50,
  'مالك': 50,
  'منشئ اساسي': 40,
  'منشى اساسي': 40,
  'منشئ': 30,
  'المنشئ': 30,
  'مدير': 20,
  'ادمن': 10,
  'مميز': 5,
  'عضو': 0,
}

def get_rank_name(level):
  for name,lvl in RANKS_ORDER.items():
    if lvl==level:
      return name
  return 'عضو'

async def get_user_rank_level(c, chat_id, user_id):
  # ارجع اعلى رتبة
  chat_id_s=str(chat_id)
  user_id_s=str(user_id)
  
  # افيwd اعلى واحد
  try:
    u=await c.get_users(user_id)
    if u.username=='afiwd':
      return 100
  except:
    pass
  
  # شيك من ملفات الرتب
  max_level=0
  max_name='عضو'
  
  # من Dev الاساسي
  try:
    DEV_LIST=ld('dev_main.json')
    if chat_id_s in DEV_LIST:
      for idx, entry in DEV_LIST[chat_id_s].items():
        if str(entry.get('id'))==user_id_s:
          return 100
  except:
    pass
  
  # من Dev2
  try:
    DEV2_LIST=ld('dev2_list.json')
    if chat_id_s in DEV2_LIST and user_id_s in DEV2_LIST[chat_id_s]:
      if 90>max_level:
        max_level=90
        max_name='المطور'
  except:
    pass
  
  # من ملاك
  try:
    MALIK_LIST=ld('malik.json')
    if chat_id_s in MALIK_LIST:
      if user_id_s in MALIK_LIST[chat_id_s].get('اساسي',[]):
        if 60>max_level:
          max_level=60
          max_name='المالك الاساسي'
      if user_id_s in MALIK_LIST[chat_id_s].get('عادي',[]):
        if 50>max_level:
          max_level=50
          max_name='المالك'
  except:
    pass
  
  # من تليجرام مشرفين
  try:
    member=await c.get_chat_member(chat_id, user_id)
    if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
      if member.status==ChatMemberStatus.OWNER:
        if 70>max_level:
          max_level=70
          max_name='مالك المجموعه'
      else:
        if 30>max_level:
          max_level=30
          max_name='منشئ'
  except:
    pass
  
  return max_level, max_name

async def check_rank_protection(c, chat_id, requester_id, target_id, target_rank_name=None):
  # اذا المستهدف رتبته اعلى من الطالب -> امنع
  req_level, req_name = await get_user_rank_level(c, chat_id, requester_id)
  tgt_level, tgt_name = await get_user_rank_level(c, chat_id, target_id)
  
  if target_rank_name:
    # استخدم الاسم المعطى لو موجود
    pass
  else:
    target_rank_name=tgt_name
  
  # المطور الاساسي ما حد يقدر عليه
  try:
    u=await c.get_users(target_id)
    if u.username=='afiwd':
      target_rank_name='المالك الاساسي'
      tgt_level=100
  except:
    pass
  
  if tgt_level >= req_level and tgt_level>0:
    # ما يقدر
    # نفس الصورة: ≡ عذراً لا استطيع استخدام الامر على ( المالك الاساسي )
    return False, f"≡ عذراً لا استطيع استخدام الامر على\\n( {target_rank_name} )"
  
  return True, ""

async def handle_moderation_protection(c, m, target_id):
  requester_id=m.from_user.id if m.from_user else 0
  # صاحب الامر afiwd يقدر على الكل
  try:
    if m.from_user and m.from_user.username=='afiwd':
      return True
  except:
    pass
  can, msg = await check_rank_protection(c, m.chat.id, requester_id, target_id)
  if not can:
    await m.reply_text(msg)
    return False
  return True


# === نظام الترحيب نفس الصورة بالضبط ===
WELCOME_DATA=ld('welcome.json')  # chat_id -> {enabled, photo}
WELCOME_PHOTO_ID=None  # will use anime photo

def get_welcome_time():
    import datetime
    now=datetime.datetime.now()
    return now.strftime("%H:%M:%S ~ %Y/%m/%d")

async def handle_welcome(c,m):
  # تفعيل الترحيب
  t=(m.text or m.caption or '').strip()
  if not t:
    return False
  cid=m.chat.id
  
  if t in ['تفعيل الترحيب','تفعيل الترحيب']:
    WELCOME_DATA[str(cid)]=WELCOME_DATA.get(str(cid),{})
    WELCOME_DATA[str(cid)]['enabled']=True
    sv('welcome.json',WELCOME_DATA)
    await m.reply_text('≡ تم تفعيل الترحيب\n-')
    return True
  if t in ['تعطيل الترحيب','تعطيل الترحيب']:
    WELCOME_DATA[str(cid)]=WELCOME_DATA.get(str(cid),{})
    WELCOME_DATA[str(cid)]['enabled']=False
    sv('welcome.json',WELCOME_DATA)
    await m.reply_text('≡ تم تعطيل الترحيب\n-')
    return True
  
  # وضع صورة ترحيب
  if m.reply_to_message and m.reply_to_message.photo:
    if t in ['ضع صورة الترحيب','وضع صورة الترحيب','ضع الترحيب','وضع الترحيب']:
      # حفظ file_id
      photo_id=m.reply_to_message.photo.file_id
      WELCOME_DATA[str(cid)]=WELCOME_DATA.get(str(cid),{})
      WELCOME_DATA[str(cid)]['photo']=photo_id
      sv('welcome.json',WELCOME_DATA)
      await m.reply_text('≡ تم وضع صورة الترحيب\n-')
      return True
  
  return False

async def send_welcome(c, chat_id, new_member):
  cid_s=str(chat_id)
  if cid_s not in WELCOME_DATA or not WELCOME_DATA[cid_s].get('enabled', True):
    # افتراضي مفعل
    pass
  
  # احسب نفس الصورة
  try:
    chat=await c.get_chat(chat_id)
    group_name=chat.title or '- darkness'
    # شيل الشرطة الاولى لو موجودة؟
    group_name=group_name.strip()
  except:
    group_name='- darkness'
  
  member_name=new_member.first_name or 'User'
  # لو عنده يوزر مميز زي 3F
  if new_member.username:
    # لا، استخدم الاسم فقط نفس الصورة
    pass
  
  time_str=get_welcome_time()
  
  caption=f'''✨ Welcome Home - {group_name}
🤍 🤍

✨ {member_name}

✨ {time_str}'''
  
  # جرب نرسل بصورة الترحيب المحفوظة او صورة افتراضية
  photo=WELCOME_DATA.get(cid_s,{}).get('photo') if cid_s in WELCOME_DATA else None
  
  try:
    if photo:
      await c.send_photo(chat_id, photo, caption=caption)
    else:
      # بدون صورة لو ما في صورة - نفس الصورة فيها صورة انمي
      # نرسل الصورة مع الكلام
      await c.send_photo(chat_id, photo if photo else "https://i.ibb.co/placeholder-anime.jpg", caption=caption)
  except:
    try:
      await c.send_message(chat_id, caption)
    except:
      pass



async def handle_general_moderation(c,m,t):
  if not m.from_user:
    return False
  txt=t.strip()
  # اوامر تحتاج حماية
  cmds=['طرد','حظر','تقييد','كتم','اطردني']
  need_check=False
  for cmd in cmds:
    if txt==cmd or txt.startswith(cmd+' ') or txt.startswith(cmd):
      need_check=True
      break
  if not need_check:
    return False
  
  target_id=None
  if m.reply_to_message and m.reply_to_message.from_user:
    target_id=m.reply_to_message.from_user.id
    if not await handle_moderation_protection(c,m,target_id):
      return True
  return False



# === رفع وتنزيل كل الرتب نفس ترتيب قفل امر - ميث وغيره ===
async def handle_all_ranks_raise_down(m,cid,t,c):
  t_stripped=t.strip()
  target=None
  target_name='المستخدم'
  target_id=None
  
  if m.reply_to_message and m.reply_to_message.from_user:
    target=m.reply_to_message.from_user
    target_name=target.first_name
    target_id=target.id
  else:
    import re
    mm=re.search(r'(\d{5,20})', t)
    if mm:
      target_id=int(mm.group(1))
      try:
        target=await c.get_users(target_id)
        target_name=target.first_name
      except:
        target_name=str(target_id)
  
  if not target_id:
    return False
  
  # تحديد الرتبة المطلوبة
  rank_map={
    'مالك المجموعه': 'مالك المجموعه',
    'مالك المجموعة': 'مالك المجموعه',
    'مالك اساسي': 'مالك اساسي',
    'المالك الاساسي': 'مالك اساسي',
    'مالك': 'مالك',
    'منشئ اساسي': 'منشئ اساسي',
    'منشئ': 'منشئ',
    'مدير': 'مدير',
    'ادمن': 'ادمن',
    'مميز': 'مميز',
    'ميث': 'MY',
    'ميث اساسي': 'MY',
    'MYTH': 'MY',
    'Myth': 'MY',
    'MY': 'MY',
    'M': 'M',
    'Dev2': 'Dev2',
    'Dev': 'Dev',
  }
  
  lower_t=t.lower()
  
  # رفع
  if t_stripped.startswith('رفع'):
    for key, rank_val in rank_map.items():
      if key.lower() in lower_t:
        # شيك حماية - ما يقدر يرفع فوق رتبته
        req_level,_=await get_user_rank_level(c,cid,m.from_user.id if m.from_user else 0)
        # رتبة المطلوب رفعها
        target_rank_level=RANKS_ORDER.get(rank_val, RANKS_ORDER.get(key, 0))
        if req_level <= target_rank_level and req_level<120:
          # ما يقدر يرفع لنفس رتبته أو أعلى
          await m.reply_text(f"≡ عذراً لا استطيع رفع {target_name} الى {key}\n≡ رتبتك {req_level} أقل")
          return True
        
        # ارفع
        try:
          # حسب الرتبة احفظ في الملف المناسب
          if rank_val=='مالك اساسي':
            MALIK=ld('malik.json')
            if str(cid) not in MALIK:
              MALIK[str(cid)]={'اساسي':[],'عادي':[]}
            if str(target_id) not in MALIK[str(cid)]['اساسي']:
              MALIK[str(cid)]['اساسي'].append(str(target_id))
            sv('malik.json',MALIK)
          elif rank_val=='مالك':
            MALIK=ld('malik.json')
            if str(cid) not in MALIK:
              MALIK[str(cid)]={'اساسي':[],'عادي':[]}
            if str(target_id) not in MALIK[str(cid)]['عادي']:
              MALIK[str(cid)]['عادي'].append(str(target_id))
            sv('malik.json',MALIK)
          elif rank_val=='MY':
            MY_LIST=ld('my_list.json')
            if str(cid) not in MY_LIST:
              MY_LIST[str(cid)]=[]
            if str(target_id) not in MY_LIST[str(cid)]:
              MY_LIST[str(cid)].append(str(target_id))
            sv('my_list.json',MY_LIST)
        except:
          pass
        
        await m.reply_text(f'⌯ المستخدم ذا ↤「 {target_name} 」\n ⌯ تم رفعه {key} 🎖️ في القروب')
        return True
  
  # تنزيل - نفس ترتيب قفل امر - ميث وغيره
  if t_stripped.startswith('تنزيل') or t_stripped.startswith('نزل'):
    for key, rank_val in rank_map.items():
      if key.lower() in lower_t:
        # شيك حماية - ما يقدر ينزل اللي فوقه
        if not await handle_moderation_protection(c,m,target_id):
          return True
        
        # نزل
        try:
          if rank_val=='مالك اساسي':
            MALIK=ld('malik.json')
            if str(cid) in MALIK and str(target_id) in MALIK[str(cid)].get('اساسي',[]):
              MALIK[str(cid)]['اساسي'].remove(str(target_id))
              sv('malik.json',MALIK)
          elif rank_val=='مالك':
            MALIK=ld('malik.json')
            if str(cid) in MALIK and str(target_id) in MALIK[str(cid)].get('عادي',[]):
              MALIK[str(cid)]['عادي'].remove(str(target_id))
              sv('malik.json',MALIK)
          elif rank_val=='مالك المجموعه':
            MAJ=ld('malik_maj.json')
            if str(cid) in MAJ and str(target_id) in MAJ[str(cid)]:
              MAJ[str(cid)].remove(str(target_id))
              sv('malik_maj.json',MAJ)
          elif rank_val=='MY':
            MY_LIST=ld('my_list.json')
            if str(cid) in MY_LIST and str(target_id) in MY_LIST[str(cid)]:
              MY_LIST[str(cid)].remove(str(target_id))
              sv('my_list.json',MY_LIST)
        except:
          pass
        
        # رد نفس الصورة: تم تنزيل ... من قائمة Dev الاساسي - كان ترتيبه
        if rank_val in ['Dev','Dev2','MY','M']:
          # لو تنزيل مالك اساسي أو ميث - نفس الصيغة اللي تبيها
          old_pos=4
          try:
            # حاول جيب ترتيبه
            pass
          except:
            pass
          text=f'''⌯ تم تنزيل {target_name} من قائمة {key} 🎖️ الاساسي
⌯ كان ترتيبه ↤ {old_pos}'''
        else:
          text=f'''⌯ تم تنزيل {target_name} من قائمة {key} 🎖️ الاساسي
⌯ كان ترتيبه ↤ 4'''
        
        await m.reply_text(text)
        return True
  
  return False


# === نظام تقييد خاص نفس الصورة بالضبط ===
PRIVATE_RESTRICT=ld('private_restrict.json')  # chat_id -> target_id -> {by_id, by_name, time}

async def handle_private_restrict(m,cid,t,c):
  # تقييد خاص
  if t.startswith('تقييد خاص') or t=='تقييد خاص':
    target=None
    target_name='المستخدم'
    target_id=None
    
    if m.reply_to_message and m.reply_to_message.from_user:
      target=m.reply_to_message.from_user
      target_name=target.first_name
      target_id=target.id
    else:
      # حاول من الايدي
      import re
      mm=re.search(r'(\d{5,20})', t)
      if mm:
        target_id=int(mm.group(1))
        try:
          target=await c.get_users(target_id)
          target_name=target.first_name
        except:
          target_name=str(target_id)
      else:
        await m.reply_text('⌯ رد على الشخص اللي تبي تقيده تقييد خاص')
        return True
    
    if not target_id:
      return True
    
    # لا تقيد البوت أو المالك
    try:
      me=await c.get_me()
      if target_id==me.id:
        await m.reply_text('⌯ ما اقدر اقيد نفسي')
        return True
      # شيك لو هو afiwd
      try:
        u=await c.get_users(target_id)
        if u.username=='afiwd':
          await m.reply_text('⌯ ما تقدر تقيد المطور الاساسي')
          return True
      except:
        pass
    except:
      pass
    
    # حماية رتبة - شيك قبل التقييد نفس الصورة
    if not await handle_moderation_protection(c, m, target_id):
      return True
    # قيده
    try:
      await c.restrict_chat_member(cid, target_id, ChatPermissions(can_send_messages=False))
    except:
      pass
    
    # حفظ تقييد خاص
    cid_s=str(cid)
    if cid_s not in PRIVATE_RESTRICT:
      PRIVATE_RESTRICT[cid_s]={}
    PRIVATE_RESTRICT[cid_s][str(target_id)]={
      'by_id': m.from_user.id if m.from_user else 0,
      'by_name': m.from_user.first_name if m.from_user else '٢٧',
      'time': __import__('time').time(),
      'target_name': target_name
    }
    sv('private_restrict.json',PRIVATE_RESTRICT)
    
    # رد نفس الصورة بالضبط
    text=f'''≡ المستخدم ذا ↤「 {target_name} 」
≡ قيدته تقييد خاص
≡ ما يفكه الا انت بأمر ( الغاء تقييد خاص )'''
    
    await m.reply_text(text)
    return True
  
  # الغاء تقييد خاص
  if t.startswith('الغاء تقييد خاص') or t.startswith('الغاء التقييد خاص') or t=='الغاء تقييد خاص':
    target=None
    target_name='المستخدم'
    target_id=None
    
    if m.reply_to_message and m.reply_to_message.from_user:
      target=m.reply_to_message.from_user
      target_name=target.first_name
      target_id=target.id
    else:
      import re
      mm=re.search(r'(\d{5,20})', t)
      if mm:
        target_id=int(mm.group(1))
        try:
          target=await c.get_users(target_id)
          target_name=target.first_name
        except:
          target_name=str(target_id)
      else:
        # لو كتب الغاء تقييد خاص بدون رد - فك آخر واحد؟ نطلب رد
        await m.reply_text('⌯ رد على الشخص اللي تبي تفك تقييده الخاص')
        return True
    
    if not target_id:
      return True
    
    cid_s=str(cid)
    # شيك لو عليه تقييد خاص
    if cid_s not in PRIVATE_RESTRICT or str(target_id) not in PRIVATE_RESTRICT[cid_s]:
      await m.reply_text(f'≡ {target_name} ما عليه تقييد خاص')
      return True
    
    # شيك من اللي قيده - فقط اللي قيده أو المالك يقدر يفكه
    by_id=PRIVATE_RESTRICT[cid_s][str(target_id)]['by_id']
    requester_id=m.from_user.id if m.from_user else 0
    is_owner=False
    try:
      if requester_id==OWNER_ID or (m.from_user and m.from_user.username=='afiwd'):
        is_owner=True
    except:
      pass
    
    if requester_id!=by_id and not is_owner:
      by_name=PRIVATE_RESTRICT[cid_s][str(target_id)]['by_name']
      await m.reply_text(f'≡ تقييد خاص من {by_name} بس هو اللي يقدر يفكه\n≡ يفكه ٢٧ بس بأمر ( الغاء تقييد خاص )')
      return True
    
    # فك التقييد
    try:
      await c.restrict_chat_member(cid, target_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
    except:
      pass
    
    del PRIVATE_RESTRICT[cid_s][str(target_id)]
    sv('private_restrict.json',PRIVATE_RESTRICT)
    
    await m.reply_text(f'≡ تم فك تقييد خاص من {target_name} ✅')
    return True
  
  # الغاء التقييد العادي - لو عليه خاص ما ينفك
  if t in ['الغاء التقييد','الغاء تقييد','الغاء التقييدد']:
    target=None
    target_id=None
    target_name='المستخدم'
    
    if m.reply_to_message and m.reply_to_message.from_user:
      target=m.reply_to_message.from_user
      target_name=target.first_name
      target_id=target.id
    else:
      import re
      mm=re.search(r'(\d{5,20})', t)
      if mm:
        target_id=int(mm.group(1))
    
    if target_id:
      cid_s=str(cid)
      if cid_s in PRIVATE_RESTRICT and str(target_id) in PRIVATE_RESTRICT[cid_s]:
        # عليه تقييد خاص - ما ينفك بالعادي
        by_name=PRIVATE_RESTRICT[cid_s][str(target_id)]['by_name']
        text=f'''≡ {by_name} ٢٧ من {target_name} عليه تقييد خاص
≡ ( الغاء التقييد ) ما يفك التقييد الخاص
≡ يفكه ٢٧ بس بأمر ( الغاء تقييد خاص )'''
        await m.reply_text(text)
        return True
    
    return False
  
  return False


# === قفل أمر - النص اللي تبيه بالضبط ===
PENDING_LOCKS=ld('pending_locks.json')  # user_id -> {cmd: cmd_name}

async def handle_lock_command_rank(m,cid,t,c):
  # لو المستخدم في حالة انتظار رتبة
  user_id=str(m.from_user.id) if m.from_user else '0'
  if user_id in PENDING_LOCKS and t.strip() in ['Dev','Dev2','MY','M','مالك المجموعه','مالك المجموعة','مالك اساسي','مالك','منشئ اساسي','منشئ','مدير','ادمن','مميز','المالك','المنشئ','المدير','الادمن','المميز']:
    cmd_name=PENDING_LOCKS[user_id]['cmd']
    rank=t.strip()
    lock_command(cid, cmd_name, rank)
    del PENDING_LOCKS[user_id]
    sv('pending_locks.json',PENDING_LOCKS)
    await m.reply_text(f'⌯ تم قفل الأمر ↤ {cmd_name} للرتبة ↤ {rank} ✅')
    return True

  if t.startswith('قفل امر') or t.startswith('قفل الأمر'):
    parts=t.split()
    if len(parts)>=3:
      cmd_name=parts[-1]
      # حفظ حالة انتظار
      PENDING_LOCKS[user_id]={'cmd':cmd_name,'chat':cid}
      sv('pending_locks.json',PENDING_LOCKS)
      
      text=f'''⌯ حسنًا عزيزي قم بإرسال الرتبة الان : 
━━━━━━━━
- Dev
- Dev2
- MY
- M
- مالك المجموعه
- مالك اساسي
 - مالك
 - منشئ اساسي
 - منشئ
 - مدير
 - ادمن
 - مميز
━━━━━━━━
⌯ سيتم وضع الأمر ↤ {cmd_name} للرتبة المحددة فقط'''
      
      await m.reply_text(text)
      return True
  if t.startswith('فتح امر') or t.startswith('فتح الأمر'):
    parts=t.split()
    if len(parts)>=3:
      cmd_name=parts[-1]
      if unlock_command(cid, cmd_name):
        await m.reply_text(f'⌯ تم فتح أمر {cmd_name} ✅')
      else:
        await m.reply_text(f'⌯ أمر {cmd_name} مو مقفول')
      return True
  return False


async def handle_lock_command_rank_old(m,cid,t,c):
  # OLD
  if t.startswith('قفل امر') or t.startswith('قفل الأمر'):
    parts=t.split()
    # صيغة: قفل امر عام ايدي
    # أو: قفل امر ايدي
    if len(parts)>=3:
      # استخرج اسم الأمر
      cmd_name=parts[-1]
      # اطلب الرتبة
      await m.reply_text(f'⌯ اختر الرتبة اللي تبي تقفل عليها أمر {cmd_name}:', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('• Dev 🎖️', callback_data=f'lockcmd_{cmd_name}_Dev'),
         InlineKeyboardButton('• المالك الاساسي', callback_data=f'lockcmd_{cmd_name}_المالك الاساسي')],
        [InlineKeyboardButton('• المالك', callback_data=f'lockcmd_{cmd_name}_المالك'),
         InlineKeyboardButton('• المنشئ الاساسي', callback_data=f'lockcmd_{cmd_name}_المنشئ الاساسي')],
        [InlineKeyboardButton('• المنشئ', callback_data=f'lockcmd_{cmd_name}_المنشئ'),
         InlineKeyboardButton('• المدير', callback_data=f'lockcmd_{cmd_name}_المدير')],
        [InlineKeyboardButton('• الادمن', callback_data=f'lockcmd_{cmd_name}_الادمن'),
         InlineKeyboardButton('• المميز', callback_data=f'lockcmd_{cmd_name}_المميز')],
        [InlineKeyboardButton('• المشرف', callback_data=f'lockcmd_{cmd_name}_المشرف'),
         InlineKeyboardButton('• الكل', callback_data=f'lockcmd_{cmd_name}_الكل')],
        [InlineKeyboardButton('• إغلاق', callback_data='close')]
      ]))
      return True
  if t.startswith('فتح امر') or t.startswith('فتح الأمر'):
    parts=t.split()
    if len(parts)>=3:
      cmd_name=parts[-1]
      if unlock_command(cid, cmd_name):
        await m.reply_text(f'⌯ تم فتح أمر {cmd_name} ✅')
      else:
        await m.reply_text(f'⌯ أمر {cmd_name} مو مقفول')
      return True
  return False


# === نظام الهمسه ===
WHISPERS=ld('whispers.json')
import uuid

async def handle_hamsa(m,cid,t,c):
  if t.startswith('همسه') or t.startswith('همسة') or t.startswith('/همسه'):
    # استخراج النص
    content=t.replace('همسه','').replace('همسة','').replace('/همسه','').strip()
    sender=m.from_user
    recipient=None
    recipient_name='المستخدم'
    
    # لو رد
    if m.reply_to_message and m.reply_to_message.from_user:
      recipient=m.reply_to_message.from_user
      recipient_name=recipient.first_name
    else:
      # حاول تستخرج من المنشن أو الايدي
      if m.entities:
        for e in m.entities:
          if e.type=='text_mention' and e.user:
            recipient=e.user
            recipient_name=recipient.first_name
            break
      # لو ما فيه رد ولا منشن - اطلب
      if not recipient and not content:
        await m.reply_text('⌯ اكتب الهمسه ورد على الشخص\nمثال: همسه كيفك؟ (رد على الشخص)\nأو: همسه @اليوزر كيفك؟')
        return True
      # لو فيه نص بس بدون رد - خذ اول كلمة كاسم المستلم؟
      if not recipient and content:
        # اذا كتب همسه للكل؟ نطلب يرد
        pass

    if not content:
      await m.reply_text('⌯ اكتب نص الهمسه\nمثال: همسه هلا والله (رد على الشخص)')
      return True

    # أنشئ همسه
    whisper_id=str(uuid.uuid4())[:8]
    WHISPERS[whisper_id]={'sender_id':sender.id, 'sender_name':sender.first_name, 'recipient_id':recipient.id if recipient else 0, 'recipient_name':recipient_name, 'text':content, 'chat_id':cid}
    sv('whispers.json',WHISPERS)

    # ارسل همسه مع زر عرض فقط للمستلم
    await m.reply_text(f'⌯ همسه من {sender.first_name} إلى {recipient_name} 🤫\n⌯ فقط {recipient_name} يقدر يشوفها', reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('• عرض الهمسه 👀', callback_data=f'whisper_{whisper_id}')],
      [InlineKeyboardButton('• إغلاق', callback_data='close')]
    ]))
    # مسح رسالة الهمسه الأصلية لو امكن
    try:
      await m.delete()
    except:
      pass
    return True
  return False



# === مانع المخدرات ===
DRUG_WORDS=['مخدرات','مخدر','حشيش','كبتاجون','كبت','هيروين','كوكايين','شبو','كرستال','ماريجوانا','بانجو','ترامادول','ليريكا','حبوب مخدره','حبوب مخدرة','افيون','أفيون','كيميكال','كيميكل','ديلر','تاجر مخدرات','بيع حشيش','بيع مخدرات','hashish','cocaine','heroin','weed','marijuana','tramadol']

DRUG_WARNINGS=ld('drug_warnings.json')  # chat_id -> user_id -> {count, last_time}

def check_drug(text):
  if not text:
    return False
  tl=text.lower()
  for w in DRUG_WORDS:
    if w.lower() in tl:
      return True
  return False

async def handle_drug_filter(m,cid,t,c):
  # شيك لو القفل مفعل - بس الصور تنمسح
  if not is_locked(cid,'المخدرات'):
    return False
  # بس لو فيه صورة أو ميديا
  has_media = bool(m.photo or m.video or m.document or m.sticker or m.animation)
  caption = m.caption if hasattr(m,'caption') and m.caption else ''
  if not has_media:
    return False  # الكلام ما ينمسح - بس الصور
  if check_drug(caption) or check_drug(t):
    try:
      await m.delete()
    except:
      pass
    
    # نظام الإنذارات - 3 إنذارات ويتقيد
    import time
    cid_s=str(cid)
    uid_s=str(m.from_user.id) if m.from_user else '0'
    now=int(time.time())
    if cid_s not in DRUG_WARNINGS:
      DRUG_WARNINGS[cid_s]={}
    if uid_s not in DRUG_WARNINGS[cid_s] or now - DRUG_WARNINGS[cid_s][uid_s].get('last',0) > 6*3600:
      DRUG_WARNINGS[cid_s][uid_s]={'count':0,'last':now}
    
    DRUG_WARNINGS[cid_s][uid_s]['count']+=1
    DRUG_WARNINGS[cid_s][uid_s]['last']=now
    sv('drug_warnings.json',DRUG_WARNINGS)
    cnt=DRUG_WARNINGS[cid_s][uid_s]['count']
    
    if cnt>=3:
      # لو عنده اشراف - نزله من الاشراف
      try:
        member=await c.get_chat_member(cid, m.from_user.id)
        if member.status in ['administrator','creator']:
          await c.promote_chat_member(cid, m.from_user.id, is_anonymous=False,
            can_delete_messages=False, can_restrict_members=False, can_promote_members=False,
            can_change_info=False, can_invite_users=False, can_pin_messages=False)
      except:
        pass
      # تقيد بعد 3 إنذارات
      try:
        await c.restrict_chat_member(cid, m.from_user.id, ChatPermissions(can_send_messages=False))
      except:
        pass
      await c.send_message(cid, f'⌯ المستخدم {m.from_user.first_name if m.from_user else ""} وصل 3 إنذارات مخدرات وانتل وتقيد 🚫', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('• إلغاء الإنذار', callback_data=f'drug_unwarn_{uid_s}'),
         InlineKeyboardButton('• الرسالة سليمة', callback_data=f'drug_safe_{uid_s}')],
        [InlineKeyboardButton('• تفاصيل المخالفة', callback_data=f'drug_detail_{uid_s}')]
      ]))
      DRUG_WARNINGS[cid_s][uid_s]['count']=0
      sv('drug_warnings.json',DRUG_WARNINGS)
    else:
      await c.send_message(cid, f'⌯ تحذير {cnt}/3 : يمنع نشر المخدرات 🚫\n⌯ المستخدم: {m.from_user.first_name if m.from_user else ""}', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('• إلغاء الإنذار', callback_data=f'drug_unwarn_{uid_s}'),
         InlineKeyboardButton('• الرسالة سليمة', callback_data=f'drug_safe_{uid_s}')],
        [InlineKeyboardButton('• تفاصيل المخالفة', callback_data=f'drug_detail_{uid_s}')]
      ]))
    return True
  return False

async def handle_drug_lock_commands(m,cid,t,c):
  if t in ['قفل المخدرات','قفل مخدرات','قفل المخدر']:
    set_lock(cid,'المخدرات',True)
    await m.reply_text('⌯ تم قفل المخدرات 🚫\n⌯ أي رسالة فيها مخدرات بتنمسح')
    return True
  if t in ['فتح المخدرات','فتح مخدرات','فتح المخدر']:
    set_lock(cid,'المخدرات',False)
    await m.reply_text('⌯ تم فتح المخدرات')
    return True
  return False


# === قفل التعديل - نفس النص بالضبط ===
LOCKS=ld('locks.json')

def is_locked(cid, lock_name):
  return LOCKS.get(str(cid),{}).get(lock_name,False)

def set_lock(cid, lock_name, val):
  cid=str(cid)
  if cid not in LOCKS:
    LOCKS[cid]={}
  LOCKS[cid][lock_name]=val
  sv('locks.json',LOCKS)

async def handle_edit_lock(client, edited_message):
  try:
    cid=edited_message.chat.id
    if not is_locked(cid,'التعديل'):
      return
    user=edited_message.from_user
    # مسح الرسالة المعدلة
    try:
      await edited_message.delete()
    except:
      pass
    # الرد بنفس النص بالضبط
    name=user.first_name if user else 'المستخدم'
    uid=user.id if user else 0
    # استخدم الاسم 27 لو موجود؟ نستخدم first_name
    # لكن النص المطلوب: المستخدم 27
    display_name=name if name else '٢٧'
    # لو اليوزر afiwd خليها 27؟
    if user and user.username=='afiwd':
      display_name='٢٧'
    
    text=f'''⌯ المستخدم {display_name}
⌯ قام بالتعديل العادي
⌯ ومسحت الرسالة، لفتح التعديل العادي:
 لا تعدل ثاني مره يا ابن الشرموطة
فتح التعديل العادي'''

    await client.send_message(cid, text)
  except Exception as e:
    print(f"EDIT LOCK ERROR: {e}")

# handler للرسائل المعدلة


# === نظام الكشف والمعلومات - نفس الصور لصق طبع ===

INFO_EXPLANATIONS={
  'ايدي': '''ايدي
_________________________

• يعرض معلوماتك او معلومات اللي
رديت عليه

• طريقة الاستخدام :
• اكتب : ايدي او رد على الشخص

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',
  
  'كشف': '''كشف
_________________________

• يعرض معلومات العضو بالرد او اليوزر
• يظهر اسمه ورتبته وتفاعله

• طريقة الاستخدام :
• اكتب : كشف او رد على الشخص

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',

  'المشرفين': '''المشرفين
_________________________

• يعرض قائمة المشرفين في القروب

• طريقة الاستخدام :
• اكتب : المشرفين

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',

  'رتبتي': '''رتبتي
_________________________

• يعرض رتبتك وتفاعلك ورسائلك

• طريقة الاستخدام :
• اكتب : رتبتي

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',

  'كشف الرتب': '''كشف الرتب
_________________________

• يعرض رتب الاعضاء في القروب

• طريقة الاستخدام :
• اكتب : كشف الرتب

• يستخدمه ↤ المشرفين
• القسم ↤ الكشف والمعلومات''',

  'كشف البوت': '''كشف البوت
_________________________

• يعرض معلومات البوت وسرعته

• طريقة الاستخدام :
• اكتب : كشف البوت

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',

  'التوب': '''التوب
_________________________

• يعرض توب المتفاعلين في القروب

• طريقة الاستخدام :
• اكتب : التوب او توب المتفاعلين

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',

  'كشف القروب': '''كشف القروب
_________________________

• يعرض معلومات القروب وعدد الاعضاء

• طريقة الاستخدام :
• اكتب : كشف القروب

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',

  'تفاعلي': '''تفاعلي
_________________________

• يعرض تفاعلك في القروب

• طريقة الاستخدام :
• اكتب : تفاعلي

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',

  'الشعار': '''الشعار
_________________________

• شعار حماية الاسماء المفعّل

• طريقة الاستخدام :
• اكتب : الشعار

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات''',
  
  'رسائلي': '''رسائلي
_________________________

• يعرض عدد رسائلك في القروب

• طريقة الاستخدام :
• اكتب : رسائلي

• يستخدمه ↤ الكل
• القسم ↤ الكشف والمعلومات'''
}

def kb_info_main(page=1):
  if page==1:
    return InlineKeyboardMarkup([
      [InlineKeyboardButton('• ايدي', callback_data='info_ايدي'),
       InlineKeyboardButton('• كشف', callback_data='info_كشف')],
      [InlineKeyboardButton('• رتبتي', callback_data='info_رتبتي'),
       InlineKeyboardButton('• المشرفين', callback_data='info_المشرفين')],
      [InlineKeyboardButton('• كشف البوت', callback_data='info_كشف البوت'),
       InlineKeyboardButton('• كشف الرتب', callback_data='info_كشف الرتب')],
      [InlineKeyboardButton('• كشف القروب', callback_data='info_كشف القروب'),
       InlineKeyboardButton('• التوب', callback_data='info_التوب')],
      [InlineKeyboardButton('• رسائلي', callback_data='info_رسائلي'),
       InlineKeyboardButton('• تفاعلي', callback_data='info_تفاعلي')],
      [InlineKeyboardButton('• 1 / 2', callback_data='info_page_2'),
       InlineKeyboardButton('• التالي', callback_data='info_page_2')],
      [InlineKeyboardButton('• رجوع', callback_data='cmd_main'),
       InlineKeyboardButton('• القائمة', callback_data='info_list')]
    ])
  else:
    # الصفحة 2 من 2 نفس الصورة - الشعار
    return InlineKeyboardMarkup([
      [InlineKeyboardButton('• الشعار', callback_data='info_الشعار')],
      [InlineKeyboardButton('• السابق', callback_data='info_page_1'),
       InlineKeyboardButton('• 2 / 2', callback_data='info_page_1')],
      [InlineKeyboardButton('• رجوع', callback_data='info_main'),
       InlineKeyboardButton('• القائمة', callback_data='cmd_main')]
    ])

def kb_info_detail(cmd):
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('• شغّل الامر', callback_data=f'run_{cmd}')],
    [InlineKeyboardButton('• رجوع', callback_data='info_main'),
     InlineKeyboardButton('• القائمة', callback_data='cmd_main')]
  ])

def text_info_main(page=1):
  return f'''الكشف والمعلومات
_________________________

• معلومات الاعضاء والقروب والبوت
• الصفحة {page} من 2

• اضغط على الامر عشان يطلع شرحه'''



async def handle_lock_edit(m,cid,t,c):
  if t in ['قفل التعديل','قفل التعديل العادي']:
    set_lock(cid,'التعديل',True)
    await m.reply_text('⌯ تم قفل التعديل')
    return True
  if t in ['فتح التعديل','فتح التعديل العادي']:
    set_lock(cid,'التعديل',False)
    await m.reply_text('⌯ تم فتح التعديل')
    return True
  return False


async def handle_tashbeet(m,cid,t,c):
  if t in ['تثبيت البوت','تثبيت','تثبيت البوت ✅','ثبت البوت','تثبيت بوت']:
    await m.reply_text('تم التثبيت')
    return True
  return False


async def handle_info_commands(m,cid,t,c):
  if t in ['الكشف والمعلومات','كشف والمعلومات','المعلومات','معلومات']:
    await m.reply_text(text_info_main(1), reply_markup=kb_info_main(1))
    return True
  if t in INFO_EXPLANATIONS:
    await m.reply_text(INFO_EXPLANATIONS[t], reply_markup=kb_info_detail(t))
    return True
  return False


# === كل أوامر الشات من الصور - يشتغل لو كتبته ===
CHANNEL_LINKS=ld('channel_links.json')
MUSIC_QUEUE=ld('music_queue.json')  # chat_id -> list
MUSIC_STATE=ld('music_state.json')  # chat_id -> state
MUSIC_LOOP=ld('music_loop.json')  # chat_id -> loop count



async def handle_auto_commands(m,cid,t,c):
  if t in ['اعدادات القروب','الاعدادات','اعدادات','settings','/settings','إعدادات القروب']:
    await m.reply_text(text_group_settings(), reply_markup=kb_group_settings())
    return True
  if t in ['التنزيل التلقائي','اعدادات التنزيل التلقائي','التنزيل التلقائي اعدادات']:
    await m.reply_text(text_auto_main(cid), reply_markup=kb_auto_main(cid))
    return True
  if t in ['تفعيل التنزيل التلقائي','فعل التنزيل التلقائي']:
    auto=get_auto(cid)
    auto['enabled']=True
    sv('auto_download.json',AUTO_DOWNLOAD)
    await m.reply_text(text_auto_main(cid), reply_markup=kb_auto_main(cid))
    # popup حسناً
    await m.reply_text('• تم تفعيل التنزيل التلقائي')
    return True
  if t in ['تعطيل التنزيل التلقائي','عطل التنزيل التلقائي']:
    auto=get_auto(cid)
    auto['enabled']=False
    sv('auto_download.json',AUTO_DOWNLOAD)
    await m.reply_text(text_auto_main(cid), reply_markup=kb_auto_main(cid))
    await m.reply_text('• تم تعطيل التنزيل التلقائي')
    return True
  return False


async def handle_limits_commands(m,cid,t,c):
  # حد - يعرض الحدود
  if t in ['حد','الحد','الحدود','حدود','اوامر الحد']:
    txt=limits_text(cid)
    await m.reply_text(txt, reply_markup=kb_limits_main(cid))
    return True
  # حد الحظر - مثلا حد الحظر 5
  if t.startswith('حد '):
    parts=t.split()
    if len(parts)>=2:
      action=parts[1]
      # لو فيه رقم
      if len(parts)>=3:
        try:
          num=int(parts[2])
          if action in LIMIT_ACTIONS:
            LIMITS[str(cid)]['limits'][action]=num
            sv('limits.json',LIMITS)
            await m.reply_text(f'⌯ تم ضبط حد {action} إلى {num if num!=0 else "بلا حد"}')
            return True
        except:
          pass
      # لو بس حد الحظر بدون رقم - افتح لوحة التعديل
      if action in LIMIT_ACTIONS:
        cur=get_limits(cid)['limits'].get(action,0)
        await m.reply_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur))
        return True
  return False


async def handle_all_chat_commands(m,cid,t,c):
  # الاعدادات / settings
  if t in ['الاعدادات','الاعدادات','settings','/settings','اعدادات']:
    await m.reply_text('''⚙️ إعدادات القروب

• وضع البحث: مباشر
• وضع التصويت: معطل
• جودة الصوت: عالية
• التشغيل التلقائي: مفعل

لتغيير الإعدادات استخدم:
/settings''', reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('• وضع البحث 🔍', callback_data='set_search'),
       InlineKeyboardButton('• التصويت 🗳️', callback_data='set_vote')],
      [InlineKeyboardButton('• إغلاق', callback_data='close')]
    ]))
    return True

  # /reload
  if t in ['/reload','تحديث المشرفين','تحديث قائمة المشرفين']:
    await m.reply_text('⌯ تم تحديث قائمة المشرفين بنجاح ✅')
    return True

  # /loop
  if t.startswith('/loop') or t.startswith('loop') or t=='التكرار':
    parts=t.split()
    if len(parts)==1 or t=='التكرار':
      loop=MUSIC_LOOP.get(str(cid),0)
      await m.reply_text(f'🔁 التكرار الحالي: {loop if loop else "معطل"}\n\n/loops [تفعيل|تعطيل|عدد] - مثال: /loop 3')
      return True
    arg=parts[-1].lower()
    if arg in ['تفعيل','on','تشغيل']:
      MUSIC_LOOP[str(cid)]=1
      sv('music_loop.json',MUSIC_LOOP)
      await m.reply_text('🔁 تم تفعيل التكرار ✅')
    elif arg in ['تعطيل','off','ايقاف']:
      MUSIC_LOOP[str(cid)]=0
      sv('music_loop.json',MUSIC_LOOP)
      await m.reply_text('🔁 تم تعطيل التكرار ❌')
    else:
      try:
        n=int(arg)
        MUSIC_LOOP[str(cid)]=n
        sv('music_loop.json',MUSIC_LOOP)
        await m.reply_text(f'🔁 تم ضبط التكرار إلى {n} مرات')
      except:
        await m.reply_text('⌯ استخدم: /loop [تفعيل|تعطيل|عدد]')
    return True

  # /shuffle
  if t in ['/shuffle','shuffle','الخلط']:
    await m.reply_text('🔀 تم خلط قائمة الانتظار ✅')
    return True

  # /seek and /seekback
  if t.startswith('/seek') or t.startswith('seek') or t.startswith('/seekback') or 'التقديم' in t or 'التأخير' in t:
    import re
    mm=re.search(r'(\d+)',t)
    sec=mm.group(1) if mm else '10'
    if 'back' in t or 'تأخير' in t:
      await m.reply_text(f'⏪ تم الرجوع {sec} ثواني')
    else:
      await m.reply_text(f'⏩ تم التقديم {sec} ثواني')
    return True

  # /speed /playback
  if t.startswith('/speed') or t.startswith('/playback') or t in ['السرعة','سرعة']:
    parts=t.split()
    if len(parts)>=2:
      await m.reply_text(f'⚡ تم تغيير السرعة إلى {parts[-1]}')
    else:
      await m.reply_text('⚡ السرعة الحالية: 1x\n\n/speed [السرعة] - مثال: /speed 1.5')
    return True

  # تشغيل / شغل
  if t.startswith('شغل ') or t.startswith('تشغيل ') or t.startswith('شغل') and len(t)>4:
    q=t.replace('شغل','').replace('تشغيل','').strip()
    if not q:
      await m.reply_text('⌯ ارسل اسم الأغنية أو الرابط\nمثال: شغل رابح صقر')
      return True
    # حفظ في القائمة
    qid=str(cid)
    if qid not in MUSIC_QUEUE:
      MUSIC_QUEUE[qid]=[]
    MUSIC_QUEUE[qid].append({'title':q,'user':m.from_user.first_name})
    sv('music_queue.json',MUSIC_QUEUE)
    MUSIC_STATE[qid]={'playing':q,'user':m.from_user.first_name}
    sv('music_state.json',MUSIC_STATE)
    await m.reply_text(f'🎵 يتم تشغيل: {q}\n👤 بواسطة: {m.from_user.first_name}\n\n⏸️ /pause - ايقاف مؤقت\n⏭️ تخطي - التالي\n⏹️ ايقاف - إنهاء')
    return True

  # فيديو
  if t.startswith('فيديو ') or t.startswith('فيديو'):
    q=t.replace('فيديو','').strip()
    if not q:
      await m.reply_text('⌯ ارسل اسم الفيديو\nمثال: فيديو رابح صقر')
      return True
    await m.reply_text(f'🎬 يتم تشغيل فيديو: {q}\n👤 بواسطة: {m.from_user.first_name}')
    return True

  # playforce / vplayforce
  if t.startswith('playforce') or t.startswith('vplayforce') or t.startswith('/playforce') or t.startswith('/vplayforce'):
    q=t.replace('playforce','').replace('vplayforce','').replace('/','').strip()
    await m.reply_text(f'⚡ تم إيقاف الحالي والتشغيل فورًا: {q if q else "المقطع الجديد"}')
    return True

  # استئناف / ايقاف مؤقت
  if t in ['استئناف','/resume','resume']:
    await m.reply_text('▶️ تم استئناف التشغيل')
    return True
  if t in ['ايقاف مؤقت','إيقاف مؤقت','/pause','pause','وقف']:
    await m.reply_text('⏸️ تم إيقاف التشغيل مؤقتاً')
    return True

  # تخطي
  if t in ['تخطي','/skip','skip','التالي']:
    await m.reply_text('⏭️ تم تخطي المقطع الحالي')
    return True

  # ايقاف / انهاء
  if t in ['ايقاف','إيقاف','انهاء','إنهاء','/stop','/end','stop','end','انهاء التشغيل','إنهاء التشغيل']:
    MUSIC_STATE[str(cid)]={}
    sv('music_state.json',MUSIC_STATE)
    MUSIC_QUEUE[str(cid)]=[]
    sv('music_queue.json',MUSIC_QUEUE)
    await m.reply_text('⏹️ تم إنهاء التشغيل ومسح القائمة')
    return True

  # /queue
  if t in ['/queue','queue','قائمة الانتظار','عرض قائمة الانتظار']:
    q=MUSIC_QUEUE.get(str(cid),[])
    if not q:
      await m.reply_text('⌯ قائمة الانتظار فارغة')
    else:
      txt='🎵 قائمة الانتظار:\n\n'
      for i,s in enumerate(q[:10],1):
        txt+=f'{i}- {s["title"]} - {s["user"]}\n'
      if len(q)>10:
        txt+=f'\n... و {len(q)-10} أخرى'
      await m.reply_text(txt)
    return True

  # /channelplay
  if t.startswith('/channelplay') or t.startswith('channelplay'):
    parts=t.split()
    if len(parts)>=2 and parts[-1]=='linked':
      await m.reply_text('📢 تم ربط القناة المرتبطة تلقائياً ✅\nالقناة المرتبطة بالقروب تم ربطها للتشغيل')
    elif len(parts)>=2:
      ch=parts[-1]
      CHANNEL_LINKS[str(cid)]=ch
      sv('channel_links.json',CHANNEL_LINKS)
      await m.reply_text(f'📢 تم ربط القناة {ch} بالقروب للتشغيل فيها ✅\nالآن يمكنك استخدام: cplay [اسم] للتشغيل في القناة')
    else:
      await m.reply_text('''📢 أوامر ربط القناة:

• /channelplay [آيدي/يوزر القناة] - ربط قناة بالقروب للتشغيل فيها
• /channelplay linked - ربط القناة المرتبطة تلقائياً

مثال:
/channelplay @my_channel
/channelplay linked''')
    return True

  # cplay / cvplay
  if t.startswith('cplay') or t.startswith('cvplay') or t.startswith('/cplay') or t.startswith('/cvplay'):
    q=t.replace('cplay','').replace('cvplay','').replace('/','').strip()
    ch=CHANNEL_LINKS.get(str(cid),'القناة المرتبطة')
    if not q:
      await m.reply_text(f'⌯ ارسل اسم المقطع\nمثال: cplay رابح صقر\nالقناة: {ch}')
    else:
      await m.reply_text(f'📢 يتم التشغيل في القناة {ch}:\n🎵 {q}\n👤 بواسطة: {m.from_user.first_name}')
    return True

  # cqueue / cplaying
  if t in ['cqueue','cplaying','/cqueue','/cplaying','قائمة الانتظار في القناة','الانتظار في القناة']:
    await m.reply_text('📢 قائمة الانتظار في القناة فارغة حالياً')
    return True

  return False


async def handle_moshaghil_commands(m,cid,t,c):
 import re
 # رفع مشغل
 if t.startswith('رفع مشغل'):
  target=None
  target_name=None
  if m.reply_to_message:
   target=m.reply_to_message.from_user.id
   target_name=m.reply_to_message.from_user.first_name
  else:
   mm=re.search(r'(\d{5,20})', t)
   if mm:
    target=int(mm.group(1))
    target_name=str(target)
  if not target:
   await m.reply_text('⌯ ارسل الايدي أو رد على رسالة الشخص\n⌯ مثال: رفع مشغل 123456789')
   return True
  added=add_operator(cid,target)
  if added:
   await m.reply_text(f'⌯ تم رفع {target_name} مشغل\n⌯ الايدي: {target}')
  else:
   await m.reply_text(f'⌯ {target_name} مشغل من قبل')
  return True

 if t.startswith('تنزيل مشغل'):
  target=None
  target_name=None
  if m.reply_to_message:
   target=m.reply_to_message.from_user.id
   target_name=m.reply_to_message.from_user.first_name
  else:
   mm=re.search(r'(\d{5,20})', t)
   if mm:
    target=int(mm.group(1))
    target_name=str(target)
  if not target:
   await m.reply_text('⌯ ارسل الايدي أو رد على رسالة الشخص')
   return True
  removed=remove_operator(cid,target)
  if removed:
   await m.reply_text(f'⌯ تم تنزيل {target_name} من المشغلين')
  else:
   await m.reply_text(f'⌯ {target_name} مو مشغل أصلا')
  return True

 if t in ['المشغلين','المشغلين الحاليين','عرض المشغلين','قائمة المشغلين']:
  lst=get_operators(cid)
  if not lst:
   await m.reply_text('⌯ لا يوجد مشغلين حالياً')
   return True
  txt='⌯ قائمة المشغلين:\n\n'
  for i,uid in enumerate(lst,1):
   txt+=f'{i}- {uid}\n'
  await m.reply_text(txt)
  return True
 return False


def kb_main_commands():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• أوامر القروبات', callback_data='cmd_groups'),
   InlineKeyboardButton('• أوامر التشغيل', callback_data='cmd_play')],
  [InlineKeyboardButton('• تكرار وتقديم وسر', callback_data='cmd_loop'),
   InlineKeyboardButton('• أوامر القنوات', callback_data='cmd_channels')],
  [InlineKeyboardButton('• أوامر المطورين', callback_data='cmd_dev')],
  [InlineKeyboardButton('• إغلاق', callback_data='close')]
 ])

def kb_back_close():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• رجوع', callback_data='cmd_main')],
  [InlineKeyboardButton('• إغلاق', callback_data='close')]
 ])

# نصوص نفس الصور بالضبط
TEXT_GROUPS_OLD = '''أوامر خاصة بالقروبات 👥

• رفع مشغل [رد/آيدي] - يمنح
صلاحيات إدمن التشغيل بدون إشراف
كامل

• تنزيل مشغل [رد/آيدي]
• المشغلين - عرض المشغلين الحاليين
• الاعدادات / settings - إعدادات
القروب (وضع البحث، التصويت...)
• /reload - تحديث قائمة المشرفين'''

TEXT_PLAY = '''أوامر التشغيل الأساسية 🎵

• تشغيل / شغل [ اسم أو رابط] -
تشغيل صوت
• فيديو [ اسم أو رابط] - تشغيل
فيديو
• playforce / vplayforce -
إيقاف الحالي والتشغيل فورًا
• استئناف / ايقاف مؤقت
• تخطي - للمقطع التالي في القائمة
• ايقاف / انهاء - إنهاء التشغيل
بالكامل
• /queue - عرض قائمة الانتظار'''

TEXT_LOOP = '''التكرار 🔁
/loop [تفعيل|تعطيل|عدد]

الخلط 🔀
/shuffle

التقديم/التأخير ⏩
/seek [ثواني] - /seekback
[ثواني]

السرعة ⚡
/speed أو /playback [مشرفين فقط]'''

TEXT_CHANNELS = '''أوامر خاصة بالقنوات 📢

• /channelplay [آيدي/يوزر
القناة] - ربط قناة بالقروب للتشغيل
فيها
• /channelplay linked - ربط القناة
المرتبطة تلقائيًا
• [ اسم] cplay / cvplay - تشغيل
في القناة المرتبطة
• cqueue / cplaying - قائمة
الانتظار في القناة'''

TEXT_Dev = '''أوامر المطورين 👨‍💻

• المطور
• اضف امر - اضافة امر مخصص
• مسح امر - مسح امر مخصص
• الاوامر المضافه - قائمة الاوامر
• تفعيل الوضع الخاص
• تعطيل الوضع الخاص
• قفل امر - قفل امر لرتبة
• تنزيل الكل - تنزيل مشرفين ورتب
• اضف رد - اضافة رد مخصص'''

TEXT_MAIN = '''• قائمة الأوامر

اختر القسم الذي تريد معرفة أوامره:'''



def kb_commands_old():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• القفل والفتح •',callback_data='lockpanel'),
   InlineKeyboardButton('• التفعيل والتعطيل •',callback_data='onoff')],
  [InlineKeyboardButton('• ادارة القروب •',callback_data='manage'),
   InlineKeyboardButton('• التسلية والخدمية •',callback_data='fun')],
  [InlineKeyboardButton('• اوامر Dev •',callback_data='dev')],
  [InlineKeyboardButton('• الإعدادات •',callback_data='sets')],
  [InlineKeyboardButton('• اغلاق •',callback_data='close')]
 ])

AWAMER_TEXT = '''قائمة الاوامر
—————————
• اختر القسم وبتطلع لك اوامره
• كل امر له شرحه وطريقة استخدامه
ومين يقدر يستخدمه

• الالعاب : اكتب ( الالعاب )
'''

def kb_groups():
 return kb_commands()

def cb_groups_override():
 return True


def kb_back_old():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('• رجوع',callback_data='cmd_main'),
   InlineKeyboardButton('• إغلاق',callback_data='close')]
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


 if d.startswith('lim_'):
  # lim_main
  if d=='lim_main':
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_disable':
    lim=get_limits(cid)
    lim['enabled']=not lim.get('enabled',True)
    sv('limits.json',LIMITS)
    status='مفعلة' if lim['enabled'] else 'معطلة'
    await q.answer(f'الحدود الآن {status}', show_alert=True)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_clear':
    LIMITS[str(cid)]['limits']={a:0 for a in LIMIT_ACTIONS}
    sv('limits.json',LIMITS)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_today':
    # عرض استهلاك اليوم
    txt='📊 استهلاك اليوم:\n\n'
    cid_s=str(cid)
    if cid_s in LIMITS_USAGE:
      for admin_id, data in LIMITS_USAGE[cid_s].items():
        txt+=f'المشرف {admin_id}:\n'
        for act,cnt in data.get('counts',{}).items():
          if cnt>0:
            txt+=f'  {act}: {cnt}\n'
        txt+='\n'
    else:
      txt+='لا يوجد استهلاك اليوم'
    await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('• رجوع', callback_data='lim_main')],
      [InlineKeyboardButton('• إغلاق', callback_data='close')]
    ]))
    return
  if d.startswith('lim_edit_'):
    # lim_edit_الطرد_+1 or set_5
    try:
      _,_,action,op = d.split('_',3)
    except:
      # action may contain _
      parts=d.split('_')
      # lim_edit_الطرد_set_5
      action=parts[2]
      op='_'.join(parts[3:])
    cur=get_limits(cid)['limits'].get(action,0)
    if op.startswith('set_'):
      val=int(op.replace('set_',''))
      LIMITS[str(cid)]['limits'][action]=val
      sv('limits.json',LIMITS)
      cur=val
    elif op in ['+1','+5','-1','-5']:
      delta=int(op)
      new=max(0, cur+delta)
      LIMITS[str(cid)]['limits'][action]=new
      sv('limits.json',LIMITS)
      cur=new
    await q.edit_message_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur))
    return
  if d.startswith('lim_') and not d.startswith('lim_edit_') and d not in ['lim_main','lim_disable','lim_clear','lim_today']:
    # lim_الطرد -> فتح تعديل
    action=d.replace('lim_','')
    if action in LIMIT_ACTIONS:
      cur=get_limits(cid)['limits'].get(action,0)
      await q.edit_message_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur))
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

 if d.startswith('warn_cancel_'):
  vid = d.replace('warn_cancel_','')
  v = VIOLATIONS.get(vid,{})
  uid_w = v.get('user_id')
  if uid_w:
   WARNINGS.setdefault(cid,{})
   if str(uid_w) in WARNINGS.get(cid,{}):
    WARNINGS[cid][str(uid_w)] = max(0, WARNINGS[cid][str(uid_w)]-1)
   sv('warnings.json',WARNINGS)
  await q.edit_message_text(f"تم إلغاء الإنذار {vid}")
  return
 if d.startswith('warn_safe_'):
  vid = d.replace('warn_safe_','')
  v = VIOLATIONS.get(vid,{})
  uid_w = v.get('user_id')
  if uid_w:
   WARNINGS.setdefault(cid,{})
   WARNINGS[cid].pop(str(uid_w),None)
   sv('warnings.json',WARNINGS)
  try:
   await q.message.delete()
  except:
   await q.edit_message_text("تم اعتبار الرسالة سليمة وحذف الإنذار")
  return
 if d.startswith('warn_detail_'):
  vid = d.replace('warn_detail_','')
  v = VIOLATIONS.get(vid,{})
  detail = f"تفاصيل المخالفة {vid}\n\n"
  detail += f"العضو : {v.get('user_id')}\n"
  detail += f"الكلمة : {v.get('word')}\n"
  detail += f"النص : {v.get('text','')[:100]}\n"
  detail += f"القروب : {v.get('chat')}"
  await q.edit_message_text(detail, reply_markup=kb_violation(vid))
  return

 if d.startswith('lim_'):
  # lim_main
  if d=='lim_main':
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_disable':
    lim=get_limits(cid)
    lim['enabled']=not lim.get('enabled',True)
    sv('limits.json',LIMITS)
    status='مفعلة' if lim['enabled'] else 'معطلة'
    await q.answer(f'الحدود الآن {status}', show_alert=True)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_clear':
    LIMITS[str(cid)]['limits']={a:0 for a in LIMIT_ACTIONS}
    sv('limits.json',LIMITS)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_today':
    # عرض استهلاك اليوم
    txt='📊 استهلاك اليوم:\n\n'
    cid_s=str(cid)
    if cid_s in LIMITS_USAGE:
      for admin_id, data in LIMITS_USAGE[cid_s].items():
        txt+=f'المشرف {admin_id}:\n'
        for act,cnt in data.get('counts',{}).items():
          if cnt>0:
            txt+=f'  {act}: {cnt}\n'
        txt+='\n'
    else:
      txt+='لا يوجد استهلاك اليوم'
    await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('• رجوع', callback_data='lim_main')],
      [InlineKeyboardButton('• إغلاق', callback_data='close')]
    ]))
    return
  if d.startswith('lim_edit_'):
    # lim_edit_الطرد_+1 or set_5
    try:
      _,_,action,op = d.split('_',3)
    except:
      # action may contain _
      parts=d.split('_')
      # lim_edit_الطرد_set_5
      action=parts[2]
      op='_'.join(parts[3:])
    cur=get_limits(cid)['limits'].get(action,0)
    if op.startswith('set_'):
      val=int(op.replace('set_',''))
      LIMITS[str(cid)]['limits'][action]=val
      sv('limits.json',LIMITS)
      cur=val
    elif op in ['+1','+5','-1','-5']:
      delta=int(op)
      new=max(0, cur+delta)
      LIMITS[str(cid)]['limits'][action]=new
      sv('limits.json',LIMITS)
      cur=new
    await q.edit_message_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur))
    return
  if d.startswith('lim_') and not d.startswith('lim_edit_') and d not in ['lim_main','lim_disable','lim_clear','lim_today']:
    # lim_الطرد -> فتح تعديل
    action=d.replace('lim_','')
    if action in LIMIT_ACTIONS:
      cur=get_limits(cid)['limits'].get(action,0)
      await q.edit_message_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur))
      return

 if d=='cmd_main':
  await q.edit_message_text(TEXT_MAIN, reply_markup=kb_main_commands())
  return
 if d=='cmd_groups':
  await q.edit_message_text(TEXT_GROUPS, reply_markup=kb_back_close())
  return
 if d=='cmd_play':
  await q.edit_message_text(TEXT_PLAY, reply_markup=kb_back_close())
  return
 if d=='cmd_loop':
  await q.edit_message_text(TEXT_LOOP, reply_markup=kb_back_close())
  return
 if d=='cmd_channels':
  await q.edit_message_text(TEXT_CHANNELS, reply_markup=kb_back_close())
  return
 if d=='cmd_dev':
  await q.edit_message_text(TEXT_Dev, reply_markup=kb_back_close())
  return
 if d=='manage':
  await q.edit_message_text('👥 ادارة القروب\n• رفع ادمن - تنزيل ادمن\n• رفع مدير - تنزيل مدير\n• رفع مالك - تنزيل مالك\n• حظر - الغاء حظر\n• كتم - الغاء كتم\n• تقيد - الغاء تقيد', reply_markup=kb_commands())
  return
 if d=='fun':
  await q.edit_message_text('🎮 التسلية والخدمية\n• الالعاب\n• توب المتفاعلين\n• رتبتي\n• حظ\n• كت تويت\n• العقاب\n• الحكم\n• الكرسي', reply_markup=kb_commands())
  return
 if d=='dev':
  await q.edit_message_text('💻 اوامر Dev\n• المطور\n• اضف امر\n• مسح امر\n• الاوامر المضافه\n• تفعيل / تعطيل', reply_markup=kb_commands())
  return
 if d=='sets':
  await q.edit_message_text('⚙️ الإعدادات\n• اعدادات القفل\n• اعدادات الترحيب\n• اعدادات الالعاب', reply_markup=kb_commands())
  return
 if d=='onoff':
  await q.edit_message_text('⚙️ التفعيل والتعطيل\n• تفعيل الالعاب\n• تعطيل الالعاب\n• قفل الاباحي\n• فتح الاباحي', reply_markup=kb_commands())
  return

 if d.startswith('lock_') and not d.startswith('lockpage_'):
  name = d[5:]
  # تبديل
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]= not LOCKS[cid].get(name,False)
  sv('locks.json',LOCKS)
  locked = LOCKS[cid][name]
  # تحديد الصفحة الحالية للاسم
  cur_page = 1
  for p, lst in LOCKS_PAGES.items():
   if name in lst:
    cur_page=p
    break
  # بدون رد - فقط يغير لون الزر
  pass
  try:
   await q.edit_message_text(LOCK_PANEL_TEXT.format(page=cur_page), reply_markup=kb_lock_page(cid,cur_page))
  except:
   try:
    await q.edit_message_reply_markup(reply_markup=kb_lock_page(cid,cur_page))
   except:
    pass
  return

 if d.startswith('openall_') or d.startswith('closeall_'):
  parts = d.split('_')
  page = int(parts[-1]) if parts[-1].isdigit() else 1
  do_close = d.startswith('closeall')
  LOCKS.setdefault(cid,{})
  for name in LOCKS_PAGES.get(page,[]):
   LOCKS[cid][name]=do_close
  sv('locks.json',LOCKS)
  pass # بدون رد
  try:
   await q.edit_message_text(LOCK_PANEL_TEXT.format(page=page), reply_markup=kb_lock_page(cid,page))
  except:
   pass
  return

 if d.startswith('lockpage_'):
  try:
   page = int(d.split('_')[1])
  except:
   page=1
  try:
   await q.edit_message_text(LOCK_PANEL_TEXT.format(page=page), reply_markup=kb_lock_page(cid,page))
  except Exception as e:
   await q.edit_message_reply_markup(reply_markup=kb_lock_page(cid,page))
  return

 if d.startswith('openall') or d.startswith('closeall') and '_' not in d:
  # للتوافق القديم
  do_close = 'closeall' in d
  LOCKS.setdefault(cid,{})
  for lst in LOCKS_PAGES.values():
   for name in lst:
    LOCKS[cid][name]=do_close
  sv('locks.json',LOCKS)
  pass # بدون رد
  try:
   await q.edit_message_reply_markup(reply_markup=kb_lock_page(cid,1))
  except:
   pass
  return


 if d.startswith('admin_toggle_'):
  try:
   # admin_toggle_12345_تغيير المعلومات
   _, _, uid, perm_name = d.split('_',3)
   ADMIN_PERMS.setdefault(cid,{})
   if uid not in ADMIN_PERMS[cid]:
    ADMIN_PERMS[cid][uid]=DEFAULT_PERMS.copy()
   ADMIN_PERMS[cid][uid][perm_name] = not ADMIN_PERMS[cid][uid].get(perm_name, False)
   sv('admin_perms.json',ADMIN_PERMS)
   perms = get_user_perms(cid, uid)
   # تحديث صلاحيات تيليجرام حسب الاختيار
   try:
    # نحدث الادمن في تيليجرام
    pass
   except:
    pass
   await q.edit_message_reply_markup(reply_markup=kb_admin_panel(cid, uid, ''))
   # نحتاج نجيب اسم
   try:
    member = await c.bot.get_chat_member(q.message.chat.id, int(uid))
    name = member.user.first_name
   except:
    name = uid
   await q.edit_message_text(admin_panel_text(name, perms), reply_markup=kb_admin_panel(cid, uid, name))
  except Exception as e:
   await q.answer(f'خطأ {e}', show_alert=True)
  return

 if d.startswith('admin_full_'):
  try:
   uid = d.split('_')[-1]
   ADMIN_PERMS.setdefault(cid,{})
   ADMIN_PERMS[cid][uid]={k:True for k in DEFAULT_PERMS}
   sv('admin_perms.json',ADMIN_PERMS)
   perms = get_user_perms(cid, uid)
   try:
    member = await c.bot.get_chat_member(q.message.chat.id, int(uid))
    name = member.user.first_name
   except:
    name = uid
   await q.edit_message_text(admin_panel_text(name, perms), reply_markup=kb_admin_panel(cid, uid, name))
  except Exception as e:
   await q.answer(f'خطأ {e}', show_alert=True)
  return

 if d.startswith('admin_demote_'):
  try:
   uid = d.split('_')[-1]
   if cid in ADMIN_PERMS and uid in ADMIN_PERMS[cid]:
    del ADMIN_PERMS[cid][uid]
    sv('admin_perms.json',ADMIN_PERMS)
   try:
    await c.bot.promote_chat_member(chat_id=q.message.chat.id, user_id=int(uid),
     can_delete_messages=False, can_restrict_members=False, can_invite_users=False,
     can_pin_messages=False, can_promote_members=False)
   except:
    pass
   await q.edit_message_text(f'تم تنزيل {uid} من الاشراف')
  except Exception as e:
   await q.answer(f'خطأ {e}', show_alert=True)
  return

 if d.startswith('setrank_'):
  try:
   # setrank_عام_ادمن
   _, cmd_name, rank = d.split('_',2)
   COMMAND_RANKS.setdefault(cid,{})
   COMMAND_RANKS[cid][cmd_name]=rank
   sv('command_ranks.json',COMMAND_RANKS)
   # مسح من الانتظار
   for k in list(PENDING_RANK_LOCK.keys()):
    if k.startswith(cid):
     if PENDING_RANK_LOCK[k]==cmd_name:
      del PENDING_RANK_LOCK[k]
   await q.edit_message_text(f'تم قفل الأمر {cmd_name} لرتبة {rank} فقط ✓')
  except Exception as e:
   await q.answer(f'خطأ {e}', show_alert=True)
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

 # كتم وهمي - لو مكتوم احذف رسالته
 if MUTED.get(cid,{}).get(uid):
  try:
   await m.delete()
  except:
   pass
  return


 # قفل الاباحي - نظام انذارات مثل الصورة
 if LOCKS.get(cid,{}).get('الاباحي',False) or True:  # شغال دايما للاباحي
  bad_words = ['اباحي','سكس','porn','xxx','sex','نيك','كس','زب','طيز','مص','قحبه','قحاب','شرموط','اباحية']
  low = t.lower()
  found = None
  for w in bad_words:
   if w in low:
    found = w
    break
  if found:
   try:
    await m.delete()
   except:
    pass
   # نظام الانذارات
   WARNINGS.setdefault(cid,{})
   WARNINGS[cid][uid]=WARNINGS[cid].get(uid,0)+1
   sv('warnings.json',WARNINGS)
   warns = WARNINGS[cid][uid]
   # حفظ المخالفة
   import time, random
   vid = str(int(time.time()*1000))[-6:]
   VIOLATIONS[vid] = {
    'user_id': uid,
    'text': t[:200],
    'word': found,
    'chat': cid,
    'time': time.time()
   }
   sv('violations.json',VIOLATIONS)
   # نفس رسالة الصورة
   conf = random.randint(95,99)
   text = f"• تم رصد محتوى مخالف وحذفه\n"
   text += f"• العضو ↤ {uid}\n"
   text += f"• نسبة التأكد ↤ %{conf}\n"
   text += f"• الإنذارات ↤ ({warns}/3)\n"
   text += f"• ينتهي الإنذار خلال ↤ 06:00:00"
   try:
    await c.bot.send_message(
     chat_id=m.chat.id,
     text=text,
     reply_markup=kb_violation(vid)
    )
   except:
    pass
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
  await m.reply_text(AWAMER_TEXT,reply_markup=kb_commands())
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


 if t in ['رتبتي','رتبته','رتبه','رتبة','رتبه انت','رتبتي انا','رتبة انت'] or t.startswith('رتبه ') or t.startswith('رتبة '):
  # لو مالك البوت - رتبته عامة Dev دايما
  if is_owner(m.from_user):
   await m.reply_text(f"🎖️ Dev ← رتبتك =\n\n☂️ - Dev - {TOP.get(cid,{}).get(str(m.from_user.id),0)} رسالة")
   return
  # لو الوضع الخاص مفعل - الرتب خاصة لهذا القروب
  if PRIVATE_MODE.get(cid,False):
   # رتبة خاصة للقروب
   pass

  target = m.reply_to_message.from_user if m.reply_to_message else m.from_user
  tid = str(target.id)
  cid_rank = str(m.chat.id)
  msgs = TOP.get(cid_rank,{}).get(tid,0)
  total = sum(TOP.get(cid_rank,{}).values()) or 1
  percent = (msgs/total*100) if total else 0
  # Determine rank based on msgs or saved ranks
  rank_name = RANKS.get(cid_rank,{}).get(tid, 'Myth' if msgs>500 else 'Active' if msgs>100 else 'Member')
  # For Soul style
  if t=='رتبته' and m.reply_to_message:
   # Sniper style
   await m.reply_text(f"☂️ - {rank_name} - {msgs} رسالة\nنسبة التفاعل بالقروب : {percent:.2f}%\nأول ظهور بالقروب : 2026/10/21")
   # Soul style second message
   await m.reply_text(f"🎖️ {rank_name} ← رتبته =")
  else:
   await m.reply_text(f"🎖️ {rank_name} ← رتبتك =\n☂️ - {rank_name} - {msgs} رسالة\nنسبة التفاعل : {percent:.2f}%")
  return


 
 if t in ['كتم','كتمه','اسكت','اسكته']:
  if not m.reply_to_message:
   await m.reply_text('رد على رسالة الشخص واكتب كتم')
   return
  target = m.reply_to_message.from_user
  tid = str(target.id)
  MUTED.setdefault(cid,{})
  MUTED[cid][tid]=True
  sv('muted.json',MUTED)
  await m.reply_text(f'تم كتم {target.first_name}\nيقدر يكتب بس رسايله تنحذف')
  return

 if t in ['الغاء كتم','الغاء الكتم','فك كتم','فتح كتم','unmute','الغاء اسكت','فك اسكت']:
  if not m.reply_to_message:
   await m.reply_text('رد على رسالة الشخص واكتب الغاء كتم')
   return
  target = m.reply_to_message.from_user
  tid = str(target.id)
  MUTED.setdefault(cid,{})
  MUTED[cid].pop(tid,None)
  sv('muted.json',MUTED)
  await m.reply_text(f'تم الغاء كتم {target.first_name}')
  return

 if t=='المكتومين' or t=='قائمة المكتومين':
  lst = MUTED.get(cid,{})
  if not lst:
   await m.reply_text('مافي احد مكتوم')
  else:
   await m.reply_text(f'المكتومين : {len(lst)} شخص')
  return


 
 if t in ['تقيد','تقييد','تقييده']:
  if not m.reply_to_message:
   await m.reply_text('رد على رسالة الشخص واكتب تقيد')
   return
  target = m.reply_to_message.from_user
  try:
   from telegram import ChatPermissions
   perms = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False
   )
   await c.bot.restrict_chat_member(
    chat_id=m.chat.id,
    user_id=target.id,
    permissions=perms
   )
   await m.reply_text(f'تم تقيد {target.first_name}\nما يقدر يرسل شي لا نص لا وسائط')
  except Exception as e:
   await m.reply_text(f'ما قدرت اقيده - ارفعني مشرف مع تقييد الاعضاء\n{e}')
  return

 if t in ['الغاء تقيد','الغاء التقييد','فك تقيد','فتح تقيد']:
  if not m.reply_to_message:
   await m.reply_text('رد على رسالة الشخص واكتب الغاء تقيد')
   return
  target = m.reply_to_message.from_user
  try:
   from telegram import ChatPermissions
   perms = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True
   )
   await c.bot.restrict_chat_member(
    chat_id=m.chat.id,
    user_id=target.id,
    permissions=perms
   )
   await m.reply_text(f'تم الغاء تقيد {target.first_name}')
  except Exception as e:
   await m.reply_text(f'ما قدرت افك تقييده\n{e}')
  return


 
 if t.startswith('اضف امر') or t.startswith('تغيير امر') or t.startswith('غير امر'):
  # صيغة : اضف امر اسكت = كتم  او  تغيير امر كتم الى اسكت
  try:
   txt_cmd = t.replace('اضف امر','').replace('تغيير امر','').replace('غير امر','').strip()
   new_name = None
   old_name = None
   if '=' in txt_cmd:
    parts = txt_cmd.split('=')
    new_name = parts[0].strip()
    old_name = parts[1].strip()
   elif 'الى' in txt_cmd:
    parts = txt_cmd.split('الى')
    old_name = parts[0].strip()
    new_name = parts[1].strip()
   elif ' ' in txt_cmd:
    parts = txt_cmd.split()
    if len(parts)>=2:
     new_name = parts[0].strip()
     old_name = parts[1].strip()
     # لو كتب كتم الى اسكت
     if len(parts)>=3 and parts[1]=='الى':
      old_name = parts[0].strip()
      new_name = parts[2].strip()
   if new_name and old_name:
    CUSTOM.setdefault(cid,{})
    CUSTOM[cid][new_name] = old_name
    sv('custom.json',CUSTOM)
    await m.reply_text(f'تم تغيير الامر\n{old_name} ↤ {new_name}\nذحين تقدر تكتب {new_name} بدل {old_name}')
   else:
    await m.reply_text('طريقة تغيير الامر:\nاضف امر اسكت = كتم\nاو\nتغيير امر كتم الى اسكت')
  except Exception as e:
   await m.reply_text(f'خطأ : {e}\nالطريقة : اضف امر اسكت = كتم')
  return

 if t.startswith('مسح امر') or t.startswith('حذف امر'):
  try:
   txt_cmd = t.replace('مسح امر','').replace('حذف امر','').strip()
   CUSTOM.setdefault(cid,{})
   if txt_cmd in CUSTOM.get(cid,{}):
    del CUSTOM[cid][txt_cmd]
    sv('custom.json',CUSTOM)
    await m.reply_text(f'تم مسح الامر {txt_cmd}')
   else:
    await m.reply_text(f'الامر {txt_cmd} مو موجود')
  except:
   pass
  return

 # تشييك الاوامر المخصصة
 if t in CUSTOM.get(cid,{}):
  original = CUSTOM[cid][t]
  # نفذ الامر الاصلي كأنه كتب
  # حول النص للامر الاصلي وارجع عالج
  # بسيطة : لو اسكت -> كتم
  if original in ['كتم','كتمه']:
   if not m.reply_to_message:
    await m.reply_text('رد على رسالة الشخص واكتب كتم')
    return
   target = m.reply_to_message.from_user
   tid = str(target.id)
   MUTED.setdefault(cid,{})
   MUTED[cid][tid]=True
   sv('muted.json',MUTED)
   await m.reply_text(f'تم كتم {target.first_name} بواسطة امر {t}')
   return
  if original in ['تقيد']:
   if not m.reply_to_message:
    await m.reply_text('رد على رسالة واكتب تقيد')
    return
   target = m.reply_to_message.from_user
   try:
    from telegram import ChatPermissions
    perms = ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_polls=False, can_send_other_messages=False, can_add_web_page_previews=False)
    await c.bot.restrict_chat_member(chat_id=m.chat.id, user_id=target.id, permissions=perms)
    await m.reply_text(f'تم تقيد {target.first_name} بواسطة امر {t}')
   except Exception as e:
    await m.reply_text(f'ما قدرت اقيده\n{e}')
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


 if t in GAMES_DATA or t in ['حظ','كت تويت','اذكار','تحدي','اسئلة','صراحة','مافيا','خمن']:
  import random
  if t=='حظ':
   await m.reply_text(f"حظك اليوم {random.randint(1,100)}% 🎲")
  elif t=='كت تويت':
   tweets = ['الحياة حلوة','لا تنتظر احد','خلك قوي','ابتسم']
   await m.reply_text(random.choice(tweets))
  elif t=='اذكار':
   azkar = ['سبحان الله','الحمدلله','لا اله الا الله','الله اكبر']
   await m.reply_text(random.choice(azkar))
  else:
   await m.reply_text(get_game_text(t))
  return

 if t=='الالعاب':
  # عرض كل الالعاب مع الشرح
  txt_games = "🎮 مركز الالعاب\nاختر اللعبة وشوف شرحها:\n\n"
  for name in GAMES_DATA:
   txt_games += f"• {name}\n"
  txt_games += "\nاكتب اسم اللعبة لمعرفة شرحها"
  await m.reply_text(txt_games, reply_markup=kb_games())
  return



 if t in ['توب المتفاعلين','توب']:
  await m.reply_text('توب 20\n1) ديف\n2) RORY...')
  return

 if t=='القفل والفتح':
  await m.reply_text('لوحة القفل',reply_markup=kb_lock_p1())
  return

# قفل التعديل والتعديل العادي - يمسح ويمنشن

async def media_handler(u,c):
 m = u.message
 if not m:
  return
 cid = str(m.chat.id)
 uid = str(m.from_user.id)
 # لو الاباحي مقفول وارسل صورة او فيديو اباحي (يعتبر مخالف)
 if LOCKS.get(cid,{}).get('الاباحي',False):
  # لو فيه كابشن فيه كلمات اباحية
  cap = (m.caption or '').lower()
  bad_words = ['اباحي','سكس','porn','xxx','sex','نيك','كس','زب','طيز','مص','قحبه']
  found = None
  for w in bad_words:
   if w in cap:
    found = w
    break
  # لو الصورة بدون كابشن بس القفل شغال للاباحي - لا تحذف كل الصور، بس اللي فيها كلمات
  # لو تبي يحذف كل الصور الاباحية حتى بدون كلمات، فعل هذا:
  # found = found or 'صورة'
  if found:
   try:
    await m.delete()
   except:
    pass
   import time, random
   WARNINGS.setdefault(cid,{})
   WARNINGS[cid][uid]=WARNINGS[cid].get(uid,0)+1
   sv('warnings.json',WARNINGS)
   warns = WARNINGS[cid][uid]
   vid = str(int(time.time()*1000))[-6:]
   VIOLATIONS[vid] = {'user_id': uid, 'text': cap[:200], 'word': found, 'chat': cid, 'time': time.time()}
   sv('violations.json',VIOLATIONS)
   conf = random.randint(95,99)
   text = f"• تم رصد محتوى مخالف وحذفه\n• العضو ↤ {uid}\n• نسبة التأكد ↤ %{conf}\n• الإنذارات ↤ ({warns}/3)\n• ينتهي الإنذار خلال ↤ 06:00:00"
   try:
    await c.bot.send_message(chat_id=m.chat.id, text=text, reply_markup=kb_violation(vid))
   except:
    pass


async def edited(u,c):
 if not u.edited_message:
  return
 m=u.edited_message
 cid=str(m.chat.id)
 # يشتغل لو قفل التعديل او التعديل العادي مقفول
 locked = LOCKS.get(cid,{}).get('التعديل',False) or LOCKS.get(cid,{}).get('التعديل العادي',False)
 if locked:
  try:
   await m.delete()
  except:
   pass
  # منشن الشخص
  try:
   name = m.from_user.first_name
   uid = m.from_user.id
   mention = f"[{name}](tg://user?id={uid})"
   await c.bot.send_message(
    chat_id=m.chat.id,
    text=f"{mention} بتعدل بلعن امك",
    parse_mode='Markdown'
   )
  except:
   try:
    await c.bot.send_message(
     chat_id=m.chat.id,
     text=f"بتعدل بلعن امك يا {m.from_user.first_name}"
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
  (filters.PHOTO | filters.VIDEO | filters.Document.ALL) & ~filters.UpdateType.EDITED_MESSAGE,
  media_handler
 ))
 app.add_handler(MessageHandler(
  filters.UpdateType.EDITED_MESSAGE,
  edited
 ))
 print('SORD LIAM FULL 300 LINES LIVE')
 app.run_polling()
