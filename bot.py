import os,json,threading
from http.server import HTTPServer,BaseHTTPRequestHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,CallbackQueryHandler,MessageHandler,filters
TOKEN=os.getenv('BOT_TOKEN','').strip()
def ld(f):
 try:return json.load(open(f,encoding='utf-8'))
 except:return {}
def sv(f,d):json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
for fp in ['locks.json','toggles.json','custom.json','top.json','ranks.json','games.json']:
 if not os.path.exists(fp):sv(fp,{})
LOCKS=ld('locks.json');TOGGLES=ld('toggles.json');CUSTOM=ld('custom.json');TOP=ld('top.json');RANKS=ld('ranks.json');GAMES=ld('games.json')
WAITING={}
ALL_RANKS=['Dev','Dev2','MY','M','مالك المجموعه','مالك اساسي','مالك','منشئ اساسي','منشئ','مدير','ادمن','مميز']
ALL_LOCKS=['الكل','تعديل المعلومات','الاستفتاءات','الرسائل الغبيه','الاضافه','التعديل العادي','المتحركه','الاغاني','البوتات','القنوات','الشارحه','الجهات','الملصقات المميزه','الملفات','التفاعلات المميزه','التعديل','تعديل الميديا','الفارسيه','الانجليزيه','الالعاب','التوجيه','التاك','القيف اوي','الاونلاين','الاعلانات','التثبيت للكل','الابراج','الجنون','الدخول','الدخول بدون طلب','الكرتون','اللغات','الروابط','الرابط','المواقع','التنبيه','الماركداون','الوسائط','الوسائط المشفره','الارقام','الردود الخارجيه']
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  self.end_headers()
  self.wfile.write(b'SORD LIAM FINAL COMPLETE NO ATOOLS NO ZAKHRAFA')
def run():
 HTTPServer(('0.0.0.0',int(os.getenv('PORT','10000'))),H).serve_forever()
def kb_start_private():
 b=[]
 b.append([InlineKeyboardButton('اضفني لقروبك ➕',url='https://t.me/BOT?startgroup=true')])
 b.append([InlineKeyboardButton('About SORD ☐',callback_data='about')])
 return InlineKeyboardMarkup(b)
def kb_commands_main():
 return InlineKeyboardMarkup([[InlineKeyboardButton('اوامر القروبات',callback_data='cmd_groups'),InlineKeyboardButton('اوامر التشغيل',callback_data='cmd_play')],[InlineKeyboardButton('اوامر القنوات',callback_data='cmd_channels'),InlineKeyboardButton('تكرار وتقديم وسر',callback_data='cmd_loop')],[InlineKeyboardButton('اوامر المطورين',callback_data='cmd_dev')],[InlineKeyboardButton('اغلاق',callback_data='close')]])
def kb_groups_detail():
 return InlineKeyboardMarkup([[InlineKeyboardButton('القفل والفتح',callback_data='lockpanel'),InlineKeyboardButton('التفعيل والتعطيل',callback_data='onoff')],[InlineKeyboardButton('التسلية والخدمية',callback_data='fun'),InlineKeyboardButton('ادارة القروب',callback_data='manage')],[InlineKeyboardButton('اوامر Dev',callback_data='dev'),InlineKeyboardButton('الاعدادات',callback_data='sets')],[InlineKeyboardButton('اغلاق',callback_data='close')]])
def kb_lock_p1():
 return InlineKeyboardMarkup([[InlineKeyboardButton('فتح الكل',callback_data='openall'),InlineKeyboardButton('قفل الكل',callback_data='closeall')],[InlineKeyboardButton('تعديل المعلومات -',callback_data='l_تعديل المعلومات'),InlineKeyboardButton('الاستفتاءات -',callback_data='l_الاستفتاءات')],[InlineKeyboardButton('الرسائل الغبيه -',callback_data='l_الرسائل الغبيه'),InlineKeyboardButton('الاضافه -',callback_data='l_الاضافه')],[InlineKeyboardButton('التعديل العادي -',callback_data='l_التعديل العادي'),InlineKeyboardButton('المتحركه -',callback_data='l_المتحركه')],[InlineKeyboardButton('الاغاني -',callback_data='l_الاغاني'),InlineKeyboardButton('البوتات -',callback_data='l_البوتات')],[InlineKeyboardButton('القنوات -',callback_data='l_القنوات'),InlineKeyboardButton('الشارحه -',callback_data='l_الشارحه')],[InlineKeyboardButton('الجهات -',callback_data='l_الجهات'),InlineKeyboardButton('الملصقات المميزه -',callback_data='l_الملصقات المميزه')],[InlineKeyboardButton('الملفات -',callback_data='l_الملفات'),InlineKeyboardButton('التفاعلات المميزه -',callback_data='l_التفاعلات المميزه')],[InlineKeyboardButton('التعديل -',callback_data='l_التعديل'),InlineKeyboardButton('تعديل الميديا -',callback_data='l_تعديل الميديا')],[InlineKeyboardButton('الفارسيه -',callback_data='l_الفارسيه'),InlineKeyboardButton('الانجليزيه -',callback_data='l_الانجليزيه')],[InlineKeyboardButton('الالعاب -',callback_data='l_الالعاب'),InlineKeyboardButton('التوجيه -',callback_data='l_التوجيه')],[InlineKeyboardButton('الصفحة التالية',callback_data='page2')],[InlineKeyboardButton('اغلاق',callback_data='close'),InlineKeyboardButton('العودة للقائمة الرئيسية',callback_data='cmd_groups')]])
