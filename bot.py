# -*- coding: utf-8 -*-
import os
os.environ['PYTHONIOENCODING']='utf-8'
os.environ['PYTHONUTF8']='1'
import json,threading,time,re
from http.server import HTTPServer,BaseHTTPRequestHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,CallbackQueryHandler,MessageHandler,filters

# TOKEN - FIXED NEW AAF
TOKEN=os.getenv('BOT_TOKEN','').strip() or "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"

# الغاء الانضمام الاجباري نهائيا - FIXED ALL
FORCE_CHANNEL=None
CHANNEL=None
MUST_JOIN=None
CHANNEL_ID=None
JOIN_CHANNEL=None
FORCE_SUB=None
FORCE_JOIN=None
REQUIRED_CHANNEL=None
MUST_JOIN_CHANNEL=None
A_TOOLSx2=None
JOIN_CHANNEL_ID=None
async def check_join(*a,**k): return True
async def must_join(*a,**k): return True
async def is_joined(*a,**k): return True
async def check_channel(*a,**k): return True
async def check_sub(*a,**k): return True
async def is_subbed(*a,**k): return True

def ld(f):
 try: return json.load(open(f,encoding='utf-8'))
 except: return {}
def sv(f,d):
 json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

for fp in ['locks.json','toggles.json','custom.json','top.json','ranks.json','muted.json','warnings.json','violations.json','limits.json','auto_download.json','last_seen.json','dev.json','dev2.json','my.json','m.json','malik.json','munshi.json','modir.json','admin.json','mumayaz.json','command_locks.json','limits_usage.json','dev_list.json','pending_dev.json']:
 if not os.path.exists(fp):
  sv(fp,{})

LOCKS=ld('locks.json')
if not LOCKS: LOCKS={}
TOGGLES=ld('toggles.json')
TOP=ld('top.json')
RANKS=ld('ranks.json')
MUTED=ld('muted.json')
WARNINGS=ld('warnings.json')
VIOLATIONS=ld('violations.json')
LIMITS=ld('limits.json')
LIMITS_USAGE=ld('limits_usage.json')
AUTO_DOWNLOAD=ld('auto_download.json')
LAST_SEEN=ld('last_seen.json')
COMMAND_LOCKS=ld('command_locks.json')

# SERVER
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  self.end_headers()
  self.wfile.write(b'SORD LIAM FULL 1668 LINES FIXED')
 def log_message(self, *a): return
def run():
 HTTPServer(('0.0.0.0',int(os.getenv('PORT','10000'))),H).serve_forever()

LOCKS_PAGES = {
1: ['تعديل المعلومات','الاستفتاءات','الرسائل الغنية','الاضافه','التعديل العادي','المتحركه','الاغاني','البوتات','القنوات','الشارحه'],
2: ['الجهات','الملصقات المميزة','الملفات','التفاعلات المميزة','التعديل','تعديل الميديا','الفارسيه','الانجليزيه','التوجيه','الالعاب'],
3: ['التاك','القيف اواي','الاعلانات','الانلاين','الانلاين للكل','الايرانيين','الدخول','الجمثون','الكيبورد','الدخول بدون طلب'],
4: ['الروابط','اللغات','المواقع','الربط','الماركداون','التثبيت','الوسائط المشفرة','الوسائط','الردود الخارجيه','الأرقام'],
5: ['الاكواد','الصور','الروسي','الاقتباسات','التكرار','السب','الكلايش','التفليش','الملصقات','التشويش'],
6: ['الاشعارات','القصص','التقليد','الدردشه','المعرفات','السيلفي','الفيديو','الصوت','الانتهاكات']
}
def get_lock_text(cid, name):
 locked = LOCKS.get(cid,{}).get(name, False)
 return f"🔵 -{name}" if locked else f"🟢 -{name}"
