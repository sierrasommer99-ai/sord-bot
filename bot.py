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
    STATS[cid][str(uid)]=STATS[cid].get(str(uid),0)+1; save('stats.json',STATS)
    target=None
    if msg.reply_to_message: target=msg.reply_to_message.from_user
    def need(): return target is None
    if txt=='م1': await msg.reply_text('م1 حماية',reply_markup=kb_menu()); return
    if txt=='م2': await msg.reply_text('م2 رفع',reply_markup=kb_menu()); return
    if txt=='م3': await msg.reply_text('م3 حظر',reply_markup=kb_menu()); return
    if txt in ['الاوامر','/start']: await msg.reply_text('سترونق',reply_markup=kb_menu()); return
    if 'كس' in low or 'xnxx' in low or 'porn' in low:
        if LOCKS.get(cid,{}).get('porn',True):
            try: await msg.delete()
            except: pass
            return
    if txt=='رفع مالك':
        if need(): await msg.reply_text('رد'); return
        r=get_r(cid); r['malik'].append(target.id) if target.id not in r['malik'] else None; save('ranks.json',RANKS); await msg.reply_text('تم رفعه مالك'); return
    if txt=='تنزيل مالك':
        if need(): return
        r=get_r(cid); r['malik'].remove(target.id) if target.id in r['malik'] else None; save('ranks.json',RANKS); await msg.reply_text('تم تنزيله'); return
    if txt=='رفع منشئ':
        if need(): await msg.reply_text('رد'); return
        r=get_r(cid); r['monshe'].append(target.id) if target.id not in r['monshe'] else None; save('ranks.json',RANKS); await msg.reply_text('تم رفعه منشئ'); return
    if txt=='تنزيل منشئ':
        if need(): return
        r=get_r(cid); r['monshe'].remove(target.id) if target.id in r['monshe'] else None; save('ranks.json',RANKS); await msg.reply_text('تم تنزيله'); return
    if txt=='رفع مدير':
        if need(): await msg.reply_text('رد'); return
        r=get_r(cid); r['modir'].append(target.id) if target.id not in r['modir'] else None; save('ranks.json',RANKS); await msg.reply_text('تم رفعه مدير'); return
    if txt=='تنزيل مدير':
        if need(): return
        r=get_r(cid); r['modir'].remove(target.id) if target.id in r['modir'] else None; save('ranks.json',RANKS); await msg.reply_text('تم تنزيله'); return
    if txt=='رفع ادمن':
        if need(): await msg.reply_text('رد'); return
        r=get_r(cid); r['admin'].append(target.id) if target.id not in r['admin'] else None; save('ranks.json',RANKS); await msg.reply_text('تم رفعه ادمن'); return
    if txt=='تنزيل ادمن':
        if need(): return
        r=get_r(cid); r['admin'].remove(target.id) if target.id in r['admin'] else None; save('ranks.json',RANKS); await msg.reply_text('تم تنزيله'); return
    if txt=='رفع مميز':
        if need(): await msg.reply_text('رد'); return
        r=get_r(cid); r['momayz'].append(target.id) if target.id not in r['momayz'] else None; save('ranks.json',RANKS); await msg.reply_text('تم رفعه مميز'); return
    if txt=='تنزيل مميز':
        if need(): return
        r=get_r(cid); r['momayz'].remove(target.id) if target.id in r['momayz'] else None; save('ranks.json',RANKS); await msg.reply_text('تم تنزيله'); return
    if txt=='رفع مطور':
        if need(): await msg.reply_text('رد'); return
        r=get_r(cid); r['motawer'].append(target.id) if target.id not in r['motawer'] else None; save('ranks.json',RANKS); await msg.reply_text('تم رفعه مطور'); return
    if 'رفع' in txt and 'dev' in low:
        if need(): await msg.reply_text('رد'); return
        r=get_r(cid); r['dev'].append(target.id) if target.id not in r['dev'] else None; save('ranks.json',RANKS); await msg.reply_text('تم رفعه Dev'); return
    if txt=='رفع مشرف':
        if need(): await msg.reply_text('رد'); return
        await msg.reply_text('رفع مشرف',reply_markup=kb_prom(target.id)); return
    if txt=='المالكين': r=get_r(cid); await msg.reply_text('المالكين'); return
    if txt=='كتم':
        if need(): await msg.reply_text('رد'); return
        try: await c.bot.restrict_chat_member(cid,target.id,permissions=ChatPermissions(can_send_messages=False)); await msg.reply_text('تم كتمه')
        except: pass
        return
    if txt=='الغاء الكتم':
        if need(): return
        try: await c.bot.restrict_chat_member(cid,target.id,permissions=ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)); await msg.reply_text('تم الغاء كتمه')
        except: pass
        return
    if txt=='حظر':
        if need(): await msg.reply_text('رد'); return
        try: await c.bot.ban_chat_member(cid,target.id); await msg.reply_text('تم حظره')
        except: pass
        return
    if txt=='الغاء الحظر':
        if need(): return
        try: await c.bot.unban_chat_member(cid,target.id); await msg.reply_text('تم الغاء حظره')
        except: pass
        return
    if txt=='تقيد':
        if need(): await msg.reply_text('رد'); return
        try: await c.bot.restrict_chat_member(cid,target.id,permissions=ChatPermissions(can_send_messages=False)); await msg.reply_text('تم تقييده')
        except: pass
        return
    if txt=='طرد':
        if need(): await msg.reply_text('رد'); return
        try: await c.bot.ban_chat_member(cid,target.id); await c.bot.unban_chat_member(cid,target.id); await msg.reply_text('تم طرده')
        except: pass
        return
    if txt.startswith('قفل'):
        typ=txt.replace('قفل','').strip().split(' ')[0]
        mp={'الروابط':'link','المعرف':'user','التاك':'tag','الشارحه':'fwd','الصور':'photo','الفيديو':'video','البوتات':'bot','التعديل':'edit','الاباحي':'porn','الكل':'all'}
        if typ in mp:
            if cid not in LOCKS: LOCKS[cid]={}
            LOCKS[cid][mp[typ]]=True; save('locks.json',LOCKS); await msg.reply_text(f'تم قفل {typ}')
        return
    if txt.startswith('فتح'):
        typ=txt.replace('فتح','').strip().split(' ')[0]
        mp={'الروابط':'link','المعرف':'user','التاك':'tag','الشارحه':'fwd','الصور':'photo','الفيديو':'video','البوتات':'bot','التعديل':'edit','الاباحي':'porn','الكل':'all'}
        if typ in mp:
            if cid not in LOCKS: LOCKS[cid]={}
            LOCKS[cid][mp[typ]]=False; save('locks.json',LOCKS); await msg.reply_text(f'تم فتح {typ}')
        return
    if txt=='الاعدادات':
        out='الاعدادات:\n'
        for k,v in LOCKS.get(cid,{}).items(): out+=f'{k}:{"مقفل" if v else "مفتوح"}\n'
        await msg.reply_text(out,reply_markup=kb_menu()); return
    if txt=='رتبتي': r=rn(uid,cid); cnt=STATS.get(cid,{}).get(str(uid),0); await msg.reply_text(f'رتبتك {r} رسائلك {cnt}'); return
    if txt=='ايدي': await msg.reply_text(f'{uid}'); return
    if txt=='بوت' or txt=='سورد': await msg.reply_text(f'نعم {name}؟'); return
    if txt=='المطور': await msg.reply_text('@ADJkex'); return
async def photo_h(u,c):
    cid=str(u.effective_chat.id)
    if LOCKS.get(cid,{}).get('photo',False):
        try: await u.message.delete()
        except: pass
async def edit_h(u,c):
    if not u.edited_message: return
    cid=str(u.effective_chat.id)
    if LOCKS.get(cid,{}).get('edit',False):
        try: await u.edited_message.delete()
        except: pass
async def new_m(u,c):
    msg=u.message; cid=str(u.effective_chat.id)
    for user in msg.new_chat_members:
        if user.is_bot and user.id != c.bot.id:
            if LOCKS.get(cid,{}).get('bot',True):
                try: await c.bot.ban_chat_member(cid,user.id)
                except: pass
if __name__=='__main__':
    if not TOKEN: raise RuntimeError('no token')
    import asyncio
    threading.Thread(target=run_http,daemon=True).start()
    try: loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop)
    except: pass
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',cmd_start))
    app.add_handler(CallbackQueryHandler(cb_all))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,new_m))
    app.add_handler(MessageHandler(filters.TEXT,text_all))
    app.add_handler(MessageHandler(filters.PHOTO,photo_h))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE,edit_h))
    print('STRONG FIXED LIVE')
    app.run_polling()