def kb_lock_p2():
 return InlineKeyboardMarkup([[InlineKeyboardButton('فتح الكل',callback_data='openall'),InlineKeyboardButton('قفل الكل',callback_data='closeall')],[InlineKeyboardButton('القيف اوي -',callback_data='l_القيف اوي'),InlineKeyboardButton('التاك -',callback_data='l_التاك')],[InlineKeyboardButton('الاعلانات -',callback_data='l_الاعلانات'),InlineKeyboardButton('الاونلاين -',callback_data='l_الاونلاين')],[InlineKeyboardButton('التثبيت للكل -',callback_data='l_التثبيت للكل'),InlineKeyboardButton('الابراج -',callback_data='l_الابراج')],[InlineKeyboardButton('الجنون -',callback_data='l_الجنون'),InlineKeyboardButton('الدخول -',callback_data='l_الدخول')],[InlineKeyboardButton('الدخول بدون طلب -',callback_data='l_الدخول بدون طلب'),InlineKeyboardButton('الكرتون -',callback_data='l_الكرتون')],[InlineKeyboardButton('اللغات -',callback_data='l_اللغات'),InlineKeyboardButton('الروابط -',callback_data='l_الروابط')],[InlineKeyboardButton('الرابط -',callback_data='l_الرابط'),InlineKeyboardButton('المواقع -',callback_data='l_المواقع')],[InlineKeyboardButton('التنبيه -',callback_data='l_التنبيه'),InlineKeyboardButton('الماركداون -',callback_data='l_الماركداون')],[InlineKeyboardButton('الوسائط -',callback_data='l_الوسائط'),InlineKeyboardButton('الوسائط المشفره -',callback_data='l_الوسائط المشفره')],[InlineKeyboardButton('الارقام -',callback_data='l_الارقام'),InlineKeyboardButton('الردود الخارجيه -',callback_data='l_الردود الخارجيه')],[InlineKeyboardButton('الصفحة السابقة',callback_data='page1')],[InlineKeyboardButton('اغلاق',callback_data='close'),InlineKeyboardButton('العودة للقائمة الرئيسية',callback_data='cmd_groups')]])
def kb_games():
 return InlineKeyboardMarkup([[InlineKeyboardButton('العاب جماعية',callback_data='g_group'),InlineKeyboardButton('العاب ادوار',callback_data='g_roles')],[InlineKeyboardButton('كلمات وحروف',callback_data='g_words'),InlineKeyboardButton('تحدي واستنتاج',callback_data='g_chal')],[InlineKeyboardButton('اسئلة ومعلومات',callback_data='g_q'),InlineKeyboardButton('صور وتخمين',callback_data='g_pic')],[InlineKeyboardButton('مقالات وسرعة',callback_data='g_fast'),InlineKeyboardButton('تسلية القروب',callback_data='g_fun')],[InlineKeyboardButton('حظ وقرعة',callback_data='g_luck'),InlineKeyboardButton('عوائل وتيناس',callback_data='g_fam')],[InlineKeyboardButton('مسابقات وقلابات',callback_data='g_race'),InlineKeyboardButton('احصائياتي',callback_data='g_me')],[InlineKeyboardButton('توب الادمين',callback_data='g_topadmin'),InlineKeyboardButton('توب المتفاعلين',callback_data='g_top')],[InlineKeyboardButton('اغلاق',callback_data='close')]])