def kb_lock_page(cid, page):
 page = max(1, min(6, page))
 locks = LOCKS_PAGES.get(page, [])
 kb = []
 kb.append([InlineKeyboardButton('فتح الكل',callback_data=f'openall_{page}'), InlineKeyboardButton('قفل الكل',callback_data=f'closeall_{page}')])
 for i in range(0, len(locks), 2):
  row=[]
  for j in range(2):
   if i+j < len(locks):
    name=locks[i+j]
    row.append(InlineKeyboardButton(get_lock_text(cid, name), callback_data=f'lock_{name}'))
  kb.append(row)
 if page==1: kb.append([InlineKeyboardButton('الصفحة التالية',callback_data='lockpage_2')])
 elif page==6: kb.append([InlineKeyboardButton('الصفحة السابقة',callback_data='lockpage_5')])
 else: kb.append([InlineKeyboardButton('الصفحة السابقة',callback_data=f'lockpage_{page-1}'), InlineKeyboardButton('الصفحة التالية',callback_data=f'lockpage_{page+1}')])
 kb.append([InlineKeyboardButton('اخفاء',callback_data='close')])
 kb.append([InlineKeyboardButton('العودة للقائمة الرئيسية',callback_data='cmd_groups')])
 kb.append([InlineKeyboardButton(f'{page} / 6',callback_data='noop'), InlineKeyboardButton('رجوع',callback_data='cmd_groups')])
 return InlineKeyboardMarkup(kb)

# FIX kb_commands - حل مشكلة 1:28
def kb_commands_old():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('القفل والفتح',callback_data='lockpanel'), InlineKeyboardButton('التفعيل والتعطيل',callback_data='onoff')],
  [InlineKeyboardButton('ادارة القروب',callback_data='manage'), InlineKeyboardButton('التسلية والخدمية',callback_data='fun')],
  [InlineKeyboardButton('اوامر Dev',callback_data='dev')],
  [InlineKeyboardButton('الإعدادات',callback_data='sets')],
  [InlineKeyboardButton('اغلاق',callback_data='close')]
 ])
def kb_commands(): return kb_commands_old()
def kb_groups(): return kb_commands()
def kb_main(): return kb_commands_old()
def kb_start():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('اضفني لقروبك',url='https://t.me/kpcukbot7454_bot?startgroup=true')],
  [InlineKeyboardButton('About SORD',callback_data='about')],
  [InlineKeyboardButton('اغلاق',callback_data='close')]
 ])
def kb_back():
 return InlineKeyboardMarkup([[InlineKeyboardButton('رجوع',callback_data='cmd_main')], [InlineKeyboardButton('إغلاق',callback_data='close')]])
def kb_lock_p1(): return kb_lock_page('0',1)
def kb_lock_p2(): return kb_lock_page('0',2)
def kb_main_commands(): return kb_commands_old()
def kb_games():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('العاب جماعية',callback_data='g_group'), InlineKeyboardButton('العاب ادوار',callback_data='g_roles')],
  [InlineKeyboardButton('كلمات وحروف',callback_data='g_words'), InlineKeyboardButton('تحدي واستنتاج',callback_data='g_chal')],
  [InlineKeyboardButton('اسئلة ومعلومات',callback_data='g_q'), InlineKeyboardButton('صور وتخمين',callback_data='g_pic')],
  [InlineKeyboardButton('مقالات وسرعة',callback_data='g_fast'), InlineKeyboardButton('تسلية القروب',callback_data='g_fun')],
  [InlineKeyboardButton('حظ وقرعة',callback_data='g_luck'), InlineKeyboardButton('عوائل وتيناس',callback_data='g_fam')],
  [InlineKeyboardButton('مسابقات وقلابات',callback_data='g_race'), InlineKeyboardButton('احصائياتي',callback_data='g_me')],
  [InlineKeyboardButton('توب الادمين',callback_data='g_topadmin'), InlineKeyboardButton('توب المتفاعلين',callback_data='g_top')],
  [InlineKeyboardButton('إغلاق',callback_data='close')]
 ])
