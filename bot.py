import os
import asyncio
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

for fp in ['locks.json','ranks.json','data.json','stats.json']:
    if not os.path.exists(fp):
        save(fp,{})

LOCKS=load('locks.json')
STATS=load('stats.json')

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'SOVE V5')

def run_server():
    p=int(os.getenv('PORT','10000'))
    HTTPServer(('0.0.0.0',p),H).serve_forever()

def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('القفل والفتح',callback_data='menu_lock'),InlineKeyboardButton('التفعيل والتعطيل',callback_data='menu_toggle')],
        [InlineKeyboardButton('ادارة القروب',callback_data='menu_admin'),InlineKeyboardButton('التسلية والخدمية',callback_data='menu_fun')],
        [InlineKeyboardButton('اوامر Dev',callback_data='menu_dev')],
        [InlineKeyboardButton('الاعدادات',callback_data='menu_settings')],
        [InlineKeyboardButton('اغلاق',callback_data='close')]
    ])

def kb_fun():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('الخدمات',callback_data='fun_services'),InlineKeyboardButton('المحتوى',callback_data='fun_content')],
        [InlineKeyboardButton('رتب التسلية',callback_data='fun_rank'),InlineKeyboardButton('التسلية',callback_data='fun_games')],
        [InlineKeyboardButton('رجوع',callback_data='back_main')]
    ])

def kb_services():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('الطقس',callback_data='svc_weather'),InlineKeyboardButton('اذان',callback_data='svc_azan')],
        [InlineKeyboardButton('الوقت',callback_data='svc_time'),InlineKeyboardButton('التاريخ',callback_data='svc_date')],
        [InlineKeyboardButton('ترجم',callback_data='svc_tr'),InlineKeyboardButton('معنى',callback_data='svc_mean')],
        [InlineKeyboardButton('زخرفه',callback_data='svc_zakh'),InlineKeyboardButton('العمر',callback_data='svc_age')],
        [InlineKeyboardButton('العملات',callback_data='svc_cur