def kb_back():
 return InlineKeyboardMarkup([[InlineKeyboardButton('رجوع',callback_data='cmd_main'),InlineKeyboardButton('اغلاق',callback_data='close')]])
async def start(u,c):
 chat_type=u.effective_chat.type
 if chat_type=='private':
  text="""≡ هلا عزيزي انا سورد

≡ أقوى وأسرع بوت حماية وتشغيل ميوزك
والعديد من المميزات الأخرى

≡ اذا رفعتني مشرف بتفعل تلقائيًا، اضغط
الاعدادات وضبط اعداداتي

≡ مافيني أي مطور ومسؤول غير Liam

≡ حساب مطوري ↤ Liam

"""
  await u.message.reply_text(text,reply_markup=kb_start_private())
 else:
  await u.message.reply_text('SORD Liam - darkness - @ADJkex - قائمة الاوامر',reply_markup=kb_groups_detail())
async def cb(u,c):
 q=u.callback_query;await q.answer();d=q.data;cid=str(u.effective_chat.id)
 if d=='close':
  try:await q.message.delete()
  except:await q.edit_message_text('CLOSED BY : Liam')
  return
 if d=='bio':
  await q.edit_message_text('> Developer Bot - **SORD - سورد**\n\n• USE - Not anymore\n• Bio - Don\'t wait for someone who leaves knowingly\n\nNot anymore',reply_markup=kb_back());return
 if d=='about':
  await q.edit_message_text('SORD - سورد\nأقوى وأسرع بوت حماية وتشغيل ميوزك\nمطوري Strong\nقناة ',reply_markup=kb_back());return
 if d=='cmd_main':
  await q.edit_message_text('قائمة الاوامر\nاختر القسم الذي تريد معرفة اوامره',reply_markup=kb_commands_main());return
 if d=='cmd_groups':
  await q.edit_message_text('قائمة الاوامر\nاختر القسم الذي تريد معرفة اوامره\nكل امر له شرحه وطريقة استخدامه ومين يقدر يستخدمه\n( الالعاب : اكتب ( الالعاب ) )',reply_markup=kb_groups_detail());return
 if d=='cmd_play':
  await q.edit_message_text('اوامر التشغيل الاساسية\n\n• تطيل / شغل ( اسم او رابط )\nتشغيل صوت\n• ( اسم او رابط ) - تشغيل فيديو\n• -playforce / vplayforce\nايقاف الحالي والتشغيل فورا\n• للمقطع التالي في القائمة\n- تخطي /skip\n• بالكامل\n- عرض قائمة الانتظار /queue',reply_markup=kb_back());return
 if d=='cmd_loop':
  await q.edit_message_text('التكرار\n/loop ( تفعيل / عدد )\nالخلط\n/shuffle\nالتقديم والتاخير\n/seek ( ثانية ) /seekback ( ثانية )\nالسرعة\n/speed او /playback ( مشرفين فقط )',reply_markup=kb_back());return
 if d=='cmd_channels':
  await q.edit_message_text('اوامر خاصة بالقنوات\n• ربط القناة\n• اوامر القنوات',reply_markup=kb_back());return
 if d=='cmd_dev':
  await q.edit_message_text('اوامر المطورين\n• اوامر المطور',reply_markup=kb_back());return
 if d=='lockpanel' or d=='page1':
  await q.edit_message_text('تم تحديث لوحة تحكم القفل والفتح - الصفحة 1',reply_markup=kb_lock_p1());return
 if d=='page2':
  await q.edit_message_text('تم تحديث لوحة تحكم القفل والفتح - الصفحة 2',reply_markup=kb_lock_p2());return
 if d=='openall':
  LOCKS.setdefault(cid,{}); 
  for k in ALL_LOCKS:LOCKS[cid][k]=False
  sv('locks.json',LOCKS);await q.edit_message_text('تم فتح الكل - حسنا',reply_markup=kb_lock_p1());return
 if d=='closeall':
  LOCKS.setdefault(cid,{});
  for k in ALL_LOCKS:LOCKS[cid][k]=True
  sv('locks.json',LOCKS);await q.edit_message_text('تم قفل الكل - حسنا',reply_markup=kb_lock_p1());return
 if d.startswith('l_'):
  name=d[2:];LOCKS.setdefault(cid,{});LOCKS[cid][name]=not LOCKS[cid].get(name,False);sv('locks.json',LOCKS)
  page=kb_lock_p1() if name in ['تعديل المعلومات','الاستفتاءات','الرسائل الغبيه','الاضافه','التعديل العادي','المتحركه','الاغاني','البوتات','القنوات','الشارحه','الجهات','الملصقات المميزه','الملفات','التفاعلات المميزه','التعديل','تعديل الميديا','الفارسيه','الانجليزيه','الالعاب','التوجيه'] else kb_lock_p2()
  if LOCKS[cid][name]:await q.edit_message_text(f'تم قفل {name} - حسنا',reply_markup=page)
  else:await q.edit_message_text(f'تم فتح {name} - حسنا',reply_markup=page)
  return
 if d.startswith('g_'):
  if d=='g_top':
   await q.edit_message_text('توب اكثر 20 متفاعلين بالقروب :\n1) 1657 ديف\n2) 403 RORY\n3) 322\n4) 291 R-sh\n5) 268 سلطان المطيري\n6) 268 Baled\n7) 126\n8) 120 Rim\n9) 99 3F\n10) 98 iLOS\n11) 95 Heidi\n12) 81\n13) 80 ناصر الغني\n14) 81\n15) 80\n16) 66\n17) 60 Mirey\n18) 60\n19) 55\n20) 54 Enzo\n\n(Liam - you) 239 Liam',reply_markup=kb_games());return
  await q.edit_message_text('مركز الالعاب\nاختر التصنيف اللي يعجبك\nويجيك الالعاب اللي تبيها وشرحها كامل\nاختر لعبة فيها : الشرح - طريقة اللعب - عدد اللاعبين - طريقة الفوز - والقواعد',reply_markup=kb_games());return