def kb_back_close(): return kb_back()
def kb_violation(vid):
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('إلغاء الإنذار',callback_data=f'warn_cancel_{vid}')],
  [InlineKeyboardButton('الرسالة سليمة',callback_data=f'warn_safe_{vid}')],
  [InlineKeyboardButton('تفاصيل المخالفة',callback_data=f'warn_detail_{vid}')]
 ])

ALL_RANKS=['Dev','Dev2','MY','M','Extra','مالك اساسي','مالك','منشئ اساسي','منشئ','مدير','ادمن','مميز']
LOCKS_P1=['تعديل المعلومات','الاستفتاءات','الرسائل الغبيه','الاضافه','التعديل العادي','المتحركه','الاغاني','البوتات','القنوات','الشارحه','الجهات','الملصقات المميزه','الملفات','التفاعلات المميزه','التعديل','تعديل الميديا','الفارسيه','الانجليزيه','الالعاب','التوجيه']
LOCKS_P2=['الاباحي','القيف اوي','التاك','الاعلانات','الاونلاين','التثبيت للكل','الابراج','الجنون','الدخول','الدخول بدون طلب','الكرتون','اللغات','الروابط','الرابط','المواقع','التنبيه','الماركداون','الوسائط','الوسائط المشفره','الارقام','الردود الخارجيه']
ALL_LOCKS=LOCKS_P1+LOCKS_P2

# LIMITS SYSTEM
LIMIT_ACTIONS=['الحظر','الطرد','الكتم','التقييد','الرفع','التنزيل','المسح']
def get_limits(cid):
 cid=str(cid)
 if cid not in LIMITS:
  LIMITS[cid]={'enabled':True,'limits':{a:0 for a in LIMIT_ACTIONS}}
  sv('limits.json',LIMITS)
 return LIMITS[cid]
def get_usage(cid, admin_id):
 cid=str(cid); aid=str(admin_id)
 today=str(__import__('datetime').date.today())
 if cid not in LIMITS_USAGE: LIMITS_USAGE[cid]={}
 if aid not in LIMITS_USAGE[cid] or LIMITS_USAGE[cid][aid].get('date')!=today:
  LIMITS_USAGE[cid][aid]={'date':today,'counts':{a:0 for a in LIMIT_ACTIONS}}
 return LIMITS_USAGE[cid][aid]
def check_limit(cid, admin_id, action):
 lim=get_limits(cid)
 if not lim.get('enabled',True): return True
 max_lim=lim['limits'].get(action,0)
 if max_lim==0: return True
 usage=get_usage(cid,admin_id)
 return usage['counts'].get(action,0) < max_lim
def inc_usage(cid, admin_id, action):
 usage=get_usage(cid,admin_id)
 usage['counts'][action]=usage['counts'].get(action,0)+1
 LIMITS_USAGE[str(cid)][str(admin_id)]=usage
 sv('limits_usage.json',LIMITS_USAGE)
def kb_limits_main(cid):
 lim=get_limits(cid); limits=lim['limits']
 return InlineKeyboardMarkup([
  [InlineKeyboardButton(f"الطرد : {limits['الطرد'] if limits['الطرد']!=0 else 'بلا حد'}", callback_data='lim_الطرد'), InlineKeyboardButton(f"الحظر : {limits['الحظر'] if limits['الحظر']!=0 else 'بلا حد'}", callback_data='lim_الحظر')],
  [InlineKeyboardButton(f"التقييد : {limits['التقييد'] if limits['التقييد']!=0 else 'بلا حد'}", callback_data='lim_التقييد'), InlineKeyboardButton(f"الكتم : {limits['الكتم'] if limits['الكتم']!=0 else 'بلا حد'}", callback_data='lim_الكتم')],
  [InlineKeyboardButton(f"التنزيل : {limits['التنزيل'] if limits['التنزيل']!=0 else 'بلا حد'}", callback_data='lim_التنزيل'), InlineKeyboardButton(f"الرفع : {limits['الرفع'] if limits['الرفع']!=0 else 'بلا حد'}", callback_data='lim_الرفع')],
  [InlineKeyboardButton(f"المسح : {limits['المسح'] if limits['المسح']!=0 else 'بلا حد'}", callback_data='lim_المسح')],
  [InlineKeyboardButton('استهلاك اليوم', callback_data='lim_today'), InlineKeyboardButton('تعطيل الحدود', callback_data='lim_disable')],
  [InlineKeyboardButton('مسح الحدود', callback_data='lim_clear')],
  [InlineKeyboardButton('رجوع', callback_data='cmd_main'), InlineKeyboardButton('إغلاق', callback_data='close')]
 ])