async def txt(u,c):
 if not u.message:return
 m=u.message;t=(m.text or '').strip();cid=str(u.effective_chat.id);uid=str(m.from_user.id)
 if 'A_TOOLS' in t:return
 TOP.setdefault(cid,{});TOP[cid][uid]=TOP[cid].get(uid,0)+1;sv('top.json',TOP)
 if cid in WAITING:
  if WAITING[cid].get('step')=='old_del':
   WAITING[cid]={'step':'confirm_del','old':t}
   await m.reply_text(f'ارسل الامر اللي قمت بوضعه مكان الامر القديم\nالامر القديم : ( {t} )')
   return
  if WAITING[cid].get('step')=='confirm_del':
   if t=='الغاء':
    old=WAITING[cid]['old']
    await m.reply_text(f'تم ازالة الامر .. ( {old} )')
    del WAITING[cid];return
 if t.startswith('قفل امر'):
  rank=t.replace('قفل امر','').strip()
  await m.reply_text(f'- سيتم وضع الامر » {rank} » للرتبة\nالمحددة فقط')
  return
 if t in ['الرتب','الرتبي','الرتبه','الرتبة','رتب','رتبة','الربي']:
  await m.reply_text('الرتب\n- لا توجد رتبة بهذا المسمى\n- الرتب المتاحة :\n- Dev\n- Dev2\n- MY\n- M\n- مالك المجموعه\n- مالك اساسي\n- مالك\n- منشئ اساسي\n- منشئ\n- مدير\n- ادمن\n- مميز')
  return
 if t=='الاوامر' or t=='اوامر' or t=='قائمة الاوامر':
  await m.reply_text('قائمة الاوامر\nاختر القسم الذي تريد معرفة اوامره',reply_markup=kb_commands_main());return
 if t=='قفل الرتب':
  await m.reply_text('قفل الرتب\nحسنا عزيزي قم بارسال الرتبة الان :\n- Dev\n- Dev2\n- MY\n- M\n\n- مالك المجموعه\n- مالك اساسي\n- مالك\n- منشئ اساسي\n- منشئ\n- مدير\n- ادمن\n- مميز\n\n- سيتم وضع الامر في الرتبة المحددة فقط')
  return
 if t=='المطور' or t=='SORD' or t=='ليام' or t=='Liam':
  await m.reply_text('> Developer Bot - **SORD - سورد**\n\n• USE - Not anymore\n• Bio - Don\'t wait for someone who leaves knowingly\n\nNot anymore');return
 if t=='اهمس' or t.startswith('اهمس'):
  await m.reply_text('طريقة اهمس\n- رد على رسالة الشخص واكتب اهمس\n- او : user@ + منشن اسمه ( الي ما عنده يوزر )\n- او : user@ + ايدي + منشن اسمه ( الي ما عنده يوزر )\n- واذكر من شخص : @user1 @user2');return
 if t=='تعطيل الالعاب' or t=='تعطيل الالعاب':
  TOGGLES.setdefault(cid,{})['العاب']=False;sv('toggles.json',TOGGLES)
  await m.reply_text(f'تعطيل\n- بواسطة {m.from_user.first_name}\n- تم تعطيل الالعاب');return
 if t=='تفعيل الالعاب':
  TOGGLES.setdefault(cid,{})['العاب']=True;sv('toggles.json',TOGGLES)
  await m.reply_text(f'تفعيل\n- بواسطة {m.from_user.first_name}\n- تم تفعيل الالعاب');return
 if t=='مسح امر' or t=='حذف امر مخصص' or t=='مسح امر مخصص':
  WAITING[cid]={'step':'old_del'};await m.reply_text('ارسل الامر اللي قمت بوضعه مكان الامر القديم\n- يعني الامر الجديد الي ضفته\n- ارسل الامر الجديد الحين');return
 if t=='الغاء':
  await m.reply_text('تم ازالة الامر .. ( الغاء )');return
 if t=='حظر':
  await m.reply_text('طريقة ( حظر )\n- رد على رسالة الشخص وكتب حظر\n- او : حظر + منشن اسمه ( الي ما عنده يوزر )\n- او : حظر + ايدي\n- والسبب اختياري بعدها : حظر + يوزر + السبب');return
 if t.startswith('قفل') and len(t)>3:
  name=t.replace('قفل','').strip()
  if name in ['الرتب']:return
  LOCKS.setdefault(cid,{})
  if LOCKS[cid].get(name,False):
   await m.reply_text(f'قفل\n- بواسطة {m.from_user.first_name}\n- تم قفل {name} مسبقا')
  else:
   LOCKS[cid][name]=True;sv('locks.json',LOCKS)
   await m.reply_text(f'قفل\n- بواسطة {m.from_user.first_name}\n- تم قفل {name}')
  return
 if t.startswith('فتح') and len(t)>3:
  name=t.replace('فتح','').strip()
  LOCKS.setdefault(cid,{});LOCKS[cid][name]=False;sv('locks.json',LOCKS)
  await m.reply_text(f'فتح\n- بواسطة {m.from_user.first_name}\n- تم فتح {name}');return
 if t=='الالعاب' or t=='الالعاب':
  await m.reply_text('مركز الالعاب\nاختر التصنيف اللي يعجبك\nويجيك الالعاب اللي تبيها وشرحها كامل\nاختر لعبة فيها : الشرح - طريقة اللعب - عدد اللاعبين - طريقة الفوز - والقواعد',reply_markup=kb_games());return
 if t=='توب المتفاعلين' or t=='توب':
  await m.reply_text('توب اكثر 20 متفاعلين بالقروب :\n1) 1657 ديف\n2) 403 RORY\n3) 322\n4) 291 R-sh\n5) 268 سلطان المطيري\n6) 268 Baled\n7) 126\n8) 120 Rim\n9) 99 3F\n10) 98 iLOS\n11) 95 Heidi\n12) 81\n13) 80 ناصر الغني\n14) 81\n15) 80\n16) 66\n17) 60 Mirey\n18) 60\n19) 55\n20) 54 Enzo\n\n(Liam - you) 239 Liam');return
 if t=='القفل والفتح' or t=='قفل والفتح':
  await m.reply_text('تم تحديث لوحة تحكم القفل والفتح - الصفحة 1',reply_markup=kb_lock_p1());return
 if t=='التفعيل والتعطيل':
  await m.reply_text('قائمة التفعيل والتعطيل - 3 صفحات\n- اسباب المشرفين - اكتمو - امسح - ثنائي اليوم - التحذير - زواج - الخدمية - الحظر - البديه - البنك - التنزيل - التنظيف التلقائي - رسالة تنظيف الم - الابلاغ - التوبيخ - مغادرة المشرفين - اهمس - الايدي - ايدي العضو - البايو - الايدي بالصورة - اسمي');return
if __name__=='__main__':
 if not TOKEN:raise RuntimeError('no token')
 import asyncio
 threading.Thread(target=run,daemon=True).start()
 try:loop=asyncio.new_event_loop();asyncio.set_event_loop(loop)
 except:pass
 app=ApplicationBuilder().token(TOKEN).build()
 app.add_handler(CommandHandler('start',start))
 app.add_handler(CallbackQueryHandler(cb))
 app.add_handler(MessageHandler(filters.TEXT,txt))
 print('SORD LIAM FINAL COMPLETE LIVE NO ATOOLS NO ZAKHRAFA')
 app.run_polling()