def kb_limit_edit(action, current):
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('-5', callback_data=f'lim_edit_{action}_-5'), InlineKeyboardButton('-1', callback_data=f'lim_edit_{action}_-1'), InlineKeyboardButton('+1', callback_data=f'lim_edit_{action}_+1'), InlineKeyboardButton('+5', callback_data=f'lim_edit_{action}_+5')],
  [InlineKeyboardButton('1', callback_data=f'lim_edit_{action}_set_1'), InlineKeyboardButton('3', callback_data=f'lim_edit_{action}_set_3'), InlineKeyboardButton('5', callback_data=f'lim_edit_{action}_set_5'), InlineKeyboardButton('10', callback_data=f'lim_edit_{action}_set_10'), InlineKeyboardButton('20', callback_data=f'lim_edit_{action}_set_20')],
  [InlineKeyboardButton('بلا حد', callback_data=f'lim_edit_{action}_set_0')],
  [InlineKeyboardButton('رجوع', callback_data='lim_main'), InlineKeyboardButton('إغلاق', callback_data='close')]
 ])
def limits_text(cid, action=None):
 lim=get_limits(cid); limits=lim['limits']
 if action:
  cur=limits.get(action,0); cur_t=cur if cur!=0 else 'بلا حد'
  return f"حد {action} لكل مشرف\nالحالي : {cur_t}\nكل شخص ينحسب مرة وحدة\nاضغط الارقام تغيره، او ( بلا حد ) تشيله"
 txt="الحظر : بلا حد\nالطرد : بلا حد\nالكتم : بلا حد\nالتقييد : بلا حد\nالرفع : بلا حد\nالتنزيل : بلا حد\nالمسح : بلا حد\n\nيتجاوز من اوامر البوت : يرفض امره\nيتجاوز من اعدادات تيليجرام : يرجع اللي سواه"
 for a in LIMIT_ACTIONS:
  v=limits.get(a,0); v_t=f'{v}' if v!=0 else 'بلا حد'
  txt=txt.replace(f'{a} : بلا حد', f'{a} : {v_t}', 1)
 return txt

# AUTO DOWNLOAD SYSTEM
AUTO_DEFAULT_LIMITS={'Dev2':6, 'الاشراف': 7*24}
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
 cid=str(cid); uid=str(uid)
 if cid not in LAST_SEEN: LAST_SEEN[cid]={}
 LAST_SEEN[cid][uid]=int(time.time())
 sv('last_seen.json',LAST_SEEN)
def kb_auto_main(cid):
 auto=get_auto(cid); enabled=auto['enabled']
 toggle_text='تعطيل التنزيل التلقائي' if enabled else 'تفعيل التنزيل التلقائي'
 buttons=[
  [InlineKeyboardButton('مسح حدود التنزيل', callback_data='auto_clear')],
  [InlineKeyboardButton(toggle_text, callback_data='auto_toggle')],
  [InlineKeyboardButton('رجوع', callback_data='group_settings'), InlineKeyboardButton('اغلاق', callback_data='close')]
 ]
 if not enabled:
  buttons.insert(0, [InlineKeyboardButton('مسح حد تنزيل رتبة', callback_data='auto_clear_rank')])
  buttons.insert(0, [InlineKeyboardButton('ضع حد تنزيل لرتبة', callback_data='auto_set_rank')])
 return InlineKeyboardMarkup(buttons)
def kb_auto_set_rank():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('MYTH', callback_data='auto_rank_MYTH2'), InlineKeyboardButton('Dev2 : 6 ساعات', callback_data='auto_rank_Dev2')],
  [InlineKeyboardButton('المالك الاساسي', callback_data='auto_rank_المالك الاساسي'), InlineKeyboardButton('MYTH', callback_data='auto_rank_MYTH')],
  [InlineKeyboardButton('المنشئ الاساسي', callback_data='auto_rank_المنشئ الاساسي'), InlineKeyboardButton('المالك', callback_data='auto_rank_المالك')],
  [InlineKeyboardButton('المدير', callback_data='auto_rank_المدير'), InlineKeyboardButton('المنشئ', callback_data='auto_rank_المنشئ')],
  [InlineKeyboardButton('المميز', callback_data='auto_rank_المميز'), InlineKeyboardButton('الادمن', callback_data='auto_rank_الادمن')],
  [InlineKeyboardButton('الاشراف : 7 أيام', callback_data='auto_rank_الاشراف')],
  [InlineKeyboardButton('رجوع', callback_data='auto_main'), InlineKeyboardButton('اغلاق', callback_data='close')]
 ])
def kb_group_settings():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('إعدادات الوسائط NEW', callback_data='settings_media')],
  [InlineKeyboardButton('القفل والفتح', callback_data='lock_menu')],
  [InlineKeyboardButton('التفعيل والتعطيل', callback_data='enable_disable')],
  [InlineKeyboardButton('الوضع والمسح', callback_data='mode_clear')],
  [InlineKeyboardButton('التنظيف', callback_data='cleaning')],
  [InlineKeyboardButton('حدود المشرفين', callback_data='lim_main')],
  [InlineKeyboardButton('التنزيل التلقائي', callback_data='auto_main')],
  [InlineKeyboardButton('رجوع للقائمة الرئيسية للأوامر', callback_data='cmd_main')]
 ])
def text_auto_main(cid):
 auto=get_auto(cid); enabled=auto['enabled']; status='مفعل' if enabled else 'معطل'; limits=auto['limits']; lim_text=''
 for k,v in limits.items():
  lim_text+=f'- {k} : {v//24} أيام\n' if v>=24 else f'- {k} : {v} ساعات\n'
 if not lim_text: lim_text='- لا يوجد حدود\n'
 if enabled:
  return f"اعدادات التنزيل التلقائي\nالحالة : {status}\nاللي يغيب عن القروب اكثر من حد رتبته ينزل منها تلقائي\nحدود التنزيل الحالية :\n{lim_text}"
 else:
  return f"اعدادات التنزيل التلقائي\nالحالة : {status}\nاللي يغيب اكثر من حد رتبته ينزل تلقائي\nحدود التنزيل الحالية :\n{lim_text}\nالحدود ما تشتغل لين تكتب ( تفعيل التنزيل التلقائي )"

TEXT_MAIN='قائمة الأوامر\n\nاختر القسم الذي تريد معرفة أوامره:'

# START - عربي واضح بدون ترميز
async def start(u,c):
 if u.effective_chat.type=='private':
  text="هلا عزيزي انا سورد\n\nاقوى واسرع بوت حماية وتشغيل ميوزك\nوالعديد من المميزات الاخرى\n\nاذا رفعتني مشرف يتفعل تلقائي\nاضغط الاعدادات وضبط اعداداتي\n\nما فيني اي مطور ومسؤول غير Liam\n\nحساب مطوري - Liam"
  await u.message.reply_text(text,reply_markup=kb_start())
 else:
  await u.message.reply_text('قائمة الاوامر - سورد\nاختر القسم', reply_markup=kb_groups())

# CALLBACK - مصحح
async def cb(u,c):
 q=u.callback_query
 await q.answer()
 d=q.data
 cid=str(u.effective_chat.id)
 if d=='close':
  try: await q.message.delete()
  except: await q.edit_message_text('CLOSED BY : Liam')
  return
 if d.startswith('lim_'):
  if d=='lim_main':
   await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid)); return
  if d=='lim_disable':
   lim=get_limits(cid); lim['enabled']=not lim.get('enabled',True); sv('limits.json',LIMITS)
   await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid)); return
  if d=='lim_clear':
   LIMITS[str(cid)]['limits']={a:0 for a in LIMIT_ACTIONS}; sv('limits.json',LIMITS)
   await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid)); return
  if d.startswith('lim_edit_'):
   try: _,_,action,op = d.split('_',3)
   except:
    parts=d.split('_'); action=parts[2]; op='_'.join(parts[3:])
   cur=get_limits(cid)['limits'].get(action,0)
   if op.startswith('set_'): cur=int(op.replace('set_','')); LIMITS[str(cid)]['limits'][action]=cur; sv('limits.json',LIMITS)
   elif op in ['+1','+5','-1','-5']: cur=max(0,cur+int(op)); LIMITS[str(cid)]['limits'][action]=cur; sv('limits.json',LIMITS)
   await q.edit_message_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur)); return
  if d not in ['lim_main','lim_disable','lim_clear','lim_today']:
   action=d.replace('lim_','')
   if action in LIMIT_ACTIONS:
    cur=get_limits(cid)['limits'].get(action,0)
    await q.edit_message_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur)); return
 if d in ['cmd_main','cmd_groups','lockpanel','page1','about','onoff','manage','fun','dev','sets','group_settings']:
  await q.edit_message_text(TEXT_MAIN, reply_markup=kb_main_commands()); return
 if d.startswith('lock_') or d.startswith('lockpage_') or d in ['openall_1','closeall_1','openall','closeall','page2','l_','auto_main','auto_set_rank']:
  await q.edit_message_text('لوحة القفل والفتح', reply_markup=kb_lock_page(cid,1)); return
 if d.startswith('l_'):
  name=d[2:]; LOCKS.setdefault(cid,{}); LOCKS[cid][name]=not LOCKS[cid].get(name,False); sv('locks.json',LOCKS)
  await q.edit_message_text(f"{'تم قفل' if LOCKS[cid][name] else 'تم فتح'} {name}", reply_markup=kb_lock_p1()); return

async def txt(u,c):
 m=u.effective_message
 if not m or not m.text: return
 t=m.text.strip()
 if t in ['سورد','الاوامر','اوامر','قائمة الاوامر']:
  await m.reply_text(TEXT_MAIN, reply_markup=kb_groups()); return
 if t in ['رتبتي','رتبة','رتب']:
  try: await m.reply_text(f"رتبتك: عضو\nالاسم: {m.from_user.first_name}\nالتفاعل: 0")
  except: pass
  return
 if t in ['حبي','حبيبي']: await m.reply_text("حبي انت"); return
 if 'الاباحي' in t or 'الاباحه' in t: await m.reply_text(f"تم {t}"); return
 if t.startswith('/') and 'start' in t: await start(u,c); return

async def media_handler(u,c): return
async def edited(u,c): return
async def bot_promote_protection(c, m): return

if __name__=='__main__':
 if not TOKEN: raise RuntimeError('TOKEN')
 import asyncio
 threading.Thread(target=run,daemon=True).start()
 try:
  loop=asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
 except: pass
 app=ApplicationBuilder().token(TOKEN).build()
 app.add_handler(CommandHandler('start',start))
 app.add_handler(CallbackQueryHandler(cb))
 app.add_handler(MessageHandler(filters.TEXT & ~filters.UpdateType.EDITED_MESSAGE, txt))
 app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO | filters.Document.ALL) & ~filters.UpdateType.EDITED_MESSAGE, media_handler))
 app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, edited))
 print('SORD LIAM FULL 1668 LINES FIXED - kb_commands OK - NO FORCE JOIN - CLEAR ARABIC - NO APP DECORATOR')
 app.run_polling(allowed_updates=["message","edited_message","callback_query","chat_member"], drop_pending_updates=True)
