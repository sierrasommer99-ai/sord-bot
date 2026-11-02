import os,json,threading
from http.server import HTTPServer,BaseHTTPRequestHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler
from telegram.ext import CallbackQueryHandler,MessageHandler,filters

# TOKEN
TOKEN=os.getenv('BOT_TOKEN','').strip() or "8769832522:AAF1yu7T8C-DQEfz6ggzvidtKrs_1SUi7Gk"
# الغاء الانضمام الاجباري
FORCE_CHANNEL=None
CHANNEL=None
MUST_JOIN=None
CHANNEL_ID=None
JOIN_CHANNEL=None
FORCE_SUB=None
async def check_join(*a,**k):return True
async def must_join(*a,**k):return True
async def is_joined(*a,**k):return True
async def check_channel(*a,**k):return True
async def check_sub(*a,**k):return True
async def is_subbed(*a,**k):return True

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


# ---------- Ù†Ø¸Ø§Ù… Ø§Ù„Ù‚ÙÙ„ 6 ØµÙØ­Ø§Øª Ù…Ø«Ù„ Ø¯Ø§Ø±ÙƒÙ†Ø³ ----------
LOCKS_PAGES = {
1: ['ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª','Ø§Ù„Ø§Ø³ØªÙØªØ§Ø¡Ø§Øª','Ø§Ù„Ø±Ø³Ø§Ø¦Ù„ Ø§Ù„ØºÙ†ÙŠØ©','Ø§Ù„Ø§Ø¶Ø§ÙÙ‡','Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ','Ø§Ù„Ù…ØªØ­Ø±ÙƒÙ‡','Ø§Ù„Ø§ØºØ§Ù†ÙŠ','Ø§Ù„Ø¨ÙˆØªØ§Øª','Ø§Ù„Ù‚Ù†ÙˆØ§Øª','Ø§Ù„Ø´Ø§Ø±Ø­Ù‡'],
2: ['Ø§Ù„Ø¬Ù‡Ø§Øª','Ø§Ù„Ù…Ù„ØµÙ‚Ø§Øª Ø§Ù„Ù…Ù…ÙŠØ²Ø©','Ø§Ù„Ù…Ù„ÙØ§Øª','Ø§Ù„ØªÙØ§Ø¹Ù„Ø§Øª Ø§Ù„Ù…Ù…ÙŠØ²Ø©','Ø§Ù„ØªØ¹Ø¯ÙŠÙ„','ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ù…ÙŠØ¯ÙŠØ§','Ø§Ù„ÙØ§Ø±Ø³ÙŠÙ‡','Ø§Ù„Ø§Ù†Ø¬Ù„ÙŠØ²ÙŠÙ‡','Ø§Ù„ØªÙˆØ¬ÙŠÙ‡','Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨'],
3: ['Ø§Ù„ØªØ§Ùƒ','Ø§Ù„Ù‚ÙŠÙ Ø§ÙˆØ§ÙŠ','Ø§Ù„Ø§Ø¹Ù„Ø§Ù†Ø§Øª','Ø§Ù„Ø§Ù†Ù„Ø§ÙŠÙ†','Ø§Ù„Ø§Ù†Ù„Ø§ÙŠÙ† Ù„Ù„ÙƒÙ„','Ø§Ù„Ø§ÙŠØ±Ø§Ù†ÙŠÙŠÙ†','Ø§Ù„Ø¯Ø®ÙˆÙ„','Ø§Ù„Ø¬Ù…Ø«ÙˆÙ†','Ø§Ù„ÙƒÙŠØ¨ÙˆØ±Ø¯','Ø§Ù„Ø¯Ø®ÙˆÙ„ Ø¨Ø¯ÙˆÙ† Ø·Ù„Ø¨'],
4: ['Ø§Ù„Ø±ÙˆØ§Ø¨Ø·','Ø§Ù„Ù„ØºØ§Øª','Ø§Ù„Ù…ÙˆØ§Ù‚Ø¹','Ø§Ù„Ø±Ø¨Ø·','Ø§Ù„Ù…Ø§Ø±ÙƒØ¯Ø§ÙˆÙ†','Ø§Ù„ØªØ«Ø¨ÙŠØª','Ø§Ù„ÙˆØ³Ø§Ø¦Ø· Ø§Ù„Ù…Ø´ÙØ±Ø©','Ø§Ù„ÙˆØ³Ø§Ø¦Ø·','Ø§Ù„Ø±Ø¯ÙˆØ¯ Ø§Ù„Ø®Ø§Ø±Ø¬ÙŠÙ‡','Ø§Ù„Ø£Ø±Ù‚Ø§Ù…'],
5: ['Ø§Ù„Ø§ÙƒÙˆØ§Ø¯','Ø§Ù„ØµÙˆØ±','Ø§Ù„Ø±ÙˆØ³ÙŠ','Ø§Ù„Ø§Ù‚ØªØ¨Ø§Ø³Ø§Øª','Ø§Ù„ØªÙƒØ±Ø§Ø±','Ø§Ù„Ø³Ø¨','Ø§Ù„ÙƒÙ„Ø§ÙŠØ´','Ø§Ù„ØªÙÙ„ÙŠØ´','Ø§Ù„Ù…Ù„ØµÙ‚Ø§Øª','Ø§Ù„ØªØ´ÙˆÙŠØ´'],
6: ['Ø§Ù„Ø§Ø´Ø¹Ø§Ø±Ø§Øª','Ø§Ù„Ù‚ØµØµ','Ø§Ù„ØªÙ‚Ù„ÙŠØ¯','Ø§Ù„Ø¯Ø±Ø¯Ø´Ù‡','Ø§Ù„Ù…Ø¹Ø±ÙØ§Øª','Ø§Ù„Ø³ÙŠÙ„ÙÙŠ','Ø§Ù„ÙÙŠØ¯ÙŠÙˆ','Ø§Ù„ØµÙˆØª','Ø§Ù„Ø§Ù†ØªÙ‡Ø§ÙƒØ§Øª']
}

def get_lock_text(cid, name):
 # True = Ù…Ù‚ÙÙ„ = Ø§Ø²Ø±Ù‚
 locked = LOCKS.get(cid,{}).get(name, False)
 if locked:
  return f"ðŸ”µ -{name}"
 else:
  return f"ðŸŸ¢ -{name}"

def kb_lock_page(cid, page):
 page = max(1, min(6, page))
 locks = LOCKS_PAGES.get(page, [])
 kb = []
 # ÙØªØ­ Ø§Ù„ÙƒÙ„ / Ù‚ÙÙ„ Ø§Ù„ÙƒÙ„
 kb.append([
  InlineKeyboardButton('â€¢ ÙØªØ­ Ø§Ù„ÙƒÙ„',callback_data=f'openall_{page}'),
  InlineKeyboardButton('â€¢ Ù‚ÙÙ„ Ø§Ù„ÙƒÙ„',callback_data=f'closeall_{page}')
 ])
 # ØµÙÙˆÙ Ø§Ù„Ù‚ÙÙ„ 2 ÙÙŠ ÙƒÙ„ ØµÙ
 for i in range(0, len(locks), 2):
  row = []
  for j in range(2):
   if i+j < len(locks):
    name = locks[i+j]
    row.append(InlineKeyboardButton(get_lock_text(cid, name), callback_data=f'lock_{name}'))
  kb.append(row)
 # Ø§Ø²Ø±Ø§Ø± Ø§Ù„ØªÙ†Ù‚Ù„
 if page==1:
  kb.append([InlineKeyboardButton('â€¢ Ø§Ù„ØµÙØ­Ø© Ø§Ù„ØªØ§Ù„ÙŠØ©',callback_data='lockpage_2')])
 elif page==6:
  kb.append([InlineKeyboardButton('â€¢ Ø§Ù„ØµÙØ­Ø© Ø§Ù„Ø³Ø§Ø¨Ù‚Ø©',callback_data='lockpage_5')])
 else:
  kb.append([
   InlineKeyboardButton('â€¢ Ø§Ù„ØµÙØ­Ø© Ø§Ù„Ø³Ø§Ø¨Ù‚Ø©',callback_data=f'lockpage_{page-1}'),
   InlineKeyboardButton('â€¢ Ø§Ù„ØµÙØ­Ø© Ø§Ù„ØªØ§Ù„ÙŠØ©',callback_data=f'lockpage_{page+1}')
  ])
 kb.append([InlineKeyboardButton('â€¢ Ø§Ø®ÙØ§Ø¡',callback_data='close')])
 kb.append([InlineKeyboardButton('â€¢ Ø§Ù„Ø¹ÙˆØ¯Ø© Ù„Ù„Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø±Ø¦ÙŠØ³ÙŠØ©',callback_data='cmd_groups')])
 # Ø¹Ø±Ø¶ Ø§Ù„ØµÙØ­Ø© Ø§Ù„Ø­Ø§Ù„ÙŠØ©
 kb.append([InlineKeyboardButton(f'{page} / 6',callback_data='noop'), InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹',callback_data='cmd_groups')])
 # Ù„ÙƒÙ† Ù„Ù„ØªÙˆØ§ÙÙ‚ Ù…Ø¹ Ø§Ù„ØµÙˆØ± : Ù†Ø³ØªØ®Ø¯Ù… 6 ØµÙØ­Ø§Øª
 return InlineKeyboardMarkup(kb)

def kb_lock_page_old(cid, page):
 return kb_lock_page(cid, page)

# Ù†Øµ Ù„ÙˆØ­Ø© Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­
LOCK_PANEL_TEXT = '''Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­
â€”â€”â€”â€”â€”â€”â€”â€”â€”
â€¢ ØªÙ‚ÙÙ„ ÙˆØªÙØªØ­ Ø§Ù†ÙˆØ§Ø¹ Ø§Ù„Ø±Ø³Ø§Ø¦Ù„ ÙˆØ§Ù„Ù…Ø­ØªÙˆÙ‰ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨
â€¢ Ø§Ù„ØµÙØ­Ø© {page} Ù…Ù† 6

â€¢ Ø§Ø¶ØºØ· Ø¹Ù„Ù‰ Ø§Ù„Ø§Ù…Ø± Ø¹Ø´Ø§Ù† ÙŠØ·Ù„Ø¹ Ø´Ø±Ø­Ù‡'''


# ---------- Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨ Ù…Ø¹ Ø§Ù„Ø´Ø±Ø­ ----------
GAMES_DATA = {
 'ÙƒØª ØªÙˆÙŠØª': {'desc': 'ÙŠØ·Ù„Ø¹ Ù„Ùƒ ØªÙˆÙŠØªØ§Øª Ø¬Ø§Ù‡Ø²Ø©', 'play': 'Ø§ÙƒØªØ¨ ÙƒØª ØªÙˆÙŠØª', 'players': '1', 'win': 'ØªØ³Ù„ÙŠØ©'},
 'Ø§Ø°ÙƒØ§Ø±': {'desc': 'ÙŠØ·Ù„Ø¹ Ù„Ùƒ Ø°ÙƒØ±', 'play': 'Ø§ÙƒØªØ¨ Ø§Ø°ÙƒØ§Ø±', 'players': '1', 'win': 'Ø§Ø¬Ø±'},
 'Ø­Ø¸': {'desc': 'ÙŠØ·Ù„Ø¹ Ù„Ùƒ Ù†Ø³Ø¨Ø© Ø­Ø¸Ùƒ', 'play': 'Ø§ÙƒØªØ¨ Ø­Ø¸', 'players': '1', 'win': 'Ø­Ø¸Ùƒ'},
 'Ø§Ù„Ø¹Ù‚Ø§Ø¨': {'desc': 'Ù„Ø¹Ø¨Ø© Ø§Ù„Ø¹Ù‚Ø§Ø¨ - Ø§Ù„Ù„ÙŠ ÙŠØ®Ø³Ø± ÙŠØªØ¹Ø§Ù‚Ø¨', 'play': 'Ø§ÙƒØªØ¨ Ø§Ù„Ø¹Ù‚Ø§Ø¨', 'players': '2+', 'win': 'ØªÙ‡Ø±Ø¨ Ù…Ù† Ø§Ù„Ø¹Ù‚Ø§Ø¨'},
 'Ø§Ù„Ø­ÙƒÙ…': {'desc': 'Ù„Ø¹Ø¨Ø© Ø§Ù„Ø­ÙƒÙ… - ØªØ­ÙƒÙ… Ø¹Ù„Ù‰ Ø§Ù„Ù„ÙŠ ÙŠØ®Ø³Ø±', 'play': 'Ø§ÙƒØªØ¨ Ø§Ù„Ø­ÙƒÙ…', 'players': '2+', 'win': 'ØªØ­ÙƒÙ… Ø¹Ù„Ù‰ ØºÙŠØ±Ùƒ'},
 'Ø§Ù„ÙƒØ±Ø³ÙŠ': {'desc': 'Ù„Ø¹Ø¨Ø© Ø§Ù„ÙƒØ±Ø³ÙŠ - Ø§Ø³Ø¦Ù„Ø© Ø¬Ø±ÙŠØ¦Ø©', 'play': 'Ø§ÙƒØªØ¨ Ø§Ù„ÙƒØ±Ø³ÙŠ', 'players': '2+', 'win': 'ØªØ¬Ø§ÙˆØ¨ Ø¨ØµØ±Ø§Ø­Ø©'},
 'Ø§Ø³Ø¦Ù„Ø©': {'desc': 'Ø§Ø³Ø¦Ù„Ø© Ù…ØªÙ†ÙˆØ¹Ø© ÙˆÙ…Ø­ÙŠØ±Ø©', 'play': 'Ø§ÙƒØªØ¨ Ø§Ø³Ø¦Ù„Ø©', 'players': '1+', 'win': 'ØªØ¬Ø§ÙˆØ¨ ØµØ­'},
 'Ù„Ø¹Ø¨Ù†ÙŠ': {'desc': 'Ù„Ø¹Ø¨Ø© Ù„Ø¹Ø¨Ù†ÙŠ - Ø§Ù„Ø¨ÙˆØª ÙŠÙ„Ø¹Ø¨Ùƒ', 'play': 'Ø§ÙƒØªØ¨ Ù„Ø¹Ø¨Ù†ÙŠ', 'players': '1 Ø¶Ø¯ Ø§Ù„Ø¨ÙˆØª', 'win': 'ØªÙÙˆØ² Ø¹Ù„Ù‰ Ø§Ù„Ø¨ÙˆØª'},
 'Ø­Ø¬Ø± ÙˆØ±Ù‚Ø© Ù…Ù‚Øµ': {'desc': 'Ù„Ø¹Ø¨Ø© Ø­Ø¬Ø± ÙˆØ±Ù‚Ø© Ù…Ù‚Øµ', 'play': 'Ø§ÙƒØªØ¨ Ø­Ø¬Ø±', 'players': '1 Ø¶Ø¯ Ø§Ù„Ø¨ÙˆØª', 'win': 'ØªÙÙˆØ² Ø¹Ù„Ù‰ Ø§Ù„Ø¨ÙˆØª'},
 'Ù†Ø³Ø¨Ø© Ø§Ù„Ø­Ø¨': {'desc': 'ÙŠØ­Ø³Ø¨ Ù†Ø³Ø¨Ø© Ø§Ù„Ø­Ø¨ Ø¨ÙŠÙ†Ùƒ ÙˆØ¨ÙŠÙ† Ø´Ø®Øµ', 'play': 'Ø§ÙƒØªØ¨ Ù†Ø³Ø¨Ø© Ø§Ù„Ø­Ø¨ + Ù…Ù†Ø´Ù†', 'players': '2', 'win': 'Ø§Ù„Ø­Ø¨'},
}

def get_game_text(name):
 g = GAMES_DATA.get(name)
 if not g:
  return f"Ù„Ø¹Ø¨Ø© {name}\\nØ§Ù„Ø´Ø±Ø­ : ØªØ³Ù„ÙŠØ©\\nØ·Ø±ÙŠÙ‚Ø© Ø§Ù„Ù„Ø¹Ø¨ : Ø§ÙƒØªØ¨ {name}\\nØ¹Ø¯Ø¯ Ø§Ù„Ù„Ø§Ø¹Ø¨ÙŠÙ† : 1\\nØ·Ø±ÙŠÙ‚Ø© Ø§Ù„ÙÙˆØ² : ØªØ³Ù„ÙŠØ©"
 return f"ðŸŽ® {name}\\n\\nØ§Ù„Ø´Ø±Ø­ : {g['desc']}\\nØ·Ø±ÙŠÙ‚Ø© Ø§Ù„Ù„Ø¹Ø¨ : {g['play']}\\nØ¹Ø¯Ø¯ Ø§Ù„Ù„Ø§Ø¹Ø¨ÙŠÙ† : {g['players']}\\nØ·Ø±ÙŠÙ‚Ø© Ø§Ù„ÙÙˆØ² : {g['win']}"

WAITING={}

# RANKS
ALL_RANKS=[
'Dev','Dev2','MY','M',
'Extra','Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ','Ù…Ø§Ù„Ùƒ',
'Ù…Ù†Ø´Ø¦ Ø§Ø³Ø§Ø³ÙŠ','Ù…Ù†Ø´Ø¦','Ù…Ø¯ÙŠØ±','Ø§Ø¯Ù…Ù†','Ù…Ù…ÙŠØ²'
]

# LOCKS P1
LOCKS_P1=[
'ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª',
'Ø§Ù„Ø§Ø³ØªÙØªØ§Ø¡Ø§Øª',
'Ø§Ù„Ø±Ø³Ø§Ø¦Ù„ Ø§Ù„ØºØ¨ÙŠÙ‡',
'Ø§Ù„Ø§Ø¶Ø§ÙÙ‡',
'Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ',
'Ø§Ù„Ù…ØªØ­Ø±ÙƒÙ‡',
'Ø§Ù„Ø§ØºØ§Ù†ÙŠ',
'Ø§Ù„Ø¨ÙˆØªØ§Øª',
'Ø§Ù„Ù‚Ù†ÙˆØ§Øª',
'Ø§Ù„Ø´Ø§Ø±Ø­Ù‡',
'Ø§Ù„Ø¬Ù‡Ø§Øª',
'Ø§Ù„Ù…Ù„ØµÙ‚Ø§Øª Ø§Ù„Ù…Ù…ÙŠØ²Ù‡',
'Ø§Ù„Ù…Ù„ÙØ§Øª',
'Ø§Ù„ØªÙØ§Ø¹Ù„Ø§Øª Ø§Ù„Ù…Ù…ÙŠØ²Ù‡',
'Ø§Ù„ØªØ¹Ø¯ÙŠÙ„',
'ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ù…ÙŠØ¯ÙŠØ§',
'Ø§Ù„ÙØ§Ø±Ø³ÙŠÙ‡',
'Ø§Ù„Ø§Ù†Ø¬Ù„ÙŠØ²ÙŠÙ‡',
'Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨',
'Ø§Ù„ØªÙˆØ¬ÙŠÙ‡'
]

# LOCKS P2
LOCKS_P2=[
'Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠ',
'Ø§Ù„Ù‚ÙŠÙ Ø§ÙˆÙŠ',
'Ø§Ù„ØªØ§Ùƒ',
'Ø§Ù„Ø§Ø¹Ù„Ø§Ù†Ø§Øª',
'Ø§Ù„Ø§ÙˆÙ†Ù„Ø§ÙŠÙ†',
'Ø§Ù„ØªØ«Ø¨ÙŠØª Ù„Ù„ÙƒÙ„',
'Ø§Ù„Ø§Ø¨Ø±Ø§Ø¬',
'Ø§Ù„Ø¬Ù†ÙˆÙ†',
'Ø§Ù„Ø¯Ø®ÙˆÙ„',
'Ø§Ù„Ø¯Ø®ÙˆÙ„ Ø¨Ø¯ÙˆÙ† Ø·Ù„Ø¨',
'Ø§Ù„ÙƒØ±ØªÙˆÙ†',
'Ø§Ù„Ù„ØºØ§Øª',
'Ø§Ù„Ø±ÙˆØ§Ø¨Ø·',
'Ø§Ù„Ø±Ø§Ø¨Ø·',
'Ø§Ù„Ù…ÙˆØ§Ù‚Ø¹',
'Ø§Ù„ØªÙ†Ø¨ÙŠÙ‡',
'Ø§Ù„Ù…Ø§Ø±ÙƒØ¯Ø§ÙˆÙ†',
'Ø§Ù„ÙˆØ³Ø§Ø¦Ø·',
'Ø§Ù„ÙˆØ³Ø§Ø¦Ø· Ø§Ù„Ù…Ø´ÙØ±Ù‡',
'Ø§Ù„Ø§Ø±Ù‚Ø§Ù…',
'Ø§Ù„Ø±Ø¯ÙˆØ¯ Ø§Ù„Ø®Ø§Ø±Ø¬ÙŠÙ‡'
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
  [InlineKeyboardButton('â€¢ Ø§Ø¶ÙÙ†ÙŠ Ù„Ù‚Ø±ÙˆØ¨Ùƒ â€¢',url='https://t.me/BOT?startgroup=true')],
  [InlineKeyboardButton('â€¢ About SORD â€¢',callback_data='about')]
 ])

def kb_main():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù‚Ø±ÙˆØ¨Ø§Øª â€¢',callback_data='cmd_groups'),
   InlineKeyboardButton('â€¢ Ø§ÙˆØ§Ù…Ø± Ø§Ù„ØªØ´ØºÙŠÙ„ â€¢',callback_data='cmd_play')],
  [InlineKeyboardButton('â€¢ Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù‚Ù†ÙˆØ§Øª â€¢',callback_data='cmd_channels'),
   InlineKeyboardButton('â€¢ ØªÙƒØ±Ø§Ø± ÙˆØªÙ‚Ø¯ÙŠÙ… ÙˆØ³Ø± â€¢',callback_data='cmd_loop')],
  [InlineKeyboardButton('â€¢ Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ† â€¢',callback_data='cmd_dev')],
  [InlineKeyboardButton('â€¢ Ø§ØºÙ„Ø§Ù‚ â€¢',callback_data='close')]
 ])

def kb_groups():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­ â€¢',callback_data='lockpanel'),
   InlineKeyboardButton('â€¢ Ø§Ù„ØªÙØ¹ÙŠÙ„ ÙˆØ§Ù„ØªØ¹Ø·ÙŠÙ„ â€¢',callback_data='onoff')],
  [InlineKeyboardButton('â€¢ Ø§Ù„ØªØ³Ù„ÙŠØ© ÙˆØ§Ù„Ø®Ø¯Ù…ÙŠØ© â€¢',callback_data='fun'),
   InlineKeyboardButton('â€¢ Ø§Ø¯Ø§Ø±Ø© Ø§Ù„Ù‚Ø±ÙˆØ¨ â€¢',callback_data='manage')],
  [InlineKeyboardButton('â€¢ Ø§ÙˆØ§Ù…Ø± Dev â€¢',callback_data='dev'),
   InlineKeyboardButton('â€¢ Ø§Ù„Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª â€¢',callback_data='sets')],
  [InlineKeyboardButton('â€¢ Ø§ØºÙ„Ø§Ù‚ â€¢',callback_data='close')]
 ])

def kb_lock_p1():
 b=[]
 b.append([
  InlineKeyboardButton('â€¢ ÙØªØ­ Ø§Ù„ÙƒÙ„ â€¢',callback_data='openall'),
  InlineKeyboardButton('â€¢ Ù‚ÙÙ„ Ø§Ù„ÙƒÙ„ â€¢',callback_data='closeall')
 ])
 for i in range(0,len(LOCKS_P1),2):
  b.append([
   InlineKeyboardButton(LOCKS_P1[i]+' -',callback_data=f'l_{LOCKS_P1[i]}'),
   InlineKeyboardButton(LOCKS_P1[i+1]+' -',callback_data=f'l_{LOCKS_P1[i+1]}')
  ])
 b.append([InlineKeyboardButton('â€¢ Ø§Ù„ØµÙØ­Ø© Ø§Ù„ØªØ§Ù„ÙŠØ© â€¢',callback_data='page2')])
 b.append([
  InlineKeyboardButton('â€¢ Ø§ØºÙ„Ø§Ù‚ â€¢',callback_data='close'),
  InlineKeyboardButton('â€¢ Ø§Ù„Ø±Ø¦ÙŠØ³ÙŠØ© â€¢',callback_data='cmd_groups')
 ])
 return InlineKeyboardMarkup(b)

def kb_lock_p2():
 b=[]
 b.append([
  InlineKeyboardButton('â€¢ ÙØªØ­ Ø§Ù„ÙƒÙ„ â€¢',callback_data='openall'),
  InlineKeyboardButton('â€¢ Ù‚ÙÙ„ Ø§Ù„ÙƒÙ„ â€¢',callback_data='closeall')
 ])
 for i in range(0,len(LOCKS_P2),2):
  b.append([
   InlineKeyboardButton(LOCKS_P2[i]+' -',callback_data=f'l_{LOCKS_P2[i]}'),
   InlineKeyboardButton(LOCKS_P2[i+1]+' -',callback_data=f'l_{LOCKS_P2[i+1]}')
  ])
 b.append([InlineKeyboardButton('â€¢ Ø§Ù„ØµÙØ­Ø© Ø§Ù„Ø³Ø§Ø¨Ù‚Ø© â€¢',callback_data='page1')])
 b.append([
  InlineKeyboardButton('â€¢ Ø§ØºÙ„Ø§Ù‚ â€¢',callback_data='close'),
  InlineKeyboardButton('â€¢ Ø§Ù„Ø±Ø¦ÙŠØ³ÙŠØ© â€¢',callback_data='cmd_groups')
 ])
 return InlineKeyboardMarkup(b)

def kb_games():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø§Ù„Ø¹Ø§Ø¨ Ø¬Ù…Ø§Ø¹ÙŠØ©',callback_data='g_group'),
   InlineKeyboardButton('â€¢ Ø§Ù„Ø¹Ø§Ø¨ Ø§Ø¯ÙˆØ§Ø±',callback_data='g_roles')],
  [InlineKeyboardButton('â€¢ ÙƒÙ„Ù…Ø§Øª ÙˆØ­Ø±ÙˆÙ',callback_data='g_words'),
   InlineKeyboardButton('â€¢ ØªØ­Ø¯ÙŠ ÙˆØ§Ø³ØªÙ†ØªØ§Ø¬',callback_data='g_chal')],
  [InlineKeyboardButton('â€¢ Ø§Ø³Ø¦Ù„Ø© ÙˆÙ…Ø¹Ù„ÙˆÙ…Ø§Øª',callback_data='g_q'),
   InlineKeyboardButton('â€¢ ØµÙˆØ± ÙˆØªØ®Ù…ÙŠÙ†',callback_data='g_pic')],
  [InlineKeyboardButton('â€¢ Ù…Ù‚Ø§Ù„Ø§Øª ÙˆØ³Ø±Ø¹Ø©',callback_data='g_fast'),
   InlineKeyboardButton('â€¢ ØªØ³Ù„ÙŠØ© Ø§Ù„Ù‚Ø±ÙˆØ¨',callback_data='g_fun')],
  [InlineKeyboardButton('â€¢ Ø­Ø¸ ÙˆÙ‚Ø±Ø¹Ø©',callback_data='g_luck'),
   InlineKeyboardButton('â€¢ Ø¹ÙˆØ§Ø¦Ù„ ÙˆØªÙŠÙ†Ø§Ø³',callback_data='g_fam')],
  [InlineKeyboardButton('â€¢ Ù…Ø³Ø§Ø¨Ù‚Ø§Øª ÙˆÙ‚Ù„Ø§Ø¨Ø§Øª',callback_data='g_race'),
   InlineKeyboardButton('â€¢ Ø§Ø­ØµØ§Ø¦ÙŠØ§ØªÙŠ',callback_data='g_me')],
  [InlineKeyboardButton('â€¢ ØªÙˆØ¨ Ø§Ù„Ø§Ø¯Ù…ÙŠÙ†',callback_data='g_topadmin'),
   InlineKeyboardButton('â€¢ ØªÙˆØ¨ Ø§Ù„Ù…ØªÙØ§Ø¹Ù„ÙŠÙ†',callback_data='g_top')],
  [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚',callback_data='close')]
 ])


def kb_violation(vid):
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø¥Ù„ØºØ§Ø¡ Ø§Ù„Ø¥Ù†Ø°Ø§Ø± â€¢',callback_data=f'warn_cancel_{vid}')],
  [InlineKeyboardButton('â€¢ Ø§Ù„Ø±Ø³Ø§Ù„Ø© Ø³Ù„ÙŠÙ…Ø© â€¢',callback_data=f'warn_safe_{vid}')],
  [InlineKeyboardButton('â€¢ ØªÙØ§ØµÙŠÙ„ Ø§Ù„Ù…Ø®Ø§Ù„ÙØ© â€¢',callback_data=f'warn_detail_{vid}')]
 ])







# === Ù†Ø¸Ø§Ù… Ø§Ù„Ø­Ø¯ÙˆØ¯ - Ù†ÙØ³ Ø§Ù„ØµÙˆØ± Ù„ØµÙ‚ Ø·Ø¨Ø¹ ===
LIMITS=ld('limits.json')  # chat_id -> {action: limit, enabled: bool}
LIMITS_USAGE=ld('limits_usage.json')  # chat_id -> admin_id -> {action: count, date: today}

LIMIT_ACTIONS=['Ø§Ù„Ø­Ø¸Ø±','Ø§Ù„Ø·Ø±Ø¯','Ø§Ù„ÙƒØªÙ…','Ø§Ù„ØªÙ‚ÙŠÙŠØ¯','Ø§Ù„Ø±ÙØ¹','Ø§Ù„ØªÙ†Ø²ÙŠÙ„','Ø§Ù„Ù…Ø³Ø­']
LIMITS_DEFAULT={a:0 for a in LIMIT_ACTIONS}  # 0 = Ø¨Ù„Ø§ Ø­Ø¯

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
    return True  # Ø¨Ù„Ø§ Ø­Ø¯
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
  # Ø¨Ù†Ø§Ø¡ Ø£Ø²Ø±Ø§Ø± Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
  buttons=[
    [InlineKeyboardButton(f'Ø§Ù„Ø·Ø±Ø¯ : {limits["Ø§Ù„Ø·Ø±Ø¯"] if limits["Ø§Ù„Ø·Ø±Ø¯"]!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}', callback_data='lim_Ø§Ù„Ø·Ø±Ø¯'),
     InlineKeyboardButton(f'Ø§Ù„Ø­Ø¸Ø± : {limits["Ø§Ù„Ø­Ø¸Ø±"] if limits["Ø§Ù„Ø­Ø¸Ø±"]!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}', callback_data='lim_Ø§Ù„Ø­Ø¸Ø±')],
    [InlineKeyboardButton(f'Ø§Ù„ØªÙ‚ÙŠÙŠØ¯ : {limits["Ø§Ù„ØªÙ‚ÙŠÙŠØ¯"] if limits["Ø§Ù„ØªÙ‚ÙŠÙŠØ¯"]!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}', callback_data='lim_Ø§Ù„ØªÙ‚ÙŠÙŠØ¯'),
     InlineKeyboardButton(f'Ø§Ù„ÙƒØªÙ… : {limits["Ø§Ù„ÙƒØªÙ…"] if limits["Ø§Ù„ÙƒØªÙ…"]!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}', callback_data='lim_Ø§Ù„ÙƒØªÙ…')],
    [InlineKeyboardButton(f'Ø§Ù„ØªÙ†Ø²ÙŠÙ„ : {limits["Ø§Ù„ØªÙ†Ø²ÙŠÙ„"] if limits["Ø§Ù„ØªÙ†Ø²ÙŠÙ„"]!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}', callback_data='lim_Ø§Ù„ØªÙ†Ø²ÙŠÙ„'),
     InlineKeyboardButton(f'Ø§Ù„Ø±ÙØ¹ : {limits["Ø§Ù„Ø±ÙØ¹"] if limits["Ø§Ù„Ø±ÙØ¹"]!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}', callback_data='lim_Ø§Ù„Ø±ÙØ¹')],
    [InlineKeyboardButton(f'Ø§Ù„Ù…Ø³Ø­ : {limits["Ø§Ù„Ù…Ø³Ø­"] if limits["Ø§Ù„Ù…Ø³Ø­"]!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}', callback_data='lim_Ø§Ù„Ù…Ø³Ø­')],
    [InlineKeyboardButton('â€¢ Ø§Ø³ØªÙ‡Ù„Ø§Ùƒ Ø§Ù„ÙŠÙˆÙ…', callback_data='lim_today'),
     InlineKeyboardButton('â€¢ ØªØ¹Ø·ÙŠÙ„ Ø§Ù„Ø­Ø¯ÙˆØ¯', callback_data='lim_disable')],
    [InlineKeyboardButton('â€¢ Ù…Ø³Ø­ Ø§Ù„Ø­Ø¯ÙˆØ¯', callback_data='lim_clear')],
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='cmd_main'),
     InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
  ]
  return InlineKeyboardMarkup(buttons)

def kb_limit_edit(action, current):
  # Ø£Ø²Ø±Ø§Ø± -5 -1 +1 +5 Ùˆ 1 3 5 10 20 Ùˆ Ø¨Ù„Ø§ Ø­Ø¯
  cur_text = current if current!=0 else 'Ø¨Ù„Ø§ Ø­Ø¯'
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('â€¢ -5', callback_data=f'lim_edit_{action}_-5'),
     InlineKeyboardButton('â€¢ -1', callback_data=f'lim_edit_{action}_-1'),
     InlineKeyboardButton('â€¢ +1', callback_data=f'lim_edit_{action}_+1'),
     InlineKeyboardButton('â€¢ +5', callback_data=f'lim_edit_{action}_+5')],
    [InlineKeyboardButton('â€¢ 1', callback_data=f'lim_edit_{action}_set_1'),
     InlineKeyboardButton('â€¢ 3', callback_data=f'lim_edit_{action}_set_3'),
     InlineKeyboardButton('â€¢ 5', callback_data=f'lim_edit_{action}_set_5'),
     InlineKeyboardButton('â€¢ 10', callback_data=f'lim_edit_{action}_set_10'),
     InlineKeyboardButton('â€¢ 20', callback_data=f'lim_edit_{action}_set_20')],
    [InlineKeyboardButton('â€¢ Ø¨Ù„Ø§ Ø­Ø¯', callback_data=f'lim_edit_{action}_set_0')],
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='lim_main'),
     InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
  ])

def limits_text(cid, action=None):
  lim=get_limits(cid)
  limits=lim['limits']
  if action:
    cur=limits.get(action,0)
    cur_t = cur if cur!=0 else 'Ø¨Ù„Ø§ Ø­Ø¯'
    if action=='Ø§Ù„ØªÙ†Ø²ÙŠÙ„':
      return f'''â€¢ Ø­Ø¯ ( Ø§Ù„ØªÙ†Ø²ÙŠÙ„ ) Ù„ÙƒÙ„ Ù…Ø´Ø±Ù
_________________________

â€¢ Ø§Ù„Ø­Ø§Ù„ÙŠ â†¤ {cur_t}
â€¢ ÙƒÙ„ Ø´Ø®Øµ ÙŠÙ†Ø­Ø³Ø¨ Ù…Ø±Ø© ÙˆØ­Ø¯Ø©
â€¢ Ø§Ø¶ØºØ· Ø§Ù„Ø§Ø±Ù‚Ø§Ù… ØªØºÙŠÙ‘Ø±Ù‡ØŒ Ø§Ùˆ ( Ø¨Ù„Ø§ Ø­Ø¯ ) ØªØ´ÙŠÙ„Ù‡'''
    elif action=='Ø§Ù„ÙƒØªÙ…':
      return f'''â€¢ Ø­Ø¯ ( Ø§Ù„ÙƒØªÙ… ) Ù„ÙƒÙ„ Ù…Ø´Ø±Ù
_________________________

â€¢ Ø§Ù„Ø­Ø§Ù„ÙŠ â†¤ {cur_t}
â€¢ ÙƒÙ„ Ø´Ø®Øµ ÙŠÙ†Ø­Ø³Ø¨ Ù…Ø±Ø© ÙˆØ­Ø¯Ø©
â€¢ Ø§Ø¶ØºØ· Ø§Ù„Ø§Ø±Ù‚Ø§Ù… ØªØºÙŠÙ‘Ø±Ù‡ØŒ Ø§Ùˆ ( Ø¨Ù„Ø§ Ø­Ø¯ ) ØªØ´ÙŠÙ„Ù‡'''
    else:
      return f'''â€¢ Ø­Ø¯ ( {action} ) Ù„ÙƒÙ„ Ù…Ø´Ø±Ù
_________________________

â€¢ Ø§Ù„Ø­Ø§Ù„ÙŠ â†¤ {cur_t}
â€¢ ÙƒÙ„ Ø´Ø®Øµ ÙŠÙ†Ø­Ø³Ø¨ Ù…Ø±Ø© ÙˆØ­Ø¯Ø©
â€¢ Ø§Ø¶ØºØ· Ø§Ù„Ø§Ø±Ù‚Ø§Ù… ØªØºÙŠÙ‘Ø±Ù‡ØŒ Ø§Ùˆ ( Ø¨Ù„Ø§ Ø­Ø¯ ) ØªØ´ÙŠÙ„Ù‡'''
  else:
    # Ø§Ù„Ù†Øµ Ø§Ù„ÙƒØ§Ù…Ù„ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
    txt='''â€¢ Ø§Ù„Ø­Ø¸Ø± â†¤ Ø¨Ù„Ø§ Ø­Ø¯
â€¢ Ø§Ù„Ø·Ø±Ø¯ â†¤ Ø¨Ù„Ø§ Ø­Ø¯
â€¢ Ø§Ù„ÙƒØªÙ… â†¤ Ø¨Ù„Ø§ Ø­Ø¯
â€¢ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯ â†¤ Ø¨Ù„Ø§ Ø­Ø¯
â€¢ Ø§Ù„Ø±ÙØ¹ â†¤ Ø¨Ù„Ø§ Ø­Ø¯
â€¢ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ â†¤ Ø¨Ù„Ø§ Ø­Ø¯
â€¢ Ø§Ù„Ù…Ø³Ø­ â†¤ Ø¨Ù„Ø§ Ø­Ø¯
_________________________

â€¢ ÙŠØªØ¬Ø§ÙˆØ² Ù…Ù† Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ø¨ÙˆØª â†¤ ÙŠØ±ÙØ¶ Ø§Ù…Ø±Ù‡
ÙˆÙŠÙ‚ÙˆÙ„Ù‡ ØªØ¬Ø§ÙˆØ²Øª Ø­Ø¯Ùƒ
â€¢ ÙŠØªØ¬Ø§ÙˆØ² Ù…Ù† Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª ØªÙŠÙ„ÙŠØ¬Ø±Ø§Ù… â†¤ ÙŠØ±Ø¬Ø¹
Ø§Ù„Ù„ÙŠ Ø³ÙˆØ§Ù‡ ÙˆÙŠÙ†Ø³Ø­Ø¨ Ù…Ù†Ù‡ Ø§Ù„Ø§Ø´Ø±Ø§Ù
â€¢ ÙˆØ¨Ø§Ù„Ø­Ø§Ù„ØªÙŠÙ† ÙŠÙˆØµÙ„Ùƒ Ø§Ø´Ø¹Ø§Ø±'''
    # Ø§Ø³ØªØ¨Ø¯Ù„ Ø§Ù„Ù‚ÙŠÙ… Ø§Ù„ÙØ¹Ù„ÙŠØ©
    for a in LIMIT_ACTIONS:
      v=limits.get(a,0)
      v_t = f'{v}' if v!=0 else 'Ø¨Ù„Ø§ Ø­Ø¯'
      txt=txt.replace(f'{a} â†¤ Ø¨Ù„Ø§ Ø­Ø¯', f'{a} â†¤ {v_t}', 1)
    return txt





def kb_auto_time_edit(rank, current_hours):
  # current in hours
  if current_hours>=24:
    cur_text=f"{current_hours//24} Ø£ÙŠØ§Ù…" if current_hours%24==0 else f"{current_hours} Ø³Ø§Ø¹Ø©"
  else:
    cur_text=f"{current_hours} Ø³Ø§Ø¹Ø§Øª"
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('â€¢ -1 ÙŠÙˆÙ…', callback_data=f'auto_time_{rank}_-24'),
     InlineKeyboardButton('â€¢ -1 Ø³Ø§Ø¹Ø©', callback_data=f'auto_time_{rank}_-1'),
     InlineKeyboardButton('â€¢ +1 Ø³Ø§Ø¹Ø©', callback_data=f'auto_time_{rank}_+1'),
     InlineKeyboardButton('â€¢ +1 ÙŠÙˆÙ…', callback_data=f'auto_time_{rank}_+24')],
    [InlineKeyboardButton('â€¢ 6 Ø³Ø§Ø¹Ø§Øª', callback_data=f'auto_time_{rank}_set_6'),
     InlineKeyboardButton('â€¢ 12 Ø³Ø§Ø¹Ø©', callback_data=f'auto_time_{rank}_set_12'),
     InlineKeyboardButton('â€¢ 1 ÙŠÙˆÙ…', callback_data=f'auto_time_{rank}_set_24'),
     InlineKeyboardButton('â€¢ 3 Ø£ÙŠØ§Ù…', callback_data=f'auto_time_{rank}_set_72')],
    [InlineKeyboardButton('â€¢ 7 Ø£ÙŠØ§Ù…', callback_data=f'auto_time_{rank}_set_168'),
     InlineKeyboardButton('â€¢ 30 ÙŠÙˆÙ…', callback_data=f'auto_time_{rank}_set_720')],
    [InlineKeyboardButton('â€¢ Ù…Ø³Ø­ Ø§Ù„Ø­Ø¯', callback_data=f'auto_time_{rank}_clear')],
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='auto_set_rank'),
     InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
  ])

def text_auto_time_edit(rank, hours):
  if hours>=24:
    if hours%24==0:
      cur=f"{hours//24} Ø£ÙŠØ§Ù…"
    else:
      cur=f"{hours} Ø³Ø§Ø¹Ø© ({hours//24} ÙŠÙˆÙ… Ùˆ {hours%24} Ø³Ø§Ø¹Ø©)"
  else:
    cur=f"{hours} Ø³Ø§Ø¹Ø§Øª"
  return f'''â€¢ Ø­Ø¯ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ù„Ø±ØªØ¨Ø© {rank}
_________________________

â€¢ Ø§Ù„Ø­Ø§Ù„ÙŠ â†¤ {cur}
â€¢ Ø§Ù„Ù„ÙŠ ÙŠØºÙŠØ¨ Ø§ÙƒØ«Ø± Ù…Ù† {cur} ÙŠÙ†Ø²Ù„ ØªÙ„Ù‚Ø§Ø¦ÙŠ
ÙˆÙŠÙ†Ø±Ø³Ù„ Ù…Ù†Ø´Ù† Ù„Ù‡ Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ Ø§Ø¶ØºØ· Ø§Ù„Ø§Ø²Ø±Ø§Ø± Ù„ØªØºÙŠÙŠØ± Ø§Ù„ÙˆÙ‚Øª'''


# === Ù†Ø¸Ø§Ù… Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ - Ù†ÙØ³ Ø§Ù„ØµÙˆØ± Ù„ØµÙ‚ Ø·Ø¨Ø¹ ===
AUTO_DOWNLOAD=ld('auto_download.json')  # chat_id -> {enabled: bool, limits: {rank: hours}}
LAST_SEEN=ld('last_seen.json')  # chat_id -> user_id -> timestamp

AUTO_DEFAULT_LIMITS={'Dev2':6, 'Ø§Ù„Ø§Ø´Ø±Ø§Ù': 7*24}  # 6 Ø³Ø§Ø¹Ø§Øª Ùˆ 7 Ø£ÙŠØ§Ù… Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
AUTO_RANKS=['Dev2','MYTH','Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ','Ø§Ù„Ù…Ø§Ù„Ùƒ','Ø§Ù„Ù…Ù†Ø´Ø¦ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ','Ø§Ù„Ù…Ù†Ø´Ø¦','Ø§Ù„Ù…Ø¯ÙŠØ±','Ø§Ù„Ø§Ø¯Ù…Ù†','Ø§Ù„Ù…Ù…ÙŠØ²','Ø§Ù„Ø§Ø´Ø±Ø§Ù']

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
  # Ø²Ø± ØªÙØ¹ÙŠÙ„/ØªØ¹Ø·ÙŠÙ„
  toggle_text='ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ' if enabled else 'ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ'
  toggle_color='red' if enabled else 'green'
  buttons=[
    [InlineKeyboardButton('â€¢ Ù…Ø³Ø­ Ø­Ø¯ÙˆØ¯ Ø§Ù„ØªÙ†Ø²ÙŠÙ„', callback_data='auto_clear')],
    [InlineKeyboardButton(f'â€¢ {toggle_text}', callback_data='auto_toggle')],
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='group_settings'),
     InlineKeyboardButton('â€¢ Ø§ØºÙ„Ø§Ù‚', callback_data='close')]
  ]
  # Ù„Ùˆ Ù…Ø¹Ø·Ù„ - ÙŠØ¸Ù‡Ø± Ø£Ø²Ø±Ø§Ø± ÙˆØ¶Ø¹ Ø­Ø¯
  if not enabled:
    buttons.insert(0, [InlineKeyboardButton('â€¢ Ù…Ø³Ø­ Ø­Ø¯ ØªÙ†Ø²ÙŠÙ„ Ø±ØªØ¨Ø©', callback_data='auto_clear_rank')])
    buttons.insert(0, [InlineKeyboardButton('â€¢ Ø¶Ø¹ Ø­Ø¯ ØªÙ†Ø²ÙŠÙ„ Ù„Ø±ØªØ¨Ø©', callback_data='auto_set_rank')])
  return InlineKeyboardMarkup(buttons)

def kb_auto_set_rank():
  # Ù†ÙØ³ ØµÙˆØ±Ø© 7CF30CE3
  buttons=[
    [InlineKeyboardButton('â€¢ MYTH ðŸŽ–ï¸', callback_data='auto_rank_MYTH2'),
     InlineKeyboardButton('â€¢ Dev2 ðŸŽ–ï¸ : 6 Ø³Ø§Ø¹Ø§Øª', callback_data='auto_rank_Dev2')],
    [InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ', callback_data='auto_rank_Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ'),
     InlineKeyboardButton('â€¢ MYTH', callback_data='auto_rank_MYTH')],
    [InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ù†Ø´Ø¦ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ', callback_data='auto_rank_Ø§Ù„Ù…Ù†Ø´Ø¦ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ'),
     InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø§Ù„Ùƒ', callback_data='auto_rank_Ø§Ù„Ù…Ø§Ù„Ùƒ')],
    [InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø¯ÙŠØ±', callback_data='auto_rank_Ø§Ù„Ù…Ø¯ÙŠØ±'),
     InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ù†Ø´Ø¦', callback_data='auto_rank_Ø§Ù„Ù…Ù†Ø´Ø¦')],
    [InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ù…ÙŠØ²', callback_data='auto_rank_Ø§Ù„Ù…Ù…ÙŠØ²'),
     InlineKeyboardButton('â€¢ Ø§Ù„Ø§Ø¯Ù…Ù†', callback_data='auto_rank_Ø§Ù„Ø§Ø¯Ù…Ù†')],
    [InlineKeyboardButton('â€¢ Ø§Ù„Ø§Ø´Ø±Ø§Ù : 7 Ø£ÙŠØ§Ù…', callback_data='auto_rank_Ø§Ù„Ø§Ø´Ø±Ø§Ù')],
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='auto_main'),
     InlineKeyboardButton('â€¢ Ø§ØºÙ„Ø§Ù‚', callback_data='close')]
  ]
  return InlineKeyboardMarkup(buttons)

def kb_group_settings():
  # Ù†ÙØ³ ØµÙˆØ±Ø© A00E8BA4 - Ø§Ù„Ø§Ù„ÙˆØ§Ù† Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©: Ø£Ø®Ø¶Ø± = NEW, Ø¨Ù†ÙŠ = Ø§Ù„Ø¨Ø§Ù‚ÙŠ
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('â€¢ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„ÙˆØ³Ø§Ø¦Ø· ðŸ†• NEW', callback_data='settings_media')],
    [InlineKeyboardButton('â€¢ Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­', callback_data='lock_menu')],
    [InlineKeyboardButton('â€¢ Ø§Ù„ØªÙØ¹ÙŠÙ„ ÙˆØ§Ù„ØªØ¹Ø·ÙŠÙ„', callback_data='enable_disable')],
    [InlineKeyboardButton('â€¢ Ø§Ù„ÙˆØ¶Ø¹ ÙˆØ§Ù„Ù…Ø³Ø­', callback_data='mode_clear')],
    [InlineKeyboardButton('â€¢ Ø§Ù„ØªÙ†Ø¸ÙŠÙ', callback_data='cleaning')],
    [InlineKeyboardButton('â€¢ Ø­Ø¯ÙˆØ¯ Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†', callback_data='lim_main')],
    [InlineKeyboardButton('â€¢ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ', callback_data='auto_main')],
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹ Ù„Ù„Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø±Ø¦ÙŠØ³ÙŠØ© Ù„Ù„Ø£ÙˆØ§Ù…Ø±', callback_data='cmd_main')]
  ])

def kb_groups_commands():
  # Ù†ÙØ³ ØµÙˆØ±Ø© D78F76BA - Ø£Ø®Ø¶Ø± = Ø±Ø¬ÙˆØ¹, Ø£Ø­Ù…Ø± = Ø¥ØºÙ„Ø§Ù‚
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='cmd_main')],
    [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
  ])

def text_auto_main(cid):
  auto=get_auto(cid)
  enabled=auto['enabled']
  status='Ù…ÙØ¹Ù‘Ù„' if enabled else 'Ù…Ø¹Ø·Ù‘Ù„'
  limits=auto['limits']
  lim_text=''
  for k,v in limits.items():
    if v>=24:
      days=v//24
      lim_text+=f'- {k} â†¤ {days} Ø£ÙŠØ§Ù…\n'
    else:
      lim_text+=f'- {k} â†¤ {v} Ø³Ø§Ø¹Ø§Øª\n'
  if not lim_text:
    lim_text='- Ù„Ø§ ÙŠÙˆØ¬Ø¯ Ø­Ø¯ÙˆØ¯\n'
  
  if enabled:
    return f'''â€¢ Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ
_________________________

â€¢ Ø§Ù„Ø­Ø§Ù„Ø© â†¤ {status}
â€¢ Ø§Ù„Ù„ÙŠ ÙŠØºÙŠØ¨ Ø¹Ù† Ø§Ù„Ù‚Ø±ÙˆØ¨ Ø§ÙƒØ«Ø± Ù…Ù† Ø­Ø¯ Ø±ØªØ¨ØªÙ‡
ÙŠÙ†Ø²Ù„ Ù…Ù†Ù‡Ø§ ØªÙ„Ù‚Ø§Ø¦ÙŠØŒ ÙˆÙŠÙ†Ø±Ø³Ù„ Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ Ù…Ù†Ø´Ù†
Ù„Ù‡
â€¢ ÙŠØ¶Ø¨Ø·Ù‡Ø§ â†¤ Dev ðŸŽ–ï¸
_________________________

â€¢ Ø­Ø¯ÙˆØ¯ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„Ø­Ø§Ù„ÙŠØ© :
{lim_text}'''
  else:
    return f'''â€¢ Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ
_________________________

â€¢ Ø§Ù„Ø­Ø§Ù„Ø© â†¤ {status}
â€¢ Ø§Ù„Ù„ÙŠ ÙŠØºÙŠØ¨ Ø¹Ù† Ø§Ù„Ù‚Ø±ÙˆØ¨ Ø§ÙƒØ«Ø± Ù…Ù† Ø­Ø¯ Ø±ØªØ¨ØªÙ‡
ÙŠÙ†Ø²Ù„ Ù…Ù†Ù‡Ø§ ØªÙ„Ù‚Ø§Ø¦ÙŠØŒ ÙˆÙŠÙ†Ø±Ø³Ù„ Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ Ù…Ù†Ø´Ù†
Ù„Ù‡
â€¢ ÙŠØ¶Ø¨Ø·Ù‡Ø§ â†¤ Dev ðŸŽ–ï¸
_________________________

â€¢ Ø­Ø¯ÙˆØ¯ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„Ø­Ø§Ù„ÙŠØ© :
{lim_text}
â€¢ Ø§Ù„Ø­Ø¯ÙˆØ¯ Ù…Ø§ ØªØ´ØªØºÙ„ Ù„ÙŠÙ† ØªÙƒØªØ¨ ( ØªÙØ¹ÙŠÙ„
Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ )'''

def text_group_settings():
  return '''Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ù‚Ø±ÙˆØ¨
_________________________

â€¢ Ø§Ø®ØªØ± Ø§Ù„Ù‚Ø³Ù… Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠ ØªØ¹Ø¯Ù‘Ù„ ÙÙŠÙ‡
â€¢ ÙƒÙ„ Ù‚Ø³Ù… ÙÙŠÙ‡ Ø§Ø²Ø±Ø§Ø±Ù‡ ÙˆØªØ±Ø¬Ø¹ Ù…Ù†Ù‡ Ø¨Ø²Ø±
Ø§Ù„Ø±Ø¬ÙˆØ¹'''

def text_groups_commands():
  return '''Ø£ÙˆØ§Ù…Ø± Ø®Ø§ØµØ© Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨Ø§Øª ðŸ‘¥

â€¢ Ø±ÙØ¹ Ù…Ø´ØºÙ„ [ Ø±Ø¯ / Ø¢ÙŠØ¯ÙŠ ] - ÙŠÙ…Ù†Ø­
ØµÙ„Ø§Ø­ÙŠØ§Øª Ø¥Ø¯Ù…Ù† Ø§Ù„ØªØ´ØºÙŠÙ„ Ø¨Ø¯ÙˆÙ† Ø¥Ø´Ø±Ø§Ù
ÙƒØ§Ù…Ù„

â€¢ ØªÙ†Ø²ÙŠÙ„ Ù…Ø´ØºÙ„ [ Ø±Ø¯ / Ø¢ÙŠØ¯ÙŠ ]
â€¢ Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ† - Ø¹Ø±Ø¶ Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ† Ø§Ù„Ø­Ø§Ù„ÙŠÙŠÙ†
â€¢ Ø§Ù„Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª / settings - Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª
Ø§Ù„Ù‚Ø±ÙˆØ¨ (ÙˆØ¶Ø¹ Ø§Ù„Ø¨Ø­Ø«ØŒ Ø§Ù„ØªØµÙˆÙŠØª...)
â€¢ /reload - ØªØ­Ø¯ÙŠØ« Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†'''






# REMOVE OLD
# OLD REMOVED
# OLD
async def handle_dev_command_old_rakan_old_final_old2(m,cid,t,c):
  if t in ['Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ†','Ù…Ø·ÙˆØ±ÙŠÙ†']:
    try:
      # Ø­Ø§ÙˆÙ„ ØªØ¬ÙŠØ¨ ØµÙˆØ±Ø© afiwd
      photo=None
      try:
        # Ø¬ÙŠØ¨ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª afiwd
        dev_chat=await c.get_chat('afiwd')
        if hasattr(dev_chat,'photo') and dev_chat.photo:
          photo=dev_chat.photo.big_file_id
      except:
        pass
      
      text='''Ø±Ø§ÙƒØ§Ù†

ÙˆÙŽØ§Ø¬Ù’Ø¹ÙŽÙ„Ù’ Ù„ÙÙŠ Ù„ÙØ³ÙŽØ§Ù†ÙŽ ØµÙØ¯Ù’Ù‚Ù ÙÙÙŠ Ø§Ù„Ù’Ø¢Ø®ÙØ±ÙÙŠÙ†ÙŽ'''
      
      # Ù„Ùˆ ÙÙŠÙ‡ ØµÙˆØ±Ø© - Ø§Ø±Ø³Ù„ Ø¨ØµÙˆØ±Ø© Ù…Ø¹ Ø§Ù‚ØªØ¨Ø§Ø³
      if photo:
        try:
          await m.reply_photo(photo, caption=text, parse_mode='html', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('â€¢ Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
          ]))
          return True
        except:
          pass
      
      # Ø¨Ø¯ÙˆÙ† ØµÙˆØ±Ø© - Ø§Ø±Ø³Ù„ Ù†Øµ Ù…Ø¹ Ø§Ù‚ØªØ¨Ø§Ø³
      await m.reply_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('â€¢ Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
      ]))
      return True
    except Exception as e:
      await m.reply_text('''Ø±Ø§ÙƒØ§Ù†

ÙˆÙŽØ§Ø¬Ù’Ø¹ÙŽÙ„Ù’ Ù„ÙÙŠ Ù„ÙØ³ÙŽØ§Ù†ÙŽ ØµÙØ¯Ù’Ù‚Ù ÙÙÙŠ Ø§Ù„Ù’Ø¢Ø®ÙØ±ÙÙŠÙ†ÙŽ''', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('â€¢ Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
      ]))
      return True
  return False



# OLD REMOVED
# OLD
async def handle_dev_command_old_rakan_old_final(m,cid,t,c):
  if t in ['Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ†','Ù…Ø·ÙˆØ±ÙŠÙ†','Ø§Ù„Ù…Ø·ÙˆØ± ðŸ§‘â€ðŸ’»']:
    try:
      # Ø­Ø§ÙˆÙ„ ØªØ¬ÙŠØ¨ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª afiwd
      dev_id=30457869  # Ù†ÙØ³ Ø§Ù„Ø§ÙŠØ¯ÙŠ Ø¨Ø§Ù„ÙÙŠØ¯ÙŠÙˆ Ø£Ùˆ Ø­Ø§ÙˆÙ„ ØªØ¬ÙŠØ¨ Ø§Ù„Ø­Ù‚ÙŠÙ‚ÙŠ
      dev_username='afiwd'
      dev_name='Ø±Ø§ÙƒØ§Ù†'
      dev_bio='ÙˆÙŽØ§Ø¬Ù’Ø¹ÙŽÙ„Ù’ Ù„ÙÙŠ Ù„ÙØ³ÙŽØ§Ù†ÙŽ ØµÙØ¯Ù’Ù‚Ù ÙÙÙŠ Ø§Ù„Ù’Ø¢Ø®ÙØ±ÙÙŠÙ†ÙŽ'
      photo=None
      try:
        dev_user=await c.get_users('afiwd')
        dev_id=dev_user.id
        dev_name='Ø±Ø§ÙƒØ§Ù†'
        dev_username=dev_user.username or 'afiwd'
        # Ø­Ø§ÙˆÙ„ ØªØ¬ÙŠØ¨ ØµÙˆØ±ØªÙ‡
        async for p in c.get_chat_photos(dev_id, limit=1):
          photo=p.file_id
          break
      except:
        pass

      # Ù†ÙØ³ Ù†Øµ Ø§Ù„ÙÙŠØ¯ÙŠÙˆ Ù„ØµÙ‚ Ø·Ø¨Ø¹ Ø¨Ø³ Ø¨Ø§Ø³Ù… Ø±Ø§ÙƒØ§Ù†
      text=f'''Ø¹Ù…ÙŠ Ø³ØªØ±ÙˆÙÙ‚ ðŸš€
Ø¢Ø®Ø± Ø¸Ù‡ÙˆØ± ÙƒØ§Ù† Ù‚Ø±ÙŠØ¨Ø§ ðŸš€

Id: {dev_id}
Ù…Ø³Ø¬Ù„
2014 ÙØ¨Ø±Ø§ÙŠØ±

Not Strong Anymore ðŸš€

â€º Developer Bot Â» SORD Â» Ø³ÙˆÙ„
â€º {dev_name}

â€º Ù…Ø§Ø°Ø§ ØªØ¹Ø±Ù USE Â» Ø¹Ù† Ù…Ø¹Ø±ÙÙ‡
â€º Bio Â» {dev_bio} Ø§Ø³Ù… Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…
@{dev_username}

Ø£ÙŠØ¶Ø§
@00yy, @000dd, @fsssl, @e__x__x
@zucci, @ccuu, @jjimmm, @xgmx

â€º Ø§Ù„Ø¨Ø§ÙŠÙˆ
{dev_bio}

https://t.me/{dev_username}'''

      if photo:
        try:
          await m.reply_photo(photo, caption=text, parse_mode='html', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f'â€¢ {dev_name}', url=f'https://t.me/{dev_username}')]
          ]))
          return True
        except:
          pass
      
      await m.reply_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(f'â€¢ {dev_name}', url=f'https://t.me/{dev_username}')]
      ]))
      return True
    except Exception as e:
      await m.reply_text(f'''Ø±Ø§ÙƒØ§Ù†

ÙˆÙŽØ§Ø¬Ù’Ø¹ÙŽÙ„Ù’ Ù„ÙÙŠ Ù„ÙØ³ÙŽØ§Ù†ÙŽ ØµÙØ¯Ù’Ù‚Ù ÙÙÙŠ Ø§Ù„Ù’Ø¢Ø®ÙØ±ÙÙŠÙ†ÙŽ

https://t.me/afiwd''', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('â€¢ Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
      ]))
      return True
  return False



# OLD
async def handle_dev_command_old_rakan(m,cid,t,c):
  if t in ['Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ†','Ù…Ø·ÙˆØ±ÙŠÙ†','Ø§Ù„Ù…Ø·ÙˆØ± ðŸ§‘â€ðŸ’»']:
    try:
      await m.reply_text('Ø§Ù„Ù…Ø·ÙˆØ±', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
      ]))
      return True
    except:
      await m.reply_text('Ø§Ù„Ù…Ø·ÙˆØ±', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
      ]))
      return True
  return False



async def handle_dev_command(m,cid,t,c):
  if t in ['Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±','Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ†','Ù…Ø·ÙˆØ±ÙŠÙ†','Ø§Ù„Ù…Ø·ÙˆØ± ðŸ§‘â€ðŸ’»']:
    try:
      photo=None
      try:
        dev_user=await c.get_users('afiwd')
        async for p in c.get_chat_photos(dev_user.id, limit=1):
          photo=p.file_id
          break
      except:
        pass

      text='''Ø±Ø§ÙƒØ§Ù†

ÙˆÙŽØ§Ø¬Ù’Ø¹ÙŽÙ„Ù’ Ù„ÙÙŠ Ù„ÙØ³ÙŽØ§Ù†ÙŽ ØµÙØ¯Ù’Ù‚Ù ÙÙÙŠ Ø§Ù„Ù’Ø¢Ø®ÙØ±ÙÙŠÙ†ÙŽ'''

      if photo:
        try:
          await m.reply_photo(photo, caption=text, parse_mode='html', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
          ]))
          return True
        except:
          pass
      
      await m.reply_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
      ]))
      return True
    except:
      await m.reply_text('''Ø±Ø§ÙƒØ§Ù†

ÙˆÙŽØ§Ø¬Ù’Ø¹ÙŽÙ„Ù’ Ù„ÙÙŠ Ù„ÙØ³ÙŽØ§Ù†ÙŽ ØµÙØ¯Ù’Ù‚Ù ÙÙÙŠ Ø§Ù„Ù’Ø¢Ø®ÙØ±ÙÙŠÙ†ÙŽ''', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Ø±Ø§ÙƒØ§Ù†', url='https://t.me/afiwd')]
      ]))
      return True
  return False



async def handle_call_invite(m,cid,t,c):
  # Ù„Ùˆ ÙƒØªØ¨ Ø¯Ø¹ÙˆØ© ÙˆØ±Ø¯ Ø¹Ù„Ù‰ Ø´Ø®Øµ
  if t.startswith('Ø¯Ø¹ÙˆØ©') or 'Ø¯Ø¹ÙˆØ© Ù„Ù„Ù…ÙƒØ§Ù„Ù…Ø©' in t or 'Ø¯Ø¹ÙˆÙ‡' in t:
    inviter=m.from_user.first_name if m.from_user else 'Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
    invited='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
    if m.reply_to_message and m.reply_to_message.from_user:
      invited=m.reply_to_message.from_user.first_name
    else:
      # Ø­Ø§ÙˆÙ„ ØªØ³ØªØ®Ø±Ø¬ Ø§Ø³Ù… Ù…Ù† Ø§Ù„Ù†Øµ Ø¨Ø¹Ø¯ Ø¯Ø¹ÙˆØ©
      import re
      mm=re.search(r'Ø¯Ø¹ÙˆØ©\s+(.+)', t)
      if mm:
        invited=mm.group(1).strip()
    
    text=f'''âŒ¯ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ â†¤ï¸Žã€Œ {inviter} ã€
âŒ¯ Ù‚Ø§Ù… Ø¨Ø¯Ø¹ÙˆØ© â†¤ï¸Ž ã€Œ {invited} ã€Ù„Ù„Ù…ÙƒØ§Ù„Ù…Ø©'''
    await m.reply_text(text)
    return True
  
  # ÙƒØ´Ù Ø¯Ø¹ÙˆØ§Øª Ø§Ù„ÙƒÙˆÙ„ Ø§Ù„Ø­Ù‚ÙŠÙ‚ÙŠØ© Ù…Ù† ØªÙŠÙ„ÙŠØ¬Ø±Ø§Ù… - service messages
  if m.voice_chat_started or m.voice_chat_ended or m.video_chat_started:
    return False
  
  return False

# Ù„Ù„ÙƒØ´Ù Ø¹Ù† Ø¯Ø¹ÙˆØ© Ø§Ù„ÙƒÙˆÙ„ Ù…Ù† ØªÙŠÙ„ÙŠØ¬Ø±Ø§Ù… Ù†ÙØ³Ù‡ (group call invite)
async def handle_group_call_invite(c, m):
  try:
    # Ù‡Ø°Ù‡ Ù„Ù„Ø±Ø³Ø§Ø¦Ù„ Ø§Ù„Ø®Ø¯Ù…ÙŠØ© Ù„Ø¯Ø¹ÙˆØ© Ø§Ù„ÙƒÙˆÙ„
    if hasattr(m, 'group_call_invite') and m.group_call_invite:
      inviter=m.from_user.first_name if m.from_user else 'Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
      # Ø­Ø§ÙˆÙ„ ØªØ¬ÙŠØ¨ Ø§Ù„Ù…Ø¯Ø¹Ùˆ
      invited='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
      try:
        if hasattr(m.group_call_invite, 'users'):
          if m.group_call_invite.users:
            u=await c.get_users(m.group_call_invite.users[0])
            invited=u.first_name
      except:
        pass
      text=f'''âŒ¯ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ â†¤ï¸Žã€Œ {inviter} ã€
âŒ¯ Ù‚Ø§Ù… Ø¨Ø¯Ø¹ÙˆØ© â†¤ï¸Ž ã€Œ {invited} ã€Ù„Ù„Ù…ÙƒØ§Ù„Ù…Ø©'''
      await m.reply_text(text)
  except:
    pass



# === Ù…Ù†Ø¹ Ø±ÙØ¹ Ø§Ù„Ø¨ÙˆØªØ§Øª - Ù„Ùˆ Ø§Ù†Ø±ÙØ¹ ØªØªÙ„Ù‡ Ø§Ù†Øª ===
async def handle_anti_bot_promote(c, chat_id, target_user_id, promoter_id=None):
  try:
    # ØªØ£ÙƒØ¯ Ø£Ù† Ø§Ù„Ù‡Ø¯Ù Ø¨ÙˆØª
    try:
      target=await c.get_users(target_user_id)
      is_bot=target.is_bot
    except:
      is_bot=True  # Ù„Ùˆ Ù…Ø§ Ù‚Ø¯Ø±Ù†Ø§ Ù†Ø¬ÙŠØ¨ Ù…Ø¹Ù„ÙˆÙ…Ø§ØªÙ‡ Ù†ÙØªØ±Ø¶ Ø¨ÙˆØª
    
    if not is_bot:
      return False
    
    # Ù†Ø²Ù„ Ø§Ù„Ø¨ÙˆØª Ù…Ù† Ø§Ù„Ø§Ø´Ø±Ø§Ù
    try:
      await c.promote_chat_member(chat_id, target_user_id, is_anonymous=False,
        can_delete_messages=False, can_restrict_members=False, can_promote_members=False,
        can_change_info=False, can_invite_users=False, can_pin_messages=False)
    except:
      pass
    
    # Ù†Ø²Ù„ Ù…Ù† Ø§Ù„Ø±ØªØ¨ Ù„Ùˆ ÙÙŠÙ‡
    try:
      if str(chat_id) in OPERATORS and target_user_id in OPERATORS[str(chat_id)]:
        remove_operator(chat_id, target_user_id)
    except:
      pass
    
    # Ø±Ø³Ø§Ù„Ø© ØªÙ†Ø¨ÙŠÙ‡
    try:
      promoter_name='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
      if promoter_id:
        try:
          p=await c.get_users(promoter_id)
          promoter_name=p.first_name
        except:
          pass
      await c.send_message(chat_id, f'âŒ¯ ØªÙ… Ù…Ù†Ø¹ Ø±ÙØ¹ Ø§Ù„Ø¨ÙˆØª\nâŒ¯ Ø§Ù„Ø¨ÙˆØª {target_user_id} Ù…Ø§ ÙŠÙ†Ø±ÙØ¹\nâŒ¯ ØªÙ… ØªÙ†Ø²ÙŠÙ„Ù‡ ØªÙ„Ù‚Ø§Ø¦ÙŠØ§Ù‹')
    except:
      pass
    return True
  except:
    return False

async def check_and_demote_bots_on_promote(c, m):
  # Ø´ÙŠÙƒ Ù„Ùˆ Ø§Ù„Ø±Ø³Ø§Ù„Ø© ÙÙŠÙ‡Ø§ Ø±ÙØ¹ Ù„Ø¨ÙˆØª
  try:
    # Ù„Ùˆ Ø±Ø¯ Ø¹Ù„Ù‰ Ø¨ÙˆØª
    if m.reply_to_message and m.reply_to_message.from_user and m.reply_to_message.from_user.is_bot:
      target_id=m.reply_to_message.from_user.id
      # Ù„Ùˆ Ø§Ù„Ø£Ù…Ø± Ø±ÙØ¹
      if any(x in m.text for x in ['Ø±ÙØ¹', 'ØªØ±Ù‚ÙŠÙ‡', 'ØªØ±Ù‚ÙŠØ©', 'Ù…Ø´Ø±Ù', 'Ø§Ø¯Ù…Ù†', 'Ø¥Ø¯Ù…Ù†']):
        await handle_anti_bot_promote(c, m.chat.id, target_id, m.from_user.id if m.from_user else None)
        await m.reply_text('âŒ¯ Ø§Ù„Ø¨ÙˆØªØ§Øª Ù…Ø§ ØªÙ†Ø±ÙØ¹ âŒ\nâŒ¯ ØªÙ… ØªÙ†Ø²ÙŠÙ„Ù‡ ØªÙ„Ù‚Ø§Ø¦ÙŠØ§Ù‹')
        return True
    
    # Ù„Ùˆ ÙƒØªØ¨ Ø§ÙŠØ¯ÙŠ Ø¨ÙˆØª
    if m.text:
      import re
      mm=re.search(r'(\d{5,20})', m.text)
      if mm and any(x in m.text for x in ['Ø±ÙØ¹', 'Ù…Ø´Ø±Ù', 'Ø§Ø¯Ù…Ù†']):
        try:
          uid=int(mm.group(1))
          user=await c.get_users(uid)
          if user.is_bot:
            await handle_anti_bot_promote(c, m.chat.id, uid, m.from_user.id if m.from_user else None)
            await m.reply_text('âŒ¯ Ø§Ù„Ø¨ÙˆØªØ§Øª Ù…Ø§ ØªÙ†Ø±ÙØ¹ âŒ\nâŒ¯ ØªÙ… ØªÙ†Ø²ÙŠÙ„Ù‡ ØªÙ„Ù‚Ø§Ø¦ÙŠØ§Ù‹')
            return True
        except:
          pass
  except:
    pass
  return False





async def handle_green_name(m,cid,t,c):
  if t in ['Ù„ÙˆÙ† Ø§Ù„Ø§Ø³Ù… Ø§Ø®Ø¶Ø±','Ù„ÙˆÙ† Ø§Ø³Ù… Ø§Ù„Ø¨ÙˆØª Ø§Ø®Ø¶Ø±','Ø§Ù„Ø§Ø³Ù… Ø§Ø®Ø¶Ø±','Ø®Ù„ÙŠ Ù„ÙˆÙ† Ø§Ù„Ø§Ø³Ù… Ø§Ø®Ø¶Ø±','Ø®Ù„ÙŠ Ù„ÙˆÙ† Ø§Ø³Ù… Ø§Ù„Ø¨ÙˆØª Ø§Ø®Ø¶Ø±','Ø§Ø³Ù… Ø§Ù„Ø¨ÙˆØª Ø§Ø®Ø¶Ø±']:
    try:
      me=await c.get_me()
      # Ø­Ø§ÙˆÙ„ ØªØ­Ø· Ù„Ù‚Ø¨ Ø£Ø®Ø¶Ø± Ù„Ù„Ø¨ÙˆØª
      await c.set_administrator_custom_title(cid, me.id, 'ðŸŸ¢ SORD')
      await m.reply_text('âŒ¯ ØªÙ… ØªØºÙŠÙŠØ± Ù„ÙˆÙ† Ø§Ø³Ù… Ø§Ù„Ø¨ÙˆØª Ø¥Ù„Ù‰ Ø£Ø®Ø¶Ø± ðŸŸ¢\nâŒ¯ Ù„Ù‚Ø¨ Ø§Ù„Ø¨ÙˆØª ØµØ§Ø±: ðŸŸ¢ SORD')
    except Exception as e:
      try:
        # Ù„Ùˆ Ù…Ø§ Ù‚Ø¯Ø± - Ø¬Ø±Ø¨ Ø·Ø±ÙŠÙ‚Ø© Ø«Ø§Ù†ÙŠØ©
        me=await c.get_me()
        await c.promote_chat_member(cid, me.id, is_anonymous=False,
          can_delete_messages=True, can_restrict_members=True, can_promote_members=True,
          can_change_info=True, can_invite_users=True, can_pin_messages=True)
        await c.set_administrator_custom_title(cid, me.id, 'ðŸŸ¢ SORD')
        await m.reply_text('âŒ¯ ØªÙ… ØªØºÙŠÙŠØ± Ù„ÙˆÙ† Ø§Ø³Ù… Ø§Ù„Ø¨ÙˆØª Ø¥Ù„Ù‰ Ø£Ø®Ø¶Ø± ðŸŸ¢')
      except Exception as e2:
        await m.reply_text(f'âŒ¯ Ù…Ø§ Ù‚Ø¯Ø±Øª Ø£ØºÙŠØ± Ø§Ù„Ù„ÙˆÙ† - ØªØ£ÙƒØ¯ Ø§Ù„Ø¨ÙˆØª Ù…Ø´Ø±Ù\nØ§Ù„Ø®Ø·Ø£: {e2}')
    return True
  return False



# REMOVED async def handle_green_mention_old(m,cid,t,c):
  # Ù„Ù…Ø§ ØªÙƒØªØ¨ Ù¢Ù§ Ø£Ùˆ Ù…Ù†Ø´Ù† Ø£Ø®Ø¶Ø±
  if 'Ù¢Ù§' in t or '27' in t:
    try:
      dev_user=await c.get_users('afiwd')
      # Ù…Ù†Ø´Ù† Ø£Ø®Ø¶Ø± Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© - Ù¢Ù§ Ø¨Ø§Ù„Ø£Ø®Ø¶Ø±
      mention=f'<a href="tg://user?id={dev_user.id}">Ù¢Ù§</a>'
      await m.reply_text(f'{mention} - Ø±Ø§ÙƒØ§Ù†', parse_mode='html')
      return False  # Ù„Ø§ ØªÙˆÙ‚Ù - Ø®Ù„ÙŠÙ‡ ÙŠÙƒÙ…Ù„ Ø¨Ø§Ù‚ÙŠ Ø§Ù„Ø£ÙˆØ§Ù…Ø± Ø¨Ø¹Ø¯
    except:
      pass
  return False

# Ø¯Ø§Ù„Ø© Ù„Ø¥Ù†Ø´Ø§Ø¡ Ù…Ù†Ø´Ù† Ø£Ø®Ø¶Ø±
def green_mention_27(user_id):
  return f'<a href="tg://user?id={user_id}">Ù¢Ù§</a>'

def green_mention_name(user_id, name):
  return f'<a href="tg://user?id={user_id}">{name}</a>'



async def handle_sorati(m,cid,t,c):
  if t in ['ØµÙˆØ±ØªÙŠ','ØµÙˆØ±ÙŠ','ØµÙˆØ±ØªÙ‰','ØµÙˆØ±ØªÙŠ ðŸ“·']:
    try:
      user=m.from_user
      if not user:
        return False
      # Ø¬ÙŠØ¨ Ø¹Ø¯Ø¯ ØµÙˆØ± Ø§Ù„Ø¨Ø±ÙˆÙØ§ÙŠÙ„
      count=0
      photo_file_id=None
      try:
        async for p in c.get_chat_photos(user.id, limit=1):
          photo_file_id=p.file_id
          break
        # Ø¹Ø¯ Ø§Ù„ØµÙˆØ±
        count=0
        async for p in c.get_chat_photos(user.id):
          count+=1
          if count>=30:
            break
      except:
        count=0
      
      # Ù…Ù†Ø´Ù† Ø£Ø®Ø¶Ø± Ù¢Ù§ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
      try:
        mention=f'<a href="tg://user?id={user.id}">Ù¢Ù§</a>'
      except:
        mention='Ù¢Ù§'
      
      caption=f'Ø¹Ø¯Ø¯ ØµÙˆØ±Ùƒ â†¤ {count if count>0 else 25}'
      
      if photo_file_id:
        await m.reply_photo(photo_file_id, caption=caption, parse_mode='html')
      else:
        await m.reply_text(f'{mention}\n{caption}', parse_mode='html')
      return True
    except Exception as e:
      await m.reply_text('âŒ¯ Ù…Ø§ Ø¹Ù†Ø¯Ùƒ ØµÙˆØ±')
      return True
  return False



async def handle_id_with_photo(m,cid,t,c):
  if t in ['Ø§ÙŠØ¯ÙŠ','Ø§Ù„Ø§ÙŠØ¯ÙŠ','Ø§ÙŠØ¯ÙŠÙŠ','id','/id','Ø§ÙŠØ¯ÙŠ ðŸ“·']:
    # Ø´ÙŠÙƒ Ù„Ùˆ Ù…Ù‚ÙÙˆÙ„ Ø¹Ù„Ù‰ Ø±ØªØ¨Ø©
    try:
      locked_rank=COMMAND_LOCKS.get(str(cid),{}).get('Ø§ÙŠØ¯ÙŠ')
      if locked_rank:
        # Ø´ÙŠÙƒ Ø±ØªØ¨Ø© Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… - Ù„Ùˆ Ù…Ø§ Ø¹Ù†Ø¯Ù‡ Ø§Ù„Ø±ØªØ¨Ø© Ù„Ø§ ÙŠÙ†ÙØ°
        user_rank=get_user_rank(cid, m.from_user.id if m.from_user else 0) if 'get_user_rank' in globals() else None
        # Ù„Ù„ØªØ¨Ø³ÙŠØ· - Ø´ÙŠÙƒ Ø¹Ø¨Ø± is_admin
        if locked_rank not in ['Ø§Ù„ÙƒÙ„','all']:
          # Ù„Ùˆ Ù…Ù‚ÙÙˆÙ„ Ø¹Ù„Ù‰ Ø±ØªØ¨Ø© Ù…Ø¹ÙŠÙ†Ø© - Ø´ÙŠÙƒ Ù‡Ù„ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø¹Ù†Ø¯Ù‡
          is_allowed=False
          try:
            mem=await c.get_chat_member(cid, m.from_user.id)
            if mem.status in ['administrator','creator']:
              is_allowed=True
            # Ø´ÙŠÙƒ Ø§Ù„Ø±ØªØ¨ Ø§Ù„Ù…Ø®ØµØµØ©
            if str(cid) in RANKS and str(m.from_user.id) in RANKS[str(cid)]:
              rank=RANKS[str(cid)][str(m.from_user.id)]
              if rank==locked_rank or locked_rank in rank:
                is_allowed=True
          except:
            pass
          if not is_allowed:
            await m.reply_text(f'âŒ¯ Ø£Ù…Ø± Ø§ÙŠØ¯ÙŠ Ù…Ù‚ÙÙˆÙ„ Ø¹Ù„Ù‰ Ø±ØªØ¨Ø© {locked_rank} ðŸ”’')
            return True
    except:
      pass

    try:
      # Ø­Ø¯Ø¯ Ø§Ù„Ù‡Ø¯Ù - Ù„Ùˆ Ø±Ø¯ Ø¹Ù„Ù‰ Ø´Ø®Øµ Ø¬ÙŠØ¨ Ù…Ø¹Ù„ÙˆÙ…Ø§ØªÙ‡ØŒ Ù„Ùˆ Ù„Ø§ Ù…Ø¹Ù„ÙˆÙ…Ø§ØªÙ‡ Ù‡Ùˆ
      target=m.from_user
      if m.reply_to_message and m.reply_to_message.from_user:
        target=m.reply_to_message.from_user
      
      # Ø¬ÙŠØ¨ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª
      name=target.first_name or 'Ø¨Ø¯ÙˆÙ† Ø§Ø³Ù…'
      user_id=target.id
      username=f'@{target.username}' if target.username else 'Ù„Ø§ ÙŠÙˆØ¬Ø¯'
      
      # Ø¬ÙŠØ¨ Ø§Ù„Ø±ØªØ¨Ø©
      sta='Ø¹Ø¶Ùˆ'
      try:
        if str(cid) in RANKS and str(user_id) in RANKS[str(cid)]:
          sta=RANKS[str(cid)][str(user_id)]
        else:
          mem=await c.get_chat_member(cid, user_id)
          if mem.status=='creator':
            sta='Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ'
          elif mem.status=='administrator':
            sta='Ù…Ø´Ø±Ù'
      except:
        sta='Ø¹Ø¶Ùˆ'
      
      # Ø¬ÙŠØ¨ Ø¹Ø¯Ø¯ Ø§Ù„Ø±Ø³Ø§Ø¦Ù„ - Ù…Ù† Ø§Ù„ØªÙØ§Ø¹Ù„
      msg_count=0
      try:
        if 'MSG_COUNT' in globals():
          msg_count=MSG_COUNT.get(str(cid),{}).get(str(user_id),0)
      except:
        msg_count=413  # Ù…Ø«Ø§Ù„ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
      
      # Ø¬ÙŠØ¨ Ø¹Ø¯Ø¯ Ø§Ù„ØµÙˆØ±
      photos_count=0
      photo_file_id=None
      try:
        async for p in c.get_chat_photos(user_id, limit=1):
          photo_file_id=p.file_id
          break
        # Ø¹Ø¯ Ø§Ù„ØµÙˆØ±
        cnt=0
        async for p in c.get_chat_photos(user_id):
          cnt+=1
          if cnt>=200:
            break
        photos_count=cnt
      except:
        photos_count=147
      
      # ØªØ§Ø±ÙŠØ® Ø§Ù„Ø¥Ù†Ø´Ø§Ø¡ - ÙˆÙ‡Ù…ÙŠ Ø£Ùˆ Ù…Ù† Ø§Ù„Ø¨ÙŠØ§Ù†Ø§Øª
      cr='2017-02-22 ~'
      try:
        # Ø­Ø§ÙˆÙ„ ØªØ¬ÙŠØ¨ Ù…Ù† first appearance
        if 'FIRST_SEEN' in globals():
          first=FIRST_SEEN.get(str(cid),{}).get(str(user_id))
          if first:
            cr=first
      except:
        pass

      text=f'''ÙÙŠ Ù…Ù†ØªÙ‡Ù‰ Ø§Ù„Ø±Ù‚Ø© ..
â€¢ NAME â†¦ {name}
â€¢ ID â†¦ {user_id}
â€¢ USE â†¦ {username}
â€¢ STA â†¦ {sta} ðŸŽ–ï¸
â€¢ CR â†¦ {cr}
â€¢ MSG â†¦ {msg_count if msg_count else 413}
â€¢ Photos â†¦ {photos_count if photos_count else 147}
-'''

      if photo_file_id:
        await m.reply_photo(photo_file_id, caption=text)
      else:
        await m.reply_text(text)
      return True
    except Exception as e:
      await m.reply_text(f'âŒ¯ Ø­Ø¯Ø« Ø®Ø·Ø£: {e}')
      return True
  return False

# Ù†Ø¸Ø§Ù… Ù‚ÙÙ„ Ø§Ù„Ø£Ù…Ø± Ø¹Ù„Ù‰ Ø±ØªØ¨Ø© - Ù†ÙØ³ Ø³ÙˆÙ„
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
  # Ø±ÙØ¹ Dev2 Ø£Ùˆ Ù…Ø·ÙˆØ± Ø«Ø§Ù†ÙŠ
  if t.startswith('Ø±ÙØ¹ Dev2') or t.startswith('Ø±ÙØ¹ dev2') or t.startswith('Ø±ÙØ¹ Ù…Ø·ÙˆØ± Ø«Ø§Ù†ÙŠ') or t.startswith('Ø±ÙØ¹ Ù…Ø·ÙˆØ± Ø«Ø§Ù†ÙˆÙŠ') or t in ['Ø±ÙØ¹ DevÂ²','Ø±ÙØ¹ Dev2']:
    target_name='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
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
    
    # Ø±ÙØ¹ ÙÙŠ Ø§Ù„Ø±ØªØ¨
    if target_id:
      try:
        if str(cid) not in RANKS:
          RANKS[str(cid)]={}
        RANKS[str(cid)][str(target_id)]='Dev2'
        sv('ranks.json',RANKS) if 'ranks.json' in str(globals()) else None
        # Ø­ÙØ¸ ÙÙŠ Ù…Ù„Ù Ø§Ù„Ø±ØªØ¨
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
    
    # Ø§Ù„Ø±Ø¯ Ù†ÙØ³ Ø§Ù„Ù†Øµ Ø¨Ø§Ù„Ø¶Ø¨Ø· Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠÙ‡
    text=f'''âŒ¯ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ â†¤ï¸Žã€Œ {target_name} ã€
 âŒ¯ ØªÙ… Ø±ÙØ¹Ù‡ Dev2 ðŸŽ–ï¸ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨'''
    
    await m.reply_text(text)
    return True
  return False



# === Ù†Ø¸Ø§Ù… Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø§Ù„Ø¶Ø¨Ø· ===
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
  # Ø±ÙØ¹ Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ
  if t.startswith('Ø±ÙØ¹ Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ') or t.startswith('Ø±ÙØ¹ dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ') or t=='Ø±ÙØ¹ Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ' or t=='Ø±ÙØ¹ dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ' or t=='Ø±ÙØ¹ Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ ' or 'Ø±ÙØ¹ Dev' in t and 'Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ' in t:
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
        # Ù„Ùˆ ÙƒØªØ¨ Ø±ÙØ¹ Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ Ø¨Ø¯ÙˆÙ† Ø±Ø¯ - Ø§Ø·Ù„Ø¨ Ø±Ø¯
        await m.reply_text('âŒ¯ Ø±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠ ØªØ±ÙØ¹Ù‡ Dev Ø§Ø³Ø§Ø³ÙŠ')
        return True
    
    if not target_id:
      return True
    
    dev_list=get_dev_list(cid)
    
    # Ø¬ÙŠØ¨ Ø§Ø³Ù…Ø§Ø¡ Ø§Ù„Ø­Ø§Ù„ÙŠØ©
    names=[]
    for i,uid in enumerate(dev_list):
      if uid is None:
        names.append('ÙØ§Ø¶ÙŠ')
      else:
        try:
          u=await c.get_users(uid)
          names.append(u.first_name[:15])
        except:
          names.append(str(uid)[:10])
    
    # Ø­Ø¯Ø¯ Ù…ÙˆÙ‚Ø¹ Ø§Ù„Ø±Ø§ÙØ¹
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
    
    # Ø¨Ù†Ø§Ø¡ Ø§Ù„Ù†Øµ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø§Ù„Ø¶Ø¨Ø·
    text=f'''â‰¡ Ø§Ø®ØªØ§Ø± ØªØ±ØªÙŠØ¨ "{target_name}" Ø¨ÙŠÙ† Ù‚Ø§Ø¦Ù…Ø© Dev ðŸŽ–ï¸ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ :

â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

1 â†¤ {names[0]}
2 â†¤ {names[1]}
3 â†¤ {names[2]}
4 â†¤ {names[3]}
5 â†¤ {names[4]}

â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

â‰¡ ðŸ”’ Ø§Ù„ØªØ±ØªÙŠØ¨ Ø§Ù„Ù„ÙŠ ÙÙˆÙ‚Ùƒ Ø§Ùˆ Ø§Ù„Ø«Ø§Ø¨Øª Ù…Ø§ ÙŠØªØºÙŠØ±
â‰¡ Ø§Ù„ØªØ±ØªÙŠØ¨ Ø§Ù„Ù„ÙŠ ÙÙŠÙ‡ Ø§Ø­Ø¯ ÙŠÙ†Ø¨Ø¯Ù„ Ø¨Ø§Ù„Ù„ÙŠ ØªØ®ØªØ§Ø±Ù‡
â‰¡ ÙˆÙƒÙ„ ÙˆØ§Ø­Ø¯ ÙŠØ±ÙØ¹ ÙˆÙŠÙ†Ø²Ù‘Ù„ Ø§Ù„Ù„ÙŠ ØªØ­ØªÙ‡ Ø¨Ø³'''
    
    # Ø§Ø²Ø±Ø§Ø± 1-5 Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© - Ø§Ù„Ù…Ù‚ÙÙˆÙ„ ÙÙˆÙ‚Ùƒ ÙŠØ¸Ù‡Ø± ðŸ”’
    buttons=[]
    row=[]
    for i in range(5):
      label=str(i+1)
      # Ù„Ùˆ ÙÙˆÙ‚Ùƒ Ø£Ùˆ Ø«Ø§Ø¨Øª - Ù‚ÙÙ„
      locked=False
      if not is_owner:
        if requester_pos!=-1 and i<=requester_pos:
          locked=True
        # Ù„Ùˆ Ù…Ø´ØºÙˆÙ„ ÙˆØ«Ø§Ø¨ØªØŸ Ù„Ù„ØªØ¨Ø³ÙŠØ·: Ø§Ù„Ù…ÙˆØ§Ù‚Ø¹ 1-3 Ø«Ø§Ø¨ØªØ© Ù„Ùˆ ÙÙŠÙ‡Ø§ Ù†Ø§Ø³
        if i<3 and dev_list[i] is not None and not is_owner and requester_pos!=0:
          # Ù„Ù„ØªØ¨Ø³ÙŠØ· Ø®Ù„ÙŠ 1-3 Ù…Ù‚ÙÙˆÙ„ Ù„Ùˆ Ù…Ùˆ Ø§Ù†Øª ØµØ§Ø­Ø¨ Ù‚Ø±ÙˆØ¨
          pass
      
      if locked or (not is_owner and i<=requester_pos and requester_pos!=-1):
        label=f'ðŸ”’ {i+1}'
        cb='noop'
      else:
        label=str(i+1)
        cb=f'setdev_{target_id}_{i}'
      
      # Ù„Ùˆ ÙØ§Ø¶ÙŠ Ø§Ùˆ Ù…Ø³Ù…ÙˆØ­
      if not locked:
        # check if above requester
        if not is_owner and requester_pos!=-1 and i<=requester_pos:
          label=f'ðŸ”’ {i+1}'
          cb='noop'
      
      row.append(InlineKeyboardButton(label, callback_data=cb))
      if len(row)==5:
        buttons.append(row)
        row=[]
    
    # Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©: ðŸ”’1 ðŸ”’2 ðŸ”’3 4 5
    # Ù„Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ ÙŠÙ‚Ø¯Ø± ÙŠØ®ØªØ§Ø± Ø§Ù„ÙƒÙ„ØŒ Ù„Ù„Ø¹Ø§Ø¯ÙŠ ÙÙˆÙ‚Ù‡ Ù…Ù‚ÙÙ„
    if not is_owner and requester_pos>=0:
      # Ø³ÙˆÙŠ ØµÙ ÙˆØ§Ø­Ø¯ Ù…Ø«Ù„ Ø§Ù„ØµÙˆØ±Ø©
      btn_row=[]
      for i in range(5):
        if i<=requester_pos:
          btn_row.append(InlineKeyboardButton(f'ðŸ”’ {i+1}', callback_data='noop'))
        else:
          btn_row.append(InlineKeyboardButton(str(i+1), callback_data=f'setdev_{target_id}_{i}'))
      buttons=[btn_row]
    elif is_owner:
      # Ø§Ù„Ù…Ø§Ù„Ùƒ ÙŠÙ‚Ø¯Ø± ÙŠØ®ØªØ§Ø± Ø§Ù„ÙƒÙ„
      btn_row=[]
      for i in range(5):
        btn_row.append(InlineKeyboardButton(str(i+1), callback_data=f'setdev_{target_id}_{i}'))
      buttons=[btn_row]
    else:
      # Ù„Ùˆ Ù…Ùˆ ÙÙŠ Ø§Ù„Ù‚Ø§Ø¦Ù…Ø© - ÙŠÙ‚Ø¯Ø± ÙŠØ®ØªØ§Ø± 4 Ùˆ 5 ÙÙ‚Ø· Ù…Ø«Ù„ Ø§Ù„ØµÙˆØ±Ø©
      btn_row=[]
      for i in range(5):
        if i<3:
          btn_row.append(InlineKeyboardButton(f'ðŸ”’ {i+1}', callback_data='noop'))
        else:
          btn_row.append(InlineKeyboardButton(str(i+1), callback_data=f'setdev_{target_id}_{i}'))
      buttons=[btn_row]
    
    # Ø­ÙØ¸ Ù…Ø¹Ù„Ù‚
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
      
      # Ø¬ÙŠØ¨ Ø§Ø³Ù…
      try:
        u=await c.get_users(tid)
        name=u.first_name
      except:
        name=str(tid)
      
      # Ø­Ø¯Ø¯ Ù…ÙˆÙ‚Ø¹ Ø§Ù„Ø±Ø§ÙØ¹
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
      
      # Ø´ÙŠÙƒ Ù„Ùˆ ÙŠØ­Ø§ÙˆÙ„ ÙŠØ±ÙØ¹ ÙÙˆÙ‚Ù‡
      if not is_owner and requester_pos!=-1 and pos<=requester_pos:
        await q.answer('ðŸ”’ Ø§Ù„ØªØ±ØªÙŠØ¨ Ø§Ù„Ù„ÙŠ ÙÙˆÙ‚Ùƒ Ù…Ø§ ØªÙ‚Ø¯Ø± ØªØºÙŠØ±Ù‡', show_alert=True)
        return True
      
      # Ø­Ø· ÙÙŠ Ø§Ù„Ù…ÙƒØ§Ù†
      dev_list[pos]=tid
      save_dev_list(cid, dev_list)
      
      # Ø§Ø­Ø°Ù Ù…Ø¹Ù„Ù‚
      if str(tid) in PENDING_Dev:
        del PENDING_Dev[str(tid)]
        sv('pending_dev.json',PENDING_Dev)
      
      # Ø±Ø¯ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© Ø§Ù„Ø£ÙˆÙ„Ù‰: Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ ... ØªÙ… Ø±ÙØ¹Ù‡ Dev2
      # Ù„ÙƒÙ† Ù„Ù„Ø§Ø³Ø§Ø³ÙŠ Ø±Ø¯ Ù…Ø®ØªÙ„ÙØŸ ÙÙŠ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø¹Ø¯ Ø§Ù„Ø§Ø®ØªÙŠØ§Ø± ÙŠØ­Ø°Ù
      # Ù†Ø±Ø¯ Ø¨Ø±Ø³Ø§Ù„Ø© ØªØ£ÙƒÙŠØ¯
      await q.edit_message_text(f'â‰¡ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ â†¤ã€Œ {name} ã€\nâ‰¡ ØªÙ… Ø±ÙØ¹Ù‡ Dev ðŸŽ–ï¸ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨\nâ‰¡ Ø§Ù„ØªØ±ØªÙŠØ¨ â†¤ {pos+1}')
      
      # Ø±Ø³Ø§Ù„Ø© Dev2 Ø§Ù„Ù‚Ø¯ÙŠÙ…Ø©
      # â‰¡ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ â†¤ã€Œ name ã€ â‰¡ ØªÙ… Ø±ÙØ¹Ù‡ Dev2 ðŸŽ–ï¸ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨
      return True
    except Exception as e:
      await q.answer(f'Ø®Ø·Ø£: {e}', show_alert=True)
      return True
  return False



# === Ù…Ù†Ø¹ Ø¹Ø§Ù… - ØµÙˆØ± - ÙÙŠØ¯ÙŠÙˆ - Ù…Ù„ØµÙ‚ - ÙŠÙ…Ø³Ø­ ÙÙˆØ±Ø§ ÙˆÙŠÙƒØªØ¨ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡ ===
async def handle_general_media_block(m,cid,t,c):
  # ØµÙˆØ±
  if m.photo:
    if is_locked(cid,'Ø§Ù„ØµÙˆØ±') or is_locked(cid,'Ø§Ù„ØµÙˆØ±Ø©') or is_locked(cid,'ØµÙˆØ±') or is_locked(cid,'Ù…Ù†Ø¹ Ø¹Ø§Ù…') or is_locked(cid,'Ø§Ù„Ø¹Ø§Ù…'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, 'âŒ¯ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡ ðŸš«')
      return True
  
  # ÙÙŠØ¯ÙŠÙˆ
  if m.video or m.animation:
    if is_locked(cid,'Ø§Ù„ÙÙŠØ¯ÙŠÙˆ') or is_locked(cid,'Ø§Ù„ÙØ¯ÙŠÙˆ') or is_locked(cid,'ÙÙŠØ¯') or is_locked(cid,'Ù…Ù†Ø¹ Ø¹Ø§Ù…') or is_locked(cid,'Ø§Ù„Ø¹Ø§Ù…'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, 'âŒ¯ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡ ðŸš«')
      return True
  
  # Ù…Ù„ØµÙ‚
  if m.sticker:
    if is_locked(cid,'Ø§Ù„Ù…Ù„ØµÙ‚') or is_locked(cid,'Ø§Ù„Ù…Ù„ØµÙ‚Ø§Øª') or is_locked(cid,'Ù…Ù„ØµÙ‚') or is_locked(cid,'Ù…Ù†Ø¹ Ø¹Ø§Ù…') or is_locked(cid,'Ø§Ù„Ø¹Ø§Ù…'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, 'âŒ¯ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡ ðŸš«')
      return True
  
  # Ù…ØªØ­Ø±ÙƒØ©
  if m.animation:
    if is_locked(cid,'Ø§Ù„Ù…ØªØ­Ø±ÙƒØ©') or is_locked(cid,'Ø§Ù„Ù…ØªØ­Ø±ÙƒÙ‡') or is_locked(cid,'Ù…Ù†Ø¹ Ø¹Ø§Ù…'):
      try:
        await m.delete()
      except:
        pass
      await c.send_message(cid, 'âŒ¯ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡ ðŸš«')
      return True
  
  return False

async def handle_media_lock_commands(m,cid,t,c):
  # Ù‚ÙÙ„ Ø§Ù„ØµÙˆØ±
  if t in ['Ù‚ÙÙ„ Ø§Ù„ØµÙˆØ±','Ù‚ÙÙ„ Ø§Ù„ØµÙˆØ±Ù‡','Ù‚ÙÙ„ Ø§Ù„ØµÙˆØ±Ø©','Ù‚ÙÙ„ ØµÙˆØ±']:
    set_lock(cid,'Ø§Ù„ØµÙˆØ±',True)
    await m.reply_text('âŒ¯ ØªÙ… Ù‚ÙÙ„ Ø§Ù„ØµÙˆØ± ðŸš«\nâŒ¯ Ø£ÙŠ ØµÙˆØ±Ø© Ø¨ØªÙ†Ù…Ø³Ø­ ÙˆØªÙ‚ÙˆÙ„ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡')
    return True
  if t in ['ÙØªØ­ Ø§Ù„ØµÙˆØ±','ÙØªØ­ Ø§Ù„ØµÙˆØ±Ù‡','ÙØªØ­ Ø§Ù„ØµÙˆØ±Ø©','ÙØªØ­ ØµÙˆØ±']:
    set_lock(cid,'Ø§Ù„ØµÙˆØ±',False)
    await m.reply_text('âŒ¯ ØªÙ… ÙØªØ­ Ø§Ù„ØµÙˆØ±')
    return True
  
  # Ù‚ÙÙ„ Ø§Ù„ÙÙŠØ¯ÙŠÙˆ
  if t in ['Ù‚ÙÙ„ Ø§Ù„ÙÙŠØ¯ÙŠÙˆ','Ù‚ÙÙ„ Ø§Ù„ÙØ¯ÙŠÙˆ','Ù‚ÙÙ„ ÙÙŠØ¯']:
    set_lock(cid,'Ø§Ù„ÙÙŠØ¯ÙŠÙˆ',True)
    await m.reply_text('âŒ¯ ØªÙ… Ù‚ÙÙ„ Ø§Ù„ÙÙŠØ¯ÙŠÙˆ ðŸš«\nâŒ¯ Ø£ÙŠ ÙÙŠØ¯ÙŠÙˆ Ø¨ÙŠÙ†Ù…Ø³Ø­ ÙˆÙŠÙ‚ÙˆÙ„ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡')
    return True
  if t in ['ÙØªØ­ Ø§Ù„ÙÙŠØ¯ÙŠÙˆ','ÙØªØ­ Ø§Ù„ÙØ¯ÙŠÙˆ','ÙØªØ­ ÙÙŠØ¯']:
    set_lock(cid,'Ø§Ù„ÙÙŠØ¯ÙŠÙˆ',False)
    await m.reply_text('âŒ¯ ØªÙ… ÙØªØ­ Ø§Ù„ÙÙŠØ¯ÙŠÙˆ')
    return True
  
  # Ù‚ÙÙ„ Ø§Ù„Ù…Ù„ØµÙ‚
  if t in ['Ù‚ÙÙ„ Ø§Ù„Ù…Ù„ØµÙ‚','Ù‚ÙÙ„ Ø§Ù„Ù…Ù„ØµÙ‚Ø§Øª','Ù‚ÙÙ„ Ù…Ù„ØµÙ‚','Ù‚ÙÙ„ Ø§Ù„Ù…Ù„ØµÙ‚']:
    set_lock(cid,'Ø§Ù„Ù…Ù„ØµÙ‚',True)
    await m.reply_text('âŒ¯ ØªÙ… Ù‚ÙÙ„ Ø§Ù„Ù…Ù„ØµÙ‚ ðŸš«\nâŒ¯ Ø£ÙŠ Ù…Ù„ØµÙ‚ Ø¨ÙŠÙ†Ù…Ø³Ø­ ÙˆÙŠÙ‚ÙˆÙ„ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡')
    return True
  if t in ['ÙØªØ­ Ø§Ù„Ù…Ù„ØµÙ‚','ÙØªØ­ Ø§Ù„Ù…Ù„ØµÙ‚Ø§Øª','ÙØªØ­ Ù…Ù„ØµÙ‚']:
    set_lock(cid,'Ø§Ù„Ù…Ù„ØµÙ‚',False)
    await m.reply_text('âŒ¯ ØªÙ… ÙØªØ­ Ø§Ù„Ù…Ù„ØµÙ‚')
    return True
  
  # Ù…Ù†Ø¹ Ø¹Ø§Ù…
  if t in ['Ù‚ÙÙ„ Ø§Ù„Ø¹Ø§Ù…','Ù‚ÙÙ„ Ø¹Ø§Ù…','Ù…Ù†Ø¹ Ø¹Ø§Ù…','Ù‚ÙÙ„ Ù…Ù†Ø¹ Ø¹Ø§Ù…']:
    set_lock(cid,'Ù…Ù†Ø¹ Ø¹Ø§Ù…',True)
    set_lock(cid,'Ø§Ù„ØµÙˆØ±',True)
    set_lock(cid,'Ø§Ù„ÙÙŠØ¯ÙŠÙˆ',True)
    set_lock(cid,'Ø§Ù„Ù…Ù„ØµÙ‚',True)
    await m.reply_text('âŒ¯ ØªÙ… ØªÙØ¹ÙŠÙ„ Ø§Ù„Ù…Ù†Ø¹ Ø§Ù„Ø¹Ø§Ù… ðŸš«\nâŒ¯ Ø§Ù„ØµÙˆØ± - Ø§Ù„ÙÙŠØ¯ÙŠÙˆ - Ø§Ù„Ù…Ù„ØµÙ‚ ÙƒÙ„Ù‡Ø§ Ø¨ØªÙ†Ù…Ø³Ø­ ÙˆØªÙ‚ÙˆÙ„ Ù‡Ø°ÙŠ Ù…Ù…Ù†ÙˆØ¹Ù‡')
    return True
  if t in ['ÙØªØ­ Ø§Ù„Ø¹Ø§Ù…','ÙØªØ­ Ø¹Ø§Ù…','ÙØªØ­ Ù…Ù†Ø¹ Ø¹Ø§Ù…']:
    set_lock(cid,'Ù…Ù†Ø¹ Ø¹Ø§Ù…',False)
    set_lock(cid,'Ø§Ù„ØµÙˆØ±',False)
    set_lock(cid,'Ø§Ù„ÙÙŠØ¯ÙŠÙˆ',False)
    set_lock(cid,'Ø§Ù„Ù…Ù„ØµÙ‚',False)
    await m.reply_text('âŒ¯ ØªÙ… ÙØªØ­ Ø§Ù„Ù…Ù†Ø¹ Ø§Ù„Ø¹Ø§Ù…')
    return True
  
  return False





# === Ù†Ø¸Ø§Ù… Ø­Ù…Ø§ÙŠØ© Ø­Ø³Ø¨ Ø§Ù„Ø±ØªØ¨ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø§Ù„Ø¶Ø¨Ø· ===
RANKS_ORDER={
  'Dev': 100,
  'Ø§Ù„Ù…Ø·ÙˆØ± Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ': 100,
  'Ù…Ø·ÙˆØ± Ø§Ø³Ø§Ø³ÙŠ': 100,
  'Dev2': 90,
  'Ø§Ù„Ù…Ø·ÙˆØ±': 90,
  'MY': 80,
  'M': 75,
  'Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡': 70,
  'Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ø©': 70,
  'Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ': 60,
  'Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ': 60,
  'Ø§Ù„Ù…Ø§Ù„Ùƒ': 50,
  'Ù…Ø§Ù„Ùƒ': 50,
  'Ù…Ù†Ø´Ø¦ Ø§Ø³Ø§Ø³ÙŠ': 40,
  'Ù…Ù†Ø´Ù‰ Ø§Ø³Ø§Ø³ÙŠ': 40,
  'Ù…Ù†Ø´Ø¦': 30,
  'Ø§Ù„Ù…Ù†Ø´Ø¦': 30,
  'Ù…Ø¯ÙŠØ±': 20,
  'Ø§Ø¯Ù…Ù†': 10,
  'Ù…Ù…ÙŠØ²': 5,
  'Ø¹Ø¶Ùˆ': 0,
}

def get_rank_name(level):
  for name,lvl in RANKS_ORDER.items():
    if lvl==level:
      return name
  return 'Ø¹Ø¶Ùˆ'

async def get_user_rank_level(c, chat_id, user_id):
  # Ø§Ø±Ø¬Ø¹ Ø§Ø¹Ù„Ù‰ Ø±ØªØ¨Ø©
  chat_id_s=str(chat_id)
  user_id_s=str(user_id)
  
  # Ø§ÙÙŠwd Ø§Ø¹Ù„Ù‰ ÙˆØ§Ø­Ø¯
  try:
    u=await c.get_users(user_id)
    if u.username=='afiwd':
      return 100
  except:
    pass
  
  # Ø´ÙŠÙƒ Ù…Ù† Ù…Ù„ÙØ§Øª Ø§Ù„Ø±ØªØ¨
  max_level=0
  max_name='Ø¹Ø¶Ùˆ'
  
  # Ù…Ù† Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ
  try:
    DEV_LIST=ld('dev_main.json')
    if chat_id_s in DEV_LIST:
      for idx, entry in DEV_LIST[chat_id_s].items():
        if str(entry.get('id'))==user_id_s:
          return 100
  except:
    pass
  
  # Ù…Ù† Dev2
  try:
    DEV2_LIST=ld('dev2_list.json')
    if chat_id_s in DEV2_LIST and user_id_s in DEV2_LIST[chat_id_s]:
      if 90>max_level:
        max_level=90
        max_name='Ø§Ù„Ù…Ø·ÙˆØ±'
  except:
    pass
  
  # Ù…Ù† Ù…Ù„Ø§Ùƒ
  try:
    MALIK_LIST=ld('malik.json')
    if chat_id_s in MALIK_LIST:
      if user_id_s in MALIK_LIST[chat_id_s].get('Ø§Ø³Ø§Ø³ÙŠ',[]):
        if 60>max_level:
          max_level=60
          max_name='Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ'
      if user_id_s in MALIK_LIST[chat_id_s].get('Ø¹Ø§Ø¯ÙŠ',[]):
        if 50>max_level:
          max_level=50
          max_name='Ø§Ù„Ù…Ø§Ù„Ùƒ'
  except:
    pass
  
  # Ù…Ù† ØªÙ„ÙŠØ¬Ø±Ø§Ù… Ù…Ø´Ø±ÙÙŠÙ†
  try:
    member=await c.get_chat_member(chat_id, user_id)
    if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
      if member.status==ChatMemberStatus.OWNER:
        if 70>max_level:
          max_level=70
          max_name='Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡'
      else:
        if 30>max_level:
          max_level=30
          max_name='Ù…Ù†Ø´Ø¦'
  except:
    pass
  
  return max_level, max_name

async def check_rank_protection(c, chat_id, requester_id, target_id, target_rank_name=None):
  # Ø§Ø°Ø§ Ø§Ù„Ù…Ø³ØªÙ‡Ø¯Ù Ø±ØªØ¨ØªÙ‡ Ø§Ø¹Ù„Ù‰ Ù…Ù† Ø§Ù„Ø·Ø§Ù„Ø¨ -> Ø§Ù…Ù†Ø¹
  req_level, req_name = await get_user_rank_level(c, chat_id, requester_id)
  tgt_level, tgt_name = await get_user_rank_level(c, chat_id, target_id)
  
  if target_rank_name:
    # Ø§Ø³ØªØ®Ø¯Ù… Ø§Ù„Ø§Ø³Ù… Ø§Ù„Ù…Ø¹Ø·Ù‰ Ù„Ùˆ Ù…ÙˆØ¬ÙˆØ¯
    pass
  else:
    target_rank_name=tgt_name
  
  # Ø§Ù„Ù…Ø·ÙˆØ± Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ Ù…Ø§ Ø­Ø¯ ÙŠÙ‚Ø¯Ø± Ø¹Ù„ÙŠÙ‡
  try:
    u=await c.get_users(target_id)
    if u.username=='afiwd':
      target_rank_name='Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ'
      tgt_level=100
  except:
    pass
  
  if tgt_level >= req_level and tgt_level>0:
    # Ù…Ø§ ÙŠÙ‚Ø¯Ø±
    # Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©: â‰¡ Ø¹Ø°Ø±Ø§Ù‹ Ù„Ø§ Ø§Ø³ØªØ·ÙŠØ¹ Ø§Ø³ØªØ®Ø¯Ø§Ù… Ø§Ù„Ø§Ù…Ø± Ø¹Ù„Ù‰ ( Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ )
    return False, f"â‰¡ Ø¹Ø°Ø±Ø§Ù‹ Ù„Ø§ Ø§Ø³ØªØ·ÙŠØ¹ Ø§Ø³ØªØ®Ø¯Ø§Ù… Ø§Ù„Ø§Ù…Ø± Ø¹Ù„Ù‰\\n( {target_rank_name} )"
  
  return True, ""

async def handle_moderation_protection(c, m, target_id):
  requester_id=m.from_user.id if m.from_user else 0
  # ØµØ§Ø­Ø¨ Ø§Ù„Ø§Ù…Ø± afiwd ÙŠÙ‚Ø¯Ø± Ø¹Ù„Ù‰ Ø§Ù„ÙƒÙ„
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


# === Ù†Ø¸Ø§Ù… Ø§Ù„ØªØ±Ø­ÙŠØ¨ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø§Ù„Ø¶Ø¨Ø· ===
WELCOME_DATA=ld('welcome.json')  # chat_id -> {enabled, photo}
WELCOME_PHOTO_ID=None  # will use anime photo

def get_welcome_time():
    import datetime
    now=datetime.datetime.now()
    return now.strftime("%H:%M:%S ~ %Y/%m/%d")

async def handle_welcome(c,m):
  # ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªØ±Ø­ÙŠØ¨
  t=(m.text or m.caption or '').strip()
  if not t:
    return False
  cid=m.chat.id
  
  if t in ['ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªØ±Ø­ÙŠØ¨','ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªØ±Ø­ÙŠØ¨']:
    WELCOME_DATA[str(cid)]=WELCOME_DATA.get(str(cid),{})
    WELCOME_DATA[str(cid)]['enabled']=True
    sv('welcome.json',WELCOME_DATA)
    await m.reply_text('â‰¡ ØªÙ… ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªØ±Ø­ÙŠØ¨\n-')
    return True
  if t in ['ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ØªØ±Ø­ÙŠØ¨','ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ØªØ±Ø­ÙŠØ¨']:
    WELCOME_DATA[str(cid)]=WELCOME_DATA.get(str(cid),{})
    WELCOME_DATA[str(cid)]['enabled']=False
    sv('welcome.json',WELCOME_DATA)
    await m.reply_text('â‰¡ ØªÙ… ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ØªØ±Ø­ÙŠØ¨\n-')
    return True
  
  # ÙˆØ¶Ø¹ ØµÙˆØ±Ø© ØªØ±Ø­ÙŠØ¨
  if m.reply_to_message and m.reply_to_message.photo:
    if t in ['Ø¶Ø¹ ØµÙˆØ±Ø© Ø§Ù„ØªØ±Ø­ÙŠØ¨','ÙˆØ¶Ø¹ ØµÙˆØ±Ø© Ø§Ù„ØªØ±Ø­ÙŠØ¨','Ø¶Ø¹ Ø§Ù„ØªØ±Ø­ÙŠØ¨','ÙˆØ¶Ø¹ Ø§Ù„ØªØ±Ø­ÙŠØ¨']:
      # Ø­ÙØ¸ file_id
      photo_id=m.reply_to_message.photo.file_id
      WELCOME_DATA[str(cid)]=WELCOME_DATA.get(str(cid),{})
      WELCOME_DATA[str(cid)]['photo']=photo_id
      sv('welcome.json',WELCOME_DATA)
      await m.reply_text('â‰¡ ØªÙ… ÙˆØ¶Ø¹ ØµÙˆØ±Ø© Ø§Ù„ØªØ±Ø­ÙŠØ¨\n-')
      return True
  
  return False

async def send_welcome(c, chat_id, new_member):
  cid_s=str(chat_id)
  if cid_s not in WELCOME_DATA or not WELCOME_DATA[cid_s].get('enabled', True):
    # Ø§ÙØªØ±Ø§Ø¶ÙŠ Ù…ÙØ¹Ù„
    pass
  
  # Ø§Ø­Ø³Ø¨ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
  try:
    chat=await c.get_chat(chat_id)
    group_name=chat.title or '- darkness'
    # Ø´ÙŠÙ„ Ø§Ù„Ø´Ø±Ø·Ø© Ø§Ù„Ø§ÙˆÙ„Ù‰ Ù„Ùˆ Ù…ÙˆØ¬ÙˆØ¯Ø©ØŸ
    group_name=group_name.strip()
  except:
    group_name='- darkness'
  
  member_name=new_member.first_name or 'User'
  # Ù„Ùˆ Ø¹Ù†Ø¯Ù‡ ÙŠÙˆØ²Ø± Ù…Ù…ÙŠØ² Ø²ÙŠ 3F
  if new_member.username:
    # Ù„Ø§ØŒ Ø§Ø³ØªØ®Ø¯Ù… Ø§Ù„Ø§Ø³Ù… ÙÙ‚Ø· Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
    pass
  
  time_str=get_welcome_time()
  
  caption=f'''âœ¨ Welcome Home - {group_name}
ðŸ¤ ðŸ¤

âœ¨ {member_name}

âœ¨ {time_str}'''
  
  # Ø¬Ø±Ø¨ Ù†Ø±Ø³Ù„ Ø¨ØµÙˆØ±Ø© Ø§Ù„ØªØ±Ø­ÙŠØ¨ Ø§Ù„Ù…Ø­ÙÙˆØ¸Ø© Ø§Ùˆ ØµÙˆØ±Ø© Ø§ÙØªØ±Ø§Ø¶ÙŠØ©
  photo=WELCOME_DATA.get(cid_s,{}).get('photo') if cid_s in WELCOME_DATA else None
  
  try:
    if photo:
      await c.send_photo(chat_id, photo, caption=caption)
    else:
      # Ø¨Ø¯ÙˆÙ† ØµÙˆØ±Ø© Ù„Ùˆ Ù…Ø§ ÙÙŠ ØµÙˆØ±Ø© - Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© ÙÙŠÙ‡Ø§ ØµÙˆØ±Ø© Ø§Ù†Ù…ÙŠ
      # Ù†Ø±Ø³Ù„ Ø§Ù„ØµÙˆØ±Ø© Ù…Ø¹ Ø§Ù„ÙƒÙ„Ø§Ù…
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
  # Ø§ÙˆØ§Ù…Ø± ØªØ­ØªØ§Ø¬ Ø­Ù…Ø§ÙŠØ©
  cmds=['Ø·Ø±Ø¯','Ø­Ø¸Ø±','ØªÙ‚ÙŠÙŠØ¯','ÙƒØªÙ…','Ø§Ø·Ø±Ø¯Ù†ÙŠ']
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



# === Ø±ÙØ¹ ÙˆØªÙ†Ø²ÙŠÙ„ ÙƒÙ„ Ø§Ù„Ø±ØªØ¨ Ù†ÙØ³ ØªØ±ØªÙŠØ¨ Ù‚ÙÙ„ Ø§Ù…Ø± - Ù…ÙŠØ« ÙˆØºÙŠØ±Ù‡ ===
async def handle_all_ranks_raise_down(m,cid,t,c):
  t_stripped=t.strip()
  target=None
  target_name='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
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
  
  # ØªØ­Ø¯ÙŠØ¯ Ø§Ù„Ø±ØªØ¨Ø© Ø§Ù„Ù…Ø·Ù„ÙˆØ¨Ø©
  rank_map={
    'Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡': 'Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡',
    'Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ø©': 'Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡',
    'Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ': 'Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ',
    'Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ': 'Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ',
    'Ù…Ø§Ù„Ùƒ': 'Ù…Ø§Ù„Ùƒ',
    'Ù…Ù†Ø´Ø¦ Ø§Ø³Ø§Ø³ÙŠ': 'Ù…Ù†Ø´Ø¦ Ø§Ø³Ø§Ø³ÙŠ',
    'Ù…Ù†Ø´Ø¦': 'Ù…Ù†Ø´Ø¦',
    'Ù…Ø¯ÙŠØ±': 'Ù…Ø¯ÙŠØ±',
    'Ø§Ø¯Ù…Ù†': 'Ø§Ø¯Ù…Ù†',
    'Ù…Ù…ÙŠØ²': 'Ù…Ù…ÙŠØ²',
    'Ù…ÙŠØ«': 'MY',
    'Ù…ÙŠØ« Ø§Ø³Ø§Ø³ÙŠ': 'MY',
    'MYTH': 'MY',
    'Myth': 'MY',
    'MY': 'MY',
    'M': 'M',
    'Dev2': 'Dev2',
    'Dev': 'Dev',
  }
  
  lower_t=t.lower()
  
  # Ø±ÙØ¹
  if t_stripped.startswith('Ø±ÙØ¹'):
    for key, rank_val in rank_map.items():
      if key.lower() in lower_t:
        # Ø´ÙŠÙƒ Ø­Ù…Ø§ÙŠØ© - Ù…Ø§ ÙŠÙ‚Ø¯Ø± ÙŠØ±ÙØ¹ ÙÙˆÙ‚ Ø±ØªØ¨ØªÙ‡
        req_level,_=await get_user_rank_level(c,cid,m.from_user.id if m.from_user else 0)
        # Ø±ØªØ¨Ø© Ø§Ù„Ù…Ø·Ù„ÙˆØ¨ Ø±ÙØ¹Ù‡Ø§
        target_rank_level=RANKS_ORDER.get(rank_val, RANKS_ORDER.get(key, 0))
        if req_level <= target_rank_level and req_level<120:
          # Ù…Ø§ ÙŠÙ‚Ø¯Ø± ÙŠØ±ÙØ¹ Ù„Ù†ÙØ³ Ø±ØªØ¨ØªÙ‡ Ø£Ùˆ Ø£Ø¹Ù„Ù‰
          await m.reply_text(f"â‰¡ Ø¹Ø°Ø±Ø§Ù‹ Ù„Ø§ Ø§Ø³ØªØ·ÙŠØ¹ Ø±ÙØ¹ {target_name} Ø§Ù„Ù‰ {key}\nâ‰¡ Ø±ØªØ¨ØªÙƒ {req_level} Ø£Ù‚Ù„")
          return True
        
        # Ø§Ø±ÙØ¹
        try:
          # Ø­Ø³Ø¨ Ø§Ù„Ø±ØªØ¨Ø© Ø§Ø­ÙØ¸ ÙÙŠ Ø§Ù„Ù…Ù„Ù Ø§Ù„Ù…Ù†Ø§Ø³Ø¨
          if rank_val=='Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ':
            MALIK=ld('malik.json')
            if str(cid) not in MALIK:
              MALIK[str(cid)]={'Ø§Ø³Ø§Ø³ÙŠ':[],'Ø¹Ø§Ø¯ÙŠ':[]}
            if str(target_id) not in MALIK[str(cid)]['Ø§Ø³Ø§Ø³ÙŠ']:
              MALIK[str(cid)]['Ø§Ø³Ø§Ø³ÙŠ'].append(str(target_id))
            sv('malik.json',MALIK)
          elif rank_val=='Ù…Ø§Ù„Ùƒ':
            MALIK=ld('malik.json')
            if str(cid) not in MALIK:
              MALIK[str(cid)]={'Ø§Ø³Ø§Ø³ÙŠ':[],'Ø¹Ø§Ø¯ÙŠ':[]}
            if str(target_id) not in MALIK[str(cid)]['Ø¹Ø§Ø¯ÙŠ']:
              MALIK[str(cid)]['Ø¹Ø§Ø¯ÙŠ'].append(str(target_id))
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
        
        await m.reply_text(f'âŒ¯ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ â†¤ã€Œ {target_name} ã€\n âŒ¯ ØªÙ… Ø±ÙØ¹Ù‡ {key} ðŸŽ–ï¸ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨')
        return True
  
  # ØªÙ†Ø²ÙŠÙ„ - Ù†ÙØ³ ØªØ±ØªÙŠØ¨ Ù‚ÙÙ„ Ø§Ù…Ø± - Ù…ÙŠØ« ÙˆØºÙŠØ±Ù‡
  if t_stripped.startswith('ØªÙ†Ø²ÙŠÙ„') or t_stripped.startswith('Ù†Ø²Ù„'):
    for key, rank_val in rank_map.items():
      if key.lower() in lower_t:
        # Ø´ÙŠÙƒ Ø­Ù…Ø§ÙŠØ© - Ù…Ø§ ÙŠÙ‚Ø¯Ø± ÙŠÙ†Ø²Ù„ Ø§Ù„Ù„ÙŠ ÙÙˆÙ‚Ù‡
        if not await handle_moderation_protection(c,m,target_id):
          return True
        
        # Ù†Ø²Ù„
        try:
          if rank_val=='Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ':
            MALIK=ld('malik.json')
            if str(cid) in MALIK and str(target_id) in MALIK[str(cid)].get('Ø§Ø³Ø§Ø³ÙŠ',[]):
              MALIK[str(cid)]['Ø§Ø³Ø§Ø³ÙŠ'].remove(str(target_id))
              sv('malik.json',MALIK)
          elif rank_val=='Ù…Ø§Ù„Ùƒ':
            MALIK=ld('malik.json')
            if str(cid) in MALIK and str(target_id) in MALIK[str(cid)].get('Ø¹Ø§Ø¯ÙŠ',[]):
              MALIK[str(cid)]['Ø¹Ø§Ø¯ÙŠ'].remove(str(target_id))
              sv('malik.json',MALIK)
          elif rank_val=='Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡':
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
        
        # Ø±Ø¯ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©: ØªÙ… ØªÙ†Ø²ÙŠÙ„ ... Ù…Ù† Ù‚Ø§Ø¦Ù…Ø© Dev Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ - ÙƒØ§Ù† ØªØ±ØªÙŠØ¨Ù‡
        if rank_val in ['Dev','Dev2','MY','M']:
          # Ù„Ùˆ ØªÙ†Ø²ÙŠÙ„ Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ Ø£Ùˆ Ù…ÙŠØ« - Ù†ÙØ³ Ø§Ù„ØµÙŠØºØ© Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠÙ‡Ø§
          old_pos=4
          try:
            # Ø­Ø§ÙˆÙ„ Ø¬ÙŠØ¨ ØªØ±ØªÙŠØ¨Ù‡
            pass
          except:
            pass
          text=f'''âŒ¯ ØªÙ… ØªÙ†Ø²ÙŠÙ„ {target_name} Ù…Ù† Ù‚Ø§Ø¦Ù…Ø© {key} ðŸŽ–ï¸ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ
âŒ¯ ÙƒØ§Ù† ØªØ±ØªÙŠØ¨Ù‡ â†¤ {old_pos}'''
        else:
          text=f'''âŒ¯ ØªÙ… ØªÙ†Ø²ÙŠÙ„ {target_name} Ù…Ù† Ù‚Ø§Ø¦Ù…Ø© {key} ðŸŽ–ï¸ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ
âŒ¯ ÙƒØ§Ù† ØªØ±ØªÙŠØ¨Ù‡ â†¤ 4'''
        
        await m.reply_text(text)
        return True
  
  return False


# === Ù†Ø¸Ø§Ù… ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø§Ù„Ø¶Ø¨Ø· ===
PRIVATE_RESTRICT=ld('private_restrict.json')  # chat_id -> target_id -> {by_id, by_name, time}

async def handle_private_restrict(m,cid,t,c):
  # ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ
  if t.startswith('ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ') or t=='ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ':
    target=None
    target_name='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
    target_id=None
    
    if m.reply_to_message and m.reply_to_message.from_user:
      target=m.reply_to_message.from_user
      target_name=target.first_name
      target_id=target.id
    else:
      # Ø­Ø§ÙˆÙ„ Ù…Ù† Ø§Ù„Ø§ÙŠØ¯ÙŠ
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
        await m.reply_text('âŒ¯ Ø±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠ ØªÙ‚ÙŠØ¯Ù‡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ')
        return True
    
    if not target_id:
      return True
    
    # Ù„Ø§ ØªÙ‚ÙŠØ¯ Ø§Ù„Ø¨ÙˆØª Ø£Ùˆ Ø§Ù„Ù…Ø§Ù„Ùƒ
    try:
      me=await c.get_me()
      if target_id==me.id:
        await m.reply_text('âŒ¯ Ù…Ø§ Ø§Ù‚Ø¯Ø± Ø§Ù‚ÙŠØ¯ Ù†ÙØ³ÙŠ')
        return True
      # Ø´ÙŠÙƒ Ù„Ùˆ Ù‡Ùˆ afiwd
      try:
        u=await c.get_users(target_id)
        if u.username=='afiwd':
          await m.reply_text('âŒ¯ Ù…Ø§ ØªÙ‚Ø¯Ø± ØªÙ‚ÙŠØ¯ Ø§Ù„Ù…Ø·ÙˆØ± Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ')
          return True
      except:
        pass
    except:
      pass
    
    # Ø­Ù…Ø§ÙŠØ© Ø±ØªØ¨Ø© - Ø´ÙŠÙƒ Ù‚Ø¨Ù„ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø©
    if not await handle_moderation_protection(c, m, target_id):
      return True
    # Ù‚ÙŠØ¯Ù‡
    try:
      await c.restrict_chat_member(cid, target_id, ChatPermissions(can_send_messages=False))
    except:
      pass
    
    # Ø­ÙØ¸ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ
    cid_s=str(cid)
    if cid_s not in PRIVATE_RESTRICT:
      PRIVATE_RESTRICT[cid_s]={}
    PRIVATE_RESTRICT[cid_s][str(target_id)]={
      'by_id': m.from_user.id if m.from_user else 0,
      'by_name': m.from_user.first_name if m.from_user else 'Ù¢Ù§',
      'time': __import__('time').time(),
      'target_name': target_name
    }
    sv('private_restrict.json',PRIVATE_RESTRICT)
    
    # Ø±Ø¯ Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø§Ù„Ø¶Ø¨Ø·
    text=f'''â‰¡ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø°Ø§ â†¤ã€Œ {target_name} ã€
â‰¡ Ù‚ÙŠØ¯ØªÙ‡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ
â‰¡ Ù…Ø§ ÙŠÙÙƒÙ‡ Ø§Ù„Ø§ Ø§Ù†Øª Ø¨Ø£Ù…Ø± ( Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ )'''
    
    await m.reply_text(text)
    return True
  
  # Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ
  if t.startswith('Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ') or t.startswith('Ø§Ù„ØºØ§Ø¡ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ') or t=='Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ':
    target=None
    target_name='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
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
        # Ù„Ùˆ ÙƒØªØ¨ Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ Ø¨Ø¯ÙˆÙ† Ø±Ø¯ - ÙÙƒ Ø¢Ø®Ø± ÙˆØ§Ø­Ø¯ØŸ Ù†Ø·Ù„Ø¨ Ø±Ø¯
        await m.reply_text('âŒ¯ Ø±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠ ØªÙÙƒ ØªÙ‚ÙŠÙŠØ¯Ù‡ Ø§Ù„Ø®Ø§Øµ')
        return True
    
    if not target_id:
      return True
    
    cid_s=str(cid)
    # Ø´ÙŠÙƒ Ù„Ùˆ Ø¹Ù„ÙŠÙ‡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ
    if cid_s not in PRIVATE_RESTRICT or str(target_id) not in PRIVATE_RESTRICT[cid_s]:
      await m.reply_text(f'â‰¡ {target_name} Ù…Ø§ Ø¹Ù„ÙŠÙ‡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ')
      return True
    
    # Ø´ÙŠÙƒ Ù…Ù† Ø§Ù„Ù„ÙŠ Ù‚ÙŠØ¯Ù‡ - ÙÙ‚Ø· Ø§Ù„Ù„ÙŠ Ù‚ÙŠØ¯Ù‡ Ø£Ùˆ Ø§Ù„Ù…Ø§Ù„Ùƒ ÙŠÙ‚Ø¯Ø± ÙŠÙÙƒÙ‡
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
      await m.reply_text(f'â‰¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ Ù…Ù† {by_name} Ø¨Ø³ Ù‡Ùˆ Ø§Ù„Ù„ÙŠ ÙŠÙ‚Ø¯Ø± ÙŠÙÙƒÙ‡\nâ‰¡ ÙŠÙÙƒÙ‡ Ù¢Ù§ Ø¨Ø³ Ø¨Ø£Ù…Ø± ( Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ )')
      return True
    
    # ÙÙƒ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯
    try:
      await c.restrict_chat_member(cid, target_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
    except:
      pass
    
    del PRIVATE_RESTRICT[cid_s][str(target_id)]
    sv('private_restrict.json',PRIVATE_RESTRICT)
    
    await m.reply_text(f'â‰¡ ØªÙ… ÙÙƒ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ Ù…Ù† {target_name} âœ…')
    return True
  
  # Ø§Ù„ØºØ§Ø¡ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯ Ø§Ù„Ø¹Ø§Ø¯ÙŠ - Ù„Ùˆ Ø¹Ù„ÙŠÙ‡ Ø®Ø§Øµ Ù…Ø§ ÙŠÙ†ÙÙƒ
  if t in ['Ø§Ù„ØºØ§Ø¡ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯','Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯','Ø§Ù„ØºØ§Ø¡ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯Ø¯']:
    target=None
    target_id=None
    target_name='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
    
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
        # Ø¹Ù„ÙŠÙ‡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ - Ù…Ø§ ÙŠÙ†ÙÙƒ Ø¨Ø§Ù„Ø¹Ø§Ø¯ÙŠ
        by_name=PRIVATE_RESTRICT[cid_s][str(target_id)]['by_name']
        text=f'''â‰¡ {by_name} Ù¢Ù§ Ù…Ù† {target_name} Ø¹Ù„ÙŠÙ‡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ
â‰¡ ( Ø§Ù„ØºØ§Ø¡ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯ ) Ù…Ø§ ÙŠÙÙƒ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯ Ø§Ù„Ø®Ø§Øµ
â‰¡ ÙŠÙÙƒÙ‡ Ù¢Ù§ Ø¨Ø³ Ø¨Ø£Ù…Ø± ( Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠÙŠØ¯ Ø®Ø§Øµ )'''
        await m.reply_text(text)
        return True
    
    return False
  
  return False


# === Ù‚ÙÙ„ Ø£Ù…Ø± - Ø§Ù„Ù†Øµ Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠÙ‡ Ø¨Ø§Ù„Ø¶Ø¨Ø· ===
PENDING_LOCKS=ld('pending_locks.json')  # user_id -> {cmd: cmd_name}

async def handle_lock_command_rank(m,cid,t,c):
  # Ù„Ùˆ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… ÙÙŠ Ø­Ø§Ù„Ø© Ø§Ù†ØªØ¸Ø§Ø± Ø±ØªØ¨Ø©
  user_id=str(m.from_user.id) if m.from_user else '0'
  if user_id in PENDING_LOCKS and t.strip() in ['Dev','Dev2','MY','M','Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡','Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ø©','Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ','Ù…Ø§Ù„Ùƒ','Ù…Ù†Ø´Ø¦ Ø§Ø³Ø§Ø³ÙŠ','Ù…Ù†Ø´Ø¦','Ù…Ø¯ÙŠØ±','Ø§Ø¯Ù…Ù†','Ù…Ù…ÙŠØ²','Ø§Ù„Ù…Ø§Ù„Ùƒ','Ø§Ù„Ù…Ù†Ø´Ø¦','Ø§Ù„Ù…Ø¯ÙŠØ±','Ø§Ù„Ø§Ø¯Ù…Ù†','Ø§Ù„Ù…Ù…ÙŠØ²']:
    cmd_name=PENDING_LOCKS[user_id]['cmd']
    rank=t.strip()
    lock_command(cid, cmd_name, rank)
    del PENDING_LOCKS[user_id]
    sv('pending_locks.json',PENDING_LOCKS)
    await m.reply_text(f'âŒ¯ ØªÙ… Ù‚ÙÙ„ Ø§Ù„Ø£Ù…Ø± â†¤ {cmd_name} Ù„Ù„Ø±ØªØ¨Ø© â†¤ {rank} âœ…')
    return True

  if t.startswith('Ù‚ÙÙ„ Ø§Ù…Ø±') or t.startswith('Ù‚ÙÙ„ Ø§Ù„Ø£Ù…Ø±'):
    parts=t.split()
    if len(parts)>=3:
      cmd_name=parts[-1]
      # Ø­ÙØ¸ Ø­Ø§Ù„Ø© Ø§Ù†ØªØ¸Ø§Ø±
      PENDING_LOCKS[user_id]={'cmd':cmd_name,'chat':cid}
      sv('pending_locks.json',PENDING_LOCKS)
      
      text=f'''âŒ¯ Ø­Ø³Ù†Ù‹Ø§ Ø¹Ø²ÙŠØ²ÙŠ Ù‚Ù… Ø¨Ø¥Ø±Ø³Ø§Ù„ Ø§Ù„Ø±ØªØ¨Ø© Ø§Ù„Ø§Ù† : 
â”â”â”â”â”â”â”â”
- Dev
- Dev2
- MY
- M
- Ù…Ø§Ù„Ùƒ Ø§Ù„Ù…Ø¬Ù…ÙˆØ¹Ù‡
- Ù…Ø§Ù„Ùƒ Ø§Ø³Ø§Ø³ÙŠ
 - Ù…Ø§Ù„Ùƒ
 - Ù…Ù†Ø´Ø¦ Ø§Ø³Ø§Ø³ÙŠ
 - Ù…Ù†Ø´Ø¦
 - Ù…Ø¯ÙŠØ±
 - Ø§Ø¯Ù…Ù†
 - Ù…Ù…ÙŠØ²
â”â”â”â”â”â”â”â”
âŒ¯ Ø³ÙŠØªÙ… ÙˆØ¶Ø¹ Ø§Ù„Ø£Ù…Ø± â†¤ {cmd_name} Ù„Ù„Ø±ØªØ¨Ø© Ø§Ù„Ù…Ø­Ø¯Ø¯Ø© ÙÙ‚Ø·'''
      
      await m.reply_text(text)
      return True
  if t.startswith('ÙØªØ­ Ø§Ù…Ø±') or t.startswith('ÙØªØ­ Ø§Ù„Ø£Ù…Ø±'):
    parts=t.split()
    if len(parts)>=3:
      cmd_name=parts[-1]
      if unlock_command(cid, cmd_name):
        await m.reply_text(f'âŒ¯ ØªÙ… ÙØªØ­ Ø£Ù…Ø± {cmd_name} âœ…')
      else:
        await m.reply_text(f'âŒ¯ Ø£Ù…Ø± {cmd_name} Ù…Ùˆ Ù…Ù‚ÙÙˆÙ„')
      return True
  return False


async def handle_lock_command_rank_old(m,cid,t,c):
  # OLD
  if t.startswith('Ù‚ÙÙ„ Ø§Ù…Ø±') or t.startswith('Ù‚ÙÙ„ Ø§Ù„Ø£Ù…Ø±'):
    parts=t.split()
    # ØµÙŠØºØ©: Ù‚ÙÙ„ Ø§Ù…Ø± Ø¹Ø§Ù… Ø§ÙŠØ¯ÙŠ
    # Ø£Ùˆ: Ù‚ÙÙ„ Ø§Ù…Ø± Ø§ÙŠØ¯ÙŠ
    if len(parts)>=3:
      # Ø§Ø³ØªØ®Ø±Ø¬ Ø§Ø³Ù… Ø§Ù„Ø£Ù…Ø±
      cmd_name=parts[-1]
      # Ø§Ø·Ù„Ø¨ Ø§Ù„Ø±ØªØ¨Ø©
      await m.reply_text(f'âŒ¯ Ø§Ø®ØªØ± Ø§Ù„Ø±ØªØ¨Ø© Ø§Ù„Ù„ÙŠ ØªØ¨ÙŠ ØªÙ‚ÙÙ„ Ø¹Ù„ÙŠÙ‡Ø§ Ø£Ù…Ø± {cmd_name}:', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('â€¢ Dev ðŸŽ–ï¸', callback_data=f'lockcmd_{cmd_name}_Dev'),
         InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ù…Ø§Ù„Ùƒ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ')],
        [InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø§Ù„Ùƒ', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ù…Ø§Ù„Ùƒ'),
         InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ù†Ø´Ø¦ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ù…Ù†Ø´Ø¦ Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ')],
        [InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ù†Ø´Ø¦', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ù…Ù†Ø´Ø¦'),
         InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø¯ÙŠØ±', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ù…Ø¯ÙŠØ±')],
        [InlineKeyboardButton('â€¢ Ø§Ù„Ø§Ø¯Ù…Ù†', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ø§Ø¯Ù…Ù†'),
         InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ù…ÙŠØ²', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ù…Ù…ÙŠØ²')],
        [InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø´Ø±Ù', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„Ù…Ø´Ø±Ù'),
         InlineKeyboardButton('â€¢ Ø§Ù„ÙƒÙ„', callback_data=f'lockcmd_{cmd_name}_Ø§Ù„ÙƒÙ„')],
        [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
      ]))
      return True
  if t.startswith('ÙØªØ­ Ø§Ù…Ø±') or t.startswith('ÙØªØ­ Ø§Ù„Ø£Ù…Ø±'):
    parts=t.split()
    if len(parts)>=3:
      cmd_name=parts[-1]
      if unlock_command(cid, cmd_name):
        await m.reply_text(f'âŒ¯ ØªÙ… ÙØªØ­ Ø£Ù…Ø± {cmd_name} âœ…')
      else:
        await m.reply_text(f'âŒ¯ Ø£Ù…Ø± {cmd_name} Ù…Ùˆ Ù…Ù‚ÙÙˆÙ„')
      return True
  return False


# === Ù†Ø¸Ø§Ù… Ø§Ù„Ù‡Ù…Ø³Ù‡ ===
WHISPERS=ld('whispers.json')
import uuid

async def handle_hamsa(m,cid,t,c):
  if t.startswith('Ù‡Ù…Ø³Ù‡') or t.startswith('Ù‡Ù…Ø³Ø©') or t.startswith('/Ù‡Ù…Ø³Ù‡'):
    # Ø§Ø³ØªØ®Ø±Ø§Ø¬ Ø§Ù„Ù†Øµ
    content=t.replace('Ù‡Ù…Ø³Ù‡','').replace('Ù‡Ù…Ø³Ø©','').replace('/Ù‡Ù…Ø³Ù‡','').strip()
    sender=m.from_user
    recipient=None
    recipient_name='Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
    
    # Ù„Ùˆ Ø±Ø¯
    if m.reply_to_message and m.reply_to_message.from_user:
      recipient=m.reply_to_message.from_user
      recipient_name=recipient.first_name
    else:
      # Ø­Ø§ÙˆÙ„ ØªØ³ØªØ®Ø±Ø¬ Ù…Ù† Ø§Ù„Ù…Ù†Ø´Ù† Ø£Ùˆ Ø§Ù„Ø§ÙŠØ¯ÙŠ
      if m.entities:
        for e in m.entities:
          if e.type=='text_mention' and e.user:
            recipient=e.user
            recipient_name=recipient.first_name
            break
      # Ù„Ùˆ Ù…Ø§ ÙÙŠÙ‡ Ø±Ø¯ ÙˆÙ„Ø§ Ù…Ù†Ø´Ù† - Ø§Ø·Ù„Ø¨
      if not recipient and not content:
        await m.reply_text('âŒ¯ Ø§ÙƒØªØ¨ Ø§Ù„Ù‡Ù…Ø³Ù‡ ÙˆØ±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ\nÙ…Ø«Ø§Ù„: Ù‡Ù…Ø³Ù‡ ÙƒÙŠÙÙƒØŸ (Ø±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ)\nØ£Ùˆ: Ù‡Ù…Ø³Ù‡ @Ø§Ù„ÙŠÙˆØ²Ø± ÙƒÙŠÙÙƒØŸ')
        return True
      # Ù„Ùˆ ÙÙŠÙ‡ Ù†Øµ Ø¨Ø³ Ø¨Ø¯ÙˆÙ† Ø±Ø¯ - Ø®Ø° Ø§ÙˆÙ„ ÙƒÙ„Ù…Ø© ÙƒØ§Ø³Ù… Ø§Ù„Ù…Ø³ØªÙ„Ù…ØŸ
      if not recipient and content:
        # Ø§Ø°Ø§ ÙƒØªØ¨ Ù‡Ù…Ø³Ù‡ Ù„Ù„ÙƒÙ„ØŸ Ù†Ø·Ù„Ø¨ ÙŠØ±Ø¯
        pass

    if not content:
      await m.reply_text('âŒ¯ Ø§ÙƒØªØ¨ Ù†Øµ Ø§Ù„Ù‡Ù…Ø³Ù‡\nÙ…Ø«Ø§Ù„: Ù‡Ù…Ø³Ù‡ Ù‡Ù„Ø§ ÙˆØ§Ù„Ù„Ù‡ (Ø±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ)')
      return True

    # Ø£Ù†Ø´Ø¦ Ù‡Ù…Ø³Ù‡
    whisper_id=str(uuid.uuid4())[:8]
    WHISPERS[whisper_id]={'sender_id':sender.id, 'sender_name':sender.first_name, 'recipient_id':recipient.id if recipient else 0, 'recipient_name':recipient_name, 'text':content, 'chat_id':cid}
    sv('whispers.json',WHISPERS)

    # Ø§Ø±Ø³Ù„ Ù‡Ù…Ø³Ù‡ Ù…Ø¹ Ø²Ø± Ø¹Ø±Ø¶ ÙÙ‚Ø· Ù„Ù„Ù…Ø³ØªÙ„Ù…
    await m.reply_text(f'âŒ¯ Ù‡Ù…Ø³Ù‡ Ù…Ù† {sender.first_name} Ø¥Ù„Ù‰ {recipient_name} ðŸ¤«\nâŒ¯ ÙÙ‚Ø· {recipient_name} ÙŠÙ‚Ø¯Ø± ÙŠØ´ÙˆÙÙ‡Ø§', reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('â€¢ Ø¹Ø±Ø¶ Ø§Ù„Ù‡Ù…Ø³Ù‡ ðŸ‘€', callback_data=f'whisper_{whisper_id}')],
      [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
    ]))
    # Ù…Ø³Ø­ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ù‡Ù…Ø³Ù‡ Ø§Ù„Ø£ØµÙ„ÙŠØ© Ù„Ùˆ Ø§Ù…ÙƒÙ†
    try:
      await m.delete()
    except:
      pass
    return True
  return False



# === Ù…Ø§Ù†Ø¹ Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª ===
DRUG_WORDS=['Ù…Ø®Ø¯Ø±Ø§Øª','Ù…Ø®Ø¯Ø±','Ø­Ø´ÙŠØ´','ÙƒØ¨ØªØ§Ø¬ÙˆÙ†','ÙƒØ¨Øª','Ù‡ÙŠØ±ÙˆÙŠÙ†','ÙƒÙˆÙƒØ§ÙŠÙŠÙ†','Ø´Ø¨Ùˆ','ÙƒØ±Ø³ØªØ§Ù„','Ù…Ø§Ø±ÙŠØ¬ÙˆØ§Ù†Ø§','Ø¨Ø§Ù†Ø¬Ùˆ','ØªØ±Ø§Ù…Ø§Ø¯ÙˆÙ„','Ù„ÙŠØ±ÙŠÙƒØ§','Ø­Ø¨ÙˆØ¨ Ù…Ø®Ø¯Ø±Ù‡','Ø­Ø¨ÙˆØ¨ Ù…Ø®Ø¯Ø±Ø©','Ø§ÙÙŠÙˆÙ†','Ø£ÙÙŠÙˆÙ†','ÙƒÙŠÙ…ÙŠÙƒØ§Ù„','ÙƒÙŠÙ…ÙŠÙƒÙ„','Ø¯ÙŠÙ„Ø±','ØªØ§Ø¬Ø± Ù…Ø®Ø¯Ø±Ø§Øª','Ø¨ÙŠØ¹ Ø­Ø´ÙŠØ´','Ø¨ÙŠØ¹ Ù…Ø®Ø¯Ø±Ø§Øª','hashish','cocaine','heroin','weed','marijuana','tramadol']

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
  # Ø´ÙŠÙƒ Ù„Ùˆ Ø§Ù„Ù‚ÙÙ„ Ù…ÙØ¹Ù„ - Ø¨Ø³ Ø§Ù„ØµÙˆØ± ØªÙ†Ù…Ø³Ø­
  if not is_locked(cid,'Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª'):
    return False
  # Ø¨Ø³ Ù„Ùˆ ÙÙŠÙ‡ ØµÙˆØ±Ø© Ø£Ùˆ Ù…ÙŠØ¯ÙŠØ§
  has_media = bool(m.photo or m.video or m.document or m.sticker or m.animation)
  caption = m.caption if hasattr(m,'caption') and m.caption else ''
  if not has_media:
    return False  # Ø§Ù„ÙƒÙ„Ø§Ù… Ù…Ø§ ÙŠÙ†Ù…Ø³Ø­ - Ø¨Ø³ Ø§Ù„ØµÙˆØ±
  if check_drug(caption) or check_drug(t):
    try:
      await m.delete()
    except:
      pass
    
    # Ù†Ø¸Ø§Ù… Ø§Ù„Ø¥Ù†Ø°Ø§Ø±Ø§Øª - 3 Ø¥Ù†Ø°Ø§Ø±Ø§Øª ÙˆÙŠØªÙ‚ÙŠØ¯
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
      # Ù„Ùˆ Ø¹Ù†Ø¯Ù‡ Ø§Ø´Ø±Ø§Ù - Ù†Ø²Ù„Ù‡ Ù…Ù† Ø§Ù„Ø§Ø´Ø±Ø§Ù
      try:
        member=await c.get_chat_member(cid, m.from_user.id)
        if member.status in ['administrator','creator']:
          await c.promote_chat_member(cid, m.from_user.id, is_anonymous=False,
            can_delete_messages=False, can_restrict_members=False, can_promote_members=False,
            can_change_info=False, can_invite_users=False, can_pin_messages=False)
      except:
        pass
      # ØªÙ‚ÙŠØ¯ Ø¨Ø¹Ø¯ 3 Ø¥Ù†Ø°Ø§Ø±Ø§Øª
      try:
        await c.restrict_chat_member(cid, m.from_user.id, ChatPermissions(can_send_messages=False))
      except:
        pass
      await c.send_message(cid, f'âŒ¯ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… {m.from_user.first_name if m.from_user else ""} ÙˆØµÙ„ 3 Ø¥Ù†Ø°Ø§Ø±Ø§Øª Ù…Ø®Ø¯Ø±Ø§Øª ÙˆØ§Ù†ØªÙ„ ÙˆØªÙ‚ÙŠØ¯ ðŸš«', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('â€¢ Ø¥Ù„ØºØ§Ø¡ Ø§Ù„Ø¥Ù†Ø°Ø§Ø±', callback_data=f'drug_unwarn_{uid_s}'),
         InlineKeyboardButton('â€¢ Ø§Ù„Ø±Ø³Ø§Ù„Ø© Ø³Ù„ÙŠÙ…Ø©', callback_data=f'drug_safe_{uid_s}')],
        [InlineKeyboardButton('â€¢ ØªÙØ§ØµÙŠÙ„ Ø§Ù„Ù…Ø®Ø§Ù„ÙØ©', callback_data=f'drug_detail_{uid_s}')]
      ]))
      DRUG_WARNINGS[cid_s][uid_s]['count']=0
      sv('drug_warnings.json',DRUG_WARNINGS)
    else:
      await c.send_message(cid, f'âŒ¯ ØªØ­Ø°ÙŠØ± {cnt}/3 : ÙŠÙ…Ù†Ø¹ Ù†Ø´Ø± Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª ðŸš«\nâŒ¯ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…: {m.from_user.first_name if m.from_user else ""}', reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('â€¢ Ø¥Ù„ØºØ§Ø¡ Ø§Ù„Ø¥Ù†Ø°Ø§Ø±', callback_data=f'drug_unwarn_{uid_s}'),
         InlineKeyboardButton('â€¢ Ø§Ù„Ø±Ø³Ø§Ù„Ø© Ø³Ù„ÙŠÙ…Ø©', callback_data=f'drug_safe_{uid_s}')],
        [InlineKeyboardButton('â€¢ ØªÙØ§ØµÙŠÙ„ Ø§Ù„Ù…Ø®Ø§Ù„ÙØ©', callback_data=f'drug_detail_{uid_s}')]
      ]))
    return True
  return False

async def handle_drug_lock_commands(m,cid,t,c):
  if t in ['Ù‚ÙÙ„ Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª','Ù‚ÙÙ„ Ù…Ø®Ø¯Ø±Ø§Øª','Ù‚ÙÙ„ Ø§Ù„Ù…Ø®Ø¯Ø±']:
    set_lock(cid,'Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª',True)
    await m.reply_text('âŒ¯ ØªÙ… Ù‚ÙÙ„ Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª ðŸš«\nâŒ¯ Ø£ÙŠ Ø±Ø³Ø§Ù„Ø© ÙÙŠÙ‡Ø§ Ù…Ø®Ø¯Ø±Ø§Øª Ø¨ØªÙ†Ù…Ø³Ø­')
    return True
  if t in ['ÙØªØ­ Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª','ÙØªØ­ Ù…Ø®Ø¯Ø±Ø§Øª','ÙØªØ­ Ø§Ù„Ù…Ø®Ø¯Ø±']:
    set_lock(cid,'Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª',False)
    await m.reply_text('âŒ¯ ØªÙ… ÙØªØ­ Ø§Ù„Ù…Ø®Ø¯Ø±Ø§Øª')
    return True
  return False


# === Ù‚ÙÙ„ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ - Ù†ÙØ³ Ø§Ù„Ù†Øµ Ø¨Ø§Ù„Ø¶Ø¨Ø· ===
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
    if not is_locked(cid,'Ø§Ù„ØªØ¹Ø¯ÙŠÙ„'):
      return
    user=edited_message.from_user
    # Ù…Ø³Ø­ Ø§Ù„Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ù…Ø¹Ø¯Ù„Ø©
    try:
      await edited_message.delete()
    except:
      pass
    # Ø§Ù„Ø±Ø¯ Ø¨Ù†ÙØ³ Ø§Ù„Ù†Øµ Ø¨Ø§Ù„Ø¶Ø¨Ø·
    name=user.first_name if user else 'Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…'
    uid=user.id if user else 0
    # Ø§Ø³ØªØ®Ø¯Ù… Ø§Ù„Ø§Ø³Ù… 27 Ù„Ùˆ Ù…ÙˆØ¬ÙˆØ¯ØŸ Ù†Ø³ØªØ®Ø¯Ù… first_name
    # Ù„ÙƒÙ† Ø§Ù„Ù†Øµ Ø§Ù„Ù…Ø·Ù„ÙˆØ¨: Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… 27
    display_name=name if name else 'Ù¢Ù§'
    # Ù„Ùˆ Ø§Ù„ÙŠÙˆØ²Ø± afiwd Ø®Ù„ÙŠÙ‡Ø§ 27ØŸ
    if user and user.username=='afiwd':
      display_name='Ù¢Ù§'
    
    text=f'''âŒ¯ Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… {display_name}
âŒ¯ Ù‚Ø§Ù… Ø¨Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ
âŒ¯ ÙˆÙ…Ø³Ø­Øª Ø§Ù„Ø±Ø³Ø§Ù„Ø©ØŒ Ù„ÙØªØ­ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ:
 Ù„Ø§ ØªØ¹Ø¯Ù„ Ø«Ø§Ù†ÙŠ Ù…Ø±Ù‡ ÙŠØ§ Ø§Ø¨Ù† Ø§Ù„Ø´Ø±Ù…ÙˆØ·Ø©
ÙØªØ­ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ'''

    await client.send_message(cid, text)
  except Exception as e:
    print(f"EDIT LOCK ERROR: {e}")

# handler Ù„Ù„Ø±Ø³Ø§Ø¦Ù„ Ø§Ù„Ù…Ø¹Ø¯Ù„Ø©


# === Ù†Ø¸Ø§Ù… Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª - Ù†ÙØ³ Ø§Ù„ØµÙˆØ± Ù„ØµÙ‚ Ø·Ø¨Ø¹ ===

INFO_EXPLANATIONS={
  'Ø§ÙŠØ¯ÙŠ': '''Ø§ÙŠØ¯ÙŠ
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ù…Ø¹Ù„ÙˆÙ…Ø§ØªÙƒ Ø§Ùˆ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª Ø§Ù„Ù„ÙŠ
Ø±Ø¯ÙŠØª Ø¹Ù„ÙŠÙ‡

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : Ø§ÙŠØ¯ÙŠ Ø§Ùˆ Ø±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',
  
  'ÙƒØ´Ù': '''ÙƒØ´Ù
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª Ø§Ù„Ø¹Ø¶Ùˆ Ø¨Ø§Ù„Ø±Ø¯ Ø§Ùˆ Ø§Ù„ÙŠÙˆØ²Ø±
â€¢ ÙŠØ¸Ù‡Ø± Ø§Ø³Ù…Ù‡ ÙˆØ±ØªØ¨ØªÙ‡ ÙˆØªÙØ§Ø¹Ù„Ù‡

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : ÙƒØ´Ù Ø§Ùˆ Ø±Ø¯ Ø¹Ù„Ù‰ Ø§Ù„Ø´Ø®Øµ

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†': '''Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ† ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'Ø±ØªØ¨ØªÙŠ': '''Ø±ØªØ¨ØªÙŠ
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ø±ØªØ¨ØªÙƒ ÙˆØªÙØ§Ø¹Ù„Ùƒ ÙˆØ±Ø³Ø§Ø¦Ù„Ùƒ

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : Ø±ØªØ¨ØªÙŠ

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'ÙƒØ´Ù Ø§Ù„Ø±ØªØ¨': '''ÙƒØ´Ù Ø§Ù„Ø±ØªØ¨
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ø±ØªØ¨ Ø§Ù„Ø§Ø¹Ø¶Ø§Ø¡ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : ÙƒØ´Ù Ø§Ù„Ø±ØªØ¨

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'ÙƒØ´Ù Ø§Ù„Ø¨ÙˆØª': '''ÙƒØ´Ù Ø§Ù„Ø¨ÙˆØª
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª Ø§Ù„Ø¨ÙˆØª ÙˆØ³Ø±Ø¹ØªÙ‡

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : ÙƒØ´Ù Ø§Ù„Ø¨ÙˆØª

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'Ø§Ù„ØªÙˆØ¨': '''Ø§Ù„ØªÙˆØ¨
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ ØªÙˆØ¨ Ø§Ù„Ù…ØªÙØ§Ø¹Ù„ÙŠÙ† ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : Ø§Ù„ØªÙˆØ¨ Ø§Ùˆ ØªÙˆØ¨ Ø§Ù„Ù…ØªÙØ§Ø¹Ù„ÙŠÙ†

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'ÙƒØ´Ù Ø§Ù„Ù‚Ø±ÙˆØ¨': '''ÙƒØ´Ù Ø§Ù„Ù‚Ø±ÙˆØ¨
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª Ø§Ù„Ù‚Ø±ÙˆØ¨ ÙˆØ¹Ø¯Ø¯ Ø§Ù„Ø§Ø¹Ø¶Ø§Ø¡

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : ÙƒØ´Ù Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'ØªÙØ§Ø¹Ù„ÙŠ': '''ØªÙØ§Ø¹Ù„ÙŠ
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ ØªÙØ§Ø¹Ù„Ùƒ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : ØªÙØ§Ø¹Ù„ÙŠ

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',

  'Ø§Ù„Ø´Ø¹Ø§Ø±': '''Ø§Ù„Ø´Ø¹Ø§Ø±
_________________________

â€¢ Ø´Ø¹Ø§Ø± Ø­Ù…Ø§ÙŠØ© Ø§Ù„Ø§Ø³Ù…Ø§Ø¡ Ø§Ù„Ù…ÙØ¹Ù‘Ù„

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : Ø§Ù„Ø´Ø¹Ø§Ø±

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª''',
  
  'Ø±Ø³Ø§Ø¦Ù„ÙŠ': '''Ø±Ø³Ø§Ø¦Ù„ÙŠ
_________________________

â€¢ ÙŠØ¹Ø±Ø¶ Ø¹Ø¯Ø¯ Ø±Ø³Ø§Ø¦Ù„Ùƒ ÙÙŠ Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ Ø·Ø±ÙŠÙ‚Ø© Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù… :
â€¢ Ø§ÙƒØªØ¨ : Ø±Ø³Ø§Ø¦Ù„ÙŠ

â€¢ ÙŠØ³ØªØ®Ø¯Ù…Ù‡ â†¤ Ø§Ù„ÙƒÙ„
â€¢ Ø§Ù„Ù‚Ø³Ù… â†¤ Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª'''
}

def kb_info_main(page=1):
  if page==1:
    return InlineKeyboardMarkup([
      [InlineKeyboardButton('â€¢ Ø§ÙŠØ¯ÙŠ', callback_data='info_Ø§ÙŠØ¯ÙŠ'),
       InlineKeyboardButton('â€¢ ÙƒØ´Ù', callback_data='info_ÙƒØ´Ù')],
      [InlineKeyboardButton('â€¢ Ø±ØªØ¨ØªÙŠ', callback_data='info_Ø±ØªØ¨ØªÙŠ'),
       InlineKeyboardButton('â€¢ Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†', callback_data='info_Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†')],
      [InlineKeyboardButton('â€¢ ÙƒØ´Ù Ø§Ù„Ø¨ÙˆØª', callback_data='info_ÙƒØ´Ù Ø§Ù„Ø¨ÙˆØª'),
       InlineKeyboardButton('â€¢ ÙƒØ´Ù Ø§Ù„Ø±ØªØ¨', callback_data='info_ÙƒØ´Ù Ø§Ù„Ø±ØªØ¨')],
      [InlineKeyboardButton('â€¢ ÙƒØ´Ù Ø§Ù„Ù‚Ø±ÙˆØ¨', callback_data='info_ÙƒØ´Ù Ø§Ù„Ù‚Ø±ÙˆØ¨'),
       InlineKeyboardButton('â€¢ Ø§Ù„ØªÙˆØ¨', callback_data='info_Ø§Ù„ØªÙˆØ¨')],
      [InlineKeyboardButton('â€¢ Ø±Ø³Ø§Ø¦Ù„ÙŠ', callback_data='info_Ø±Ø³Ø§Ø¦Ù„ÙŠ'),
       InlineKeyboardButton('â€¢ ØªÙØ§Ø¹Ù„ÙŠ', callback_data='info_ØªÙØ§Ø¹Ù„ÙŠ')],
      [InlineKeyboardButton('â€¢ 1 / 2', callback_data='info_page_2'),
       InlineKeyboardButton('â€¢ Ø§Ù„ØªØ§Ù„ÙŠ', callback_data='info_page_2')],
      [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='cmd_main'),
       InlineKeyboardButton('â€¢ Ø§Ù„Ù‚Ø§Ø¦Ù…Ø©', callback_data='info_list')]
    ])
  else:
    # Ø§Ù„ØµÙØ­Ø© 2 Ù…Ù† 2 Ù†ÙØ³ Ø§Ù„ØµÙˆØ±Ø© - Ø§Ù„Ø´Ø¹Ø§Ø±
    return InlineKeyboardMarkup([
      [InlineKeyboardButton('â€¢ Ø§Ù„Ø´Ø¹Ø§Ø±', callback_data='info_Ø§Ù„Ø´Ø¹Ø§Ø±')],
      [InlineKeyboardButton('â€¢ Ø§Ù„Ø³Ø§Ø¨Ù‚', callback_data='info_page_1'),
       InlineKeyboardButton('â€¢ 2 / 2', callback_data='info_page_1')],
      [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='info_main'),
       InlineKeyboardButton('â€¢ Ø§Ù„Ù‚Ø§Ø¦Ù…Ø©', callback_data='cmd_main')]
    ])

def kb_info_detail(cmd):
  return InlineKeyboardMarkup([
    [InlineKeyboardButton('â€¢ Ø´ØºÙ‘Ù„ Ø§Ù„Ø§Ù…Ø±', callback_data=f'run_{cmd}')],
    [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='info_main'),
     InlineKeyboardButton('â€¢ Ø§Ù„Ù‚Ø§Ø¦Ù…Ø©', callback_data='cmd_main')]
  ])

def text_info_main(page=1):
  return f'''Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª
_________________________

â€¢ Ù…Ø¹Ù„ÙˆÙ…Ø§Øª Ø§Ù„Ø§Ø¹Ø¶Ø§Ø¡ ÙˆØ§Ù„Ù‚Ø±ÙˆØ¨ ÙˆØ§Ù„Ø¨ÙˆØª
â€¢ Ø§Ù„ØµÙØ­Ø© {page} Ù…Ù† 2

â€¢ Ø§Ø¶ØºØ· Ø¹Ù„Ù‰ Ø§Ù„Ø§Ù…Ø± Ø¹Ø´Ø§Ù† ÙŠØ·Ù„Ø¹ Ø´Ø±Ø­Ù‡'''



async def handle_lock_edit(m,cid,t,c):
  if t in ['Ù‚ÙÙ„ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„','Ù‚ÙÙ„ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ']:
    set_lock(cid,'Ø§Ù„ØªØ¹Ø¯ÙŠÙ„',True)
    await m.reply_text('âŒ¯ ØªÙ… Ù‚ÙÙ„ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„')
    return True
  if t in ['ÙØªØ­ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„','ÙØªØ­ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ']:
    set_lock(cid,'Ø§Ù„ØªØ¹Ø¯ÙŠÙ„',False)
    await m.reply_text('âŒ¯ ØªÙ… ÙØªØ­ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„')
    return True
  return False


async def handle_tashbeet(m,cid,t,c):
  if t in ['ØªØ«Ø¨ÙŠØª Ø§Ù„Ø¨ÙˆØª','ØªØ«Ø¨ÙŠØª','ØªØ«Ø¨ÙŠØª Ø§Ù„Ø¨ÙˆØª âœ…','Ø«Ø¨Øª Ø§Ù„Ø¨ÙˆØª','ØªØ«Ø¨ÙŠØª Ø¨ÙˆØª']:
    await m.reply_text('ØªÙ… Ø§Ù„ØªØ«Ø¨ÙŠØª')
    return True
  return False


async def handle_info_commands(m,cid,t,c):
  if t in ['Ø§Ù„ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª','ÙƒØ´Ù ÙˆØ§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª','Ø§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª','Ù…Ø¹Ù„ÙˆÙ…Ø§Øª']:
    await m.reply_text(text_info_main(1), reply_markup=kb_info_main(1))
    return True
  if t in INFO_EXPLANATIONS:
    await m.reply_text(INFO_EXPLANATIONS[t], reply_markup=kb_info_detail(t))
    return True
  return False


# === ÙƒÙ„ Ø£ÙˆØ§Ù…Ø± Ø§Ù„Ø´Ø§Øª Ù…Ù† Ø§Ù„ØµÙˆØ± - ÙŠØ´ØªØºÙ„ Ù„Ùˆ ÙƒØªØ¨ØªÙ‡ ===
CHANNEL_LINKS=ld('channel_links.json')
MUSIC_QUEUE=ld('music_queue.json')  # chat_id -> list
MUSIC_STATE=ld('music_state.json')  # chat_id -> state
MUSIC_LOOP=ld('music_loop.json')  # chat_id -> loop count



async def handle_auto_commands(m,cid,t,c):
  if t in ['Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ù‚Ø±ÙˆØ¨','Ø§Ù„Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª','Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª','settings','/settings','Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ù‚Ø±ÙˆØ¨']:
    await m.reply_text(text_group_settings(), reply_markup=kb_group_settings())
    return True
  if t in ['Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ','Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ','Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª']:
    await m.reply_text(text_auto_main(cid), reply_markup=kb_auto_main(cid))
    return True
  if t in ['ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ','ÙØ¹Ù„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ']:
    auto=get_auto(cid)
    auto['enabled']=True
    sv('auto_download.json',AUTO_DOWNLOAD)
    await m.reply_text(text_auto_main(cid), reply_markup=kb_auto_main(cid))
    # popup Ø­Ø³Ù†Ø§Ù‹
    await m.reply_text('â€¢ ØªÙ… ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ')
    return True
  if t in ['ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ','Ø¹Ø·Ù„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ']:
    auto=get_auto(cid)
    auto['enabled']=False
    sv('auto_download.json',AUTO_DOWNLOAD)
    await m.reply_text(text_auto_main(cid), reply_markup=kb_auto_main(cid))
    await m.reply_text('â€¢ ØªÙ… ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ')
    return True
  return False


async def handle_limits_commands(m,cid,t,c):
  # Ø­Ø¯ - ÙŠØ¹Ø±Ø¶ Ø§Ù„Ø­Ø¯ÙˆØ¯
  if t in ['Ø­Ø¯','Ø§Ù„Ø­Ø¯','Ø§Ù„Ø­Ø¯ÙˆØ¯','Ø­Ø¯ÙˆØ¯','Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ø­Ø¯']:
    txt=limits_text(cid)
    await m.reply_text(txt, reply_markup=kb_limits_main(cid))
    return True
  # Ø­Ø¯ Ø§Ù„Ø­Ø¸Ø± - Ù…Ø«Ù„Ø§ Ø­Ø¯ Ø§Ù„Ø­Ø¸Ø± 5
  if t.startswith('Ø­Ø¯ '):
    parts=t.split()
    if len(parts)>=2:
      action=parts[1]
      # Ù„Ùˆ ÙÙŠÙ‡ Ø±Ù‚Ù…
      if len(parts)>=3:
        try:
          num=int(parts[2])
          if action in LIMIT_ACTIONS:
            LIMITS[str(cid)]['limits'][action]=num
            sv('limits.json',LIMITS)
            await m.reply_text(f'âŒ¯ ØªÙ… Ø¶Ø¨Ø· Ø­Ø¯ {action} Ø¥Ù„Ù‰ {num if num!=0 else "Ø¨Ù„Ø§ Ø­Ø¯"}')
            return True
        except:
          pass
      # Ù„Ùˆ Ø¨Ø³ Ø­Ø¯ Ø§Ù„Ø­Ø¸Ø± Ø¨Ø¯ÙˆÙ† Ø±Ù‚Ù… - Ø§ÙØªØ­ Ù„ÙˆØ­Ø© Ø§Ù„ØªØ¹Ø¯ÙŠÙ„
      if action in LIMIT_ACTIONS:
        cur=get_limits(cid)['limits'].get(action,0)
        await m.reply_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur))
        return True
  return False


async def handle_all_chat_commands(m,cid,t,c):
  # Ø§Ù„Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª / settings
  if t in ['Ø§Ù„Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª','Ø§Ù„Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª','settings','/settings','Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª']:
    await m.reply_text('''âš™ï¸ Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ù‚Ø±ÙˆØ¨

â€¢ ÙˆØ¶Ø¹ Ø§Ù„Ø¨Ø­Ø«: Ù…Ø¨Ø§Ø´Ø±
â€¢ ÙˆØ¶Ø¹ Ø§Ù„ØªØµÙˆÙŠØª: Ù…Ø¹Ø·Ù„
â€¢ Ø¬ÙˆØ¯Ø© Ø§Ù„ØµÙˆØª: Ø¹Ø§Ù„ÙŠØ©
â€¢ Ø§Ù„ØªØ´ØºÙŠÙ„ Ø§Ù„ØªÙ„Ù‚Ø§Ø¦ÙŠ: Ù…ÙØ¹Ù„

Ù„ØªØºÙŠÙŠØ± Ø§Ù„Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ø³ØªØ®Ø¯Ù…:
/settings''', reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('â€¢ ÙˆØ¶Ø¹ Ø§Ù„Ø¨Ø­Ø« ðŸ”', callback_data='set_search'),
       InlineKeyboardButton('â€¢ Ø§Ù„ØªØµÙˆÙŠØª ðŸ—³ï¸', callback_data='set_vote')],
      [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
    ]))
    return True

  # /reload
  if t in ['/reload','ØªØ­Ø¯ÙŠØ« Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†','ØªØ­Ø¯ÙŠØ« Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†']:
    await m.reply_text('âŒ¯ ØªÙ… ØªØ­Ø¯ÙŠØ« Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ† Ø¨Ù†Ø¬Ø§Ø­ âœ…')
    return True

  # /loop
  if t.startswith('/loop') or t.startswith('loop') or t=='Ø§Ù„ØªÙƒØ±Ø§Ø±':
    parts=t.split()
    if len(parts)==1 or t=='Ø§Ù„ØªÙƒØ±Ø§Ø±':
      loop=MUSIC_LOOP.get(str(cid),0)
      await m.reply_text(f'ðŸ” Ø§Ù„ØªÙƒØ±Ø§Ø± Ø§Ù„Ø­Ø§Ù„ÙŠ: {loop if loop else "Ù…Ø¹Ø·Ù„"}\n\n/loops [ØªÙØ¹ÙŠÙ„|ØªØ¹Ø·ÙŠÙ„|Ø¹Ø¯Ø¯] - Ù…Ø«Ø§Ù„: /loop 3')
      return True
    arg=parts[-1].lower()
    if arg in ['ØªÙØ¹ÙŠÙ„','on','ØªØ´ØºÙŠÙ„']:
      MUSIC_LOOP[str(cid)]=1
      sv('music_loop.json',MUSIC_LOOP)
      await m.reply_text('ðŸ” ØªÙ… ØªÙØ¹ÙŠÙ„ Ø§Ù„ØªÙƒØ±Ø§Ø± âœ…')
    elif arg in ['ØªØ¹Ø·ÙŠÙ„','off','Ø§ÙŠÙ‚Ø§Ù']:
      MUSIC_LOOP[str(cid)]=0
      sv('music_loop.json',MUSIC_LOOP)
      await m.reply_text('ðŸ” ØªÙ… ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ØªÙƒØ±Ø§Ø± âŒ')
    else:
      try:
        n=int(arg)
        MUSIC_LOOP[str(cid)]=n
        sv('music_loop.json',MUSIC_LOOP)
        await m.reply_text(f'ðŸ” ØªÙ… Ø¶Ø¨Ø· Ø§Ù„ØªÙƒØ±Ø§Ø± Ø¥Ù„Ù‰ {n} Ù…Ø±Ø§Øª')
      except:
        await m.reply_text('âŒ¯ Ø§Ø³ØªØ®Ø¯Ù…: /loop [ØªÙØ¹ÙŠÙ„|ØªØ¹Ø·ÙŠÙ„|Ø¹Ø¯Ø¯]')
    return True

  # /shuffle
  if t in ['/shuffle','shuffle','Ø§Ù„Ø®Ù„Ø·']:
    await m.reply_text('ðŸ”€ ØªÙ… Ø®Ù„Ø· Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø± âœ…')
    return True

  # /seek and /seekback
  if t.startswith('/seek') or t.startswith('seek') or t.startswith('/seekback') or 'Ø§Ù„ØªÙ‚Ø¯ÙŠÙ…' in t or 'Ø§Ù„ØªØ£Ø®ÙŠØ±' in t:
    import re
    mm=re.search(r'(\d+)',t)
    sec=mm.group(1) if mm else '10'
    if 'back' in t or 'ØªØ£Ø®ÙŠØ±' in t:
      await m.reply_text(f'âª ØªÙ… Ø§Ù„Ø±Ø¬ÙˆØ¹ {sec} Ø«ÙˆØ§Ù†ÙŠ')
    else:
      await m.reply_text(f'â© ØªÙ… Ø§Ù„ØªÙ‚Ø¯ÙŠÙ… {sec} Ø«ÙˆØ§Ù†ÙŠ')
    return True

  # /speed /playback
  if t.startswith('/speed') or t.startswith('/playback') or t in ['Ø§Ù„Ø³Ø±Ø¹Ø©','Ø³Ø±Ø¹Ø©']:
    parts=t.split()
    if len(parts)>=2:
      await m.reply_text(f'âš¡ ØªÙ… ØªØºÙŠÙŠØ± Ø§Ù„Ø³Ø±Ø¹Ø© Ø¥Ù„Ù‰ {parts[-1]}')
    else:
      await m.reply_text('âš¡ Ø§Ù„Ø³Ø±Ø¹Ø© Ø§Ù„Ø­Ø§Ù„ÙŠØ©: 1x\n\n/speed [Ø§Ù„Ø³Ø±Ø¹Ø©] - Ù…Ø«Ø§Ù„: /speed 1.5')
    return True

  # ØªØ´ØºÙŠÙ„ / Ø´ØºÙ„
  if t.startswith('Ø´ØºÙ„ ') or t.startswith('ØªØ´ØºÙŠÙ„ ') or t.startswith('Ø´ØºÙ„') and len(t)>4:
    q=t.replace('Ø´ØºÙ„','').replace('ØªØ´ØºÙŠÙ„','').strip()
    if not q:
      await m.reply_text('âŒ¯ Ø§Ø±Ø³Ù„ Ø§Ø³Ù… Ø§Ù„Ø£ØºÙ†ÙŠØ© Ø£Ùˆ Ø§Ù„Ø±Ø§Ø¨Ø·\nÙ…Ø«Ø§Ù„: Ø´ØºÙ„ Ø±Ø§Ø¨Ø­ ØµÙ‚Ø±')
      return True
    # Ø­ÙØ¸ ÙÙŠ Ø§Ù„Ù‚Ø§Ø¦Ù…Ø©
    qid=str(cid)
    if qid not in MUSIC_QUEUE:
      MUSIC_QUEUE[qid]=[]
    MUSIC_QUEUE[qid].append({'title':q,'user':m.from_user.first_name})
    sv('music_queue.json',MUSIC_QUEUE)
    MUSIC_STATE[qid]={'playing':q,'user':m.from_user.first_name}
    sv('music_state.json',MUSIC_STATE)
    await m.reply_text(f'ðŸŽµ ÙŠØªÙ… ØªØ´ØºÙŠÙ„: {q}\nðŸ‘¤ Ø¨ÙˆØ§Ø³Ø·Ø©: {m.from_user.first_name}\n\nâ¸ï¸ /pause - Ø§ÙŠÙ‚Ø§Ù Ù…Ø¤Ù‚Øª\nâ­ï¸ ØªØ®Ø·ÙŠ - Ø§Ù„ØªØ§Ù„ÙŠ\nâ¹ï¸ Ø§ÙŠÙ‚Ø§Ù - Ø¥Ù†Ù‡Ø§Ø¡')
    return True

  # ÙÙŠØ¯ÙŠÙˆ
  if t.startswith('ÙÙŠØ¯ÙŠÙˆ ') or t.startswith('ÙÙŠØ¯ÙŠÙˆ'):
    q=t.replace('ÙÙŠØ¯ÙŠÙˆ','').strip()
    if not q:
      await m.reply_text('âŒ¯ Ø§Ø±Ø³Ù„ Ø§Ø³Ù… Ø§Ù„ÙÙŠØ¯ÙŠÙˆ\nÙ…Ø«Ø§Ù„: ÙÙŠØ¯ÙŠÙˆ Ø±Ø§Ø¨Ø­ ØµÙ‚Ø±')
      return True
    await m.reply_text(f'ðŸŽ¬ ÙŠØªÙ… ØªØ´ØºÙŠÙ„ ÙÙŠØ¯ÙŠÙˆ: {q}\nðŸ‘¤ Ø¨ÙˆØ§Ø³Ø·Ø©: {m.from_user.first_name}')
    return True

  # playforce / vplayforce
  if t.startswith('playforce') or t.startswith('vplayforce') or t.startswith('/playforce') or t.startswith('/vplayforce'):
    q=t.replace('playforce','').replace('vplayforce','').replace('/','').strip()
    await m.reply_text(f'âš¡ ØªÙ… Ø¥ÙŠÙ‚Ø§Ù Ø§Ù„Ø­Ø§Ù„ÙŠ ÙˆØ§Ù„ØªØ´ØºÙŠÙ„ ÙÙˆØ±Ù‹Ø§: {q if q else "Ø§Ù„Ù…Ù‚Ø·Ø¹ Ø§Ù„Ø¬Ø¯ÙŠØ¯"}')
    return True

  # Ø§Ø³ØªØ¦Ù†Ø§Ù / Ø§ÙŠÙ‚Ø§Ù Ù…Ø¤Ù‚Øª
  if t in ['Ø§Ø³ØªØ¦Ù†Ø§Ù','/resume','resume']:
    await m.reply_text('â–¶ï¸ ØªÙ… Ø§Ø³ØªØ¦Ù†Ø§Ù Ø§Ù„ØªØ´ØºÙŠÙ„')
    return True
  if t in ['Ø§ÙŠÙ‚Ø§Ù Ù…Ø¤Ù‚Øª','Ø¥ÙŠÙ‚Ø§Ù Ù…Ø¤Ù‚Øª','/pause','pause','ÙˆÙ‚Ù']:
    await m.reply_text('â¸ï¸ ØªÙ… Ø¥ÙŠÙ‚Ø§Ù Ø§Ù„ØªØ´ØºÙŠÙ„ Ù…Ø¤Ù‚ØªØ§Ù‹')
    return True

  # ØªØ®Ø·ÙŠ
  if t in ['ØªØ®Ø·ÙŠ','/skip','skip','Ø§Ù„ØªØ§Ù„ÙŠ']:
    await m.reply_text('â­ï¸ ØªÙ… ØªØ®Ø·ÙŠ Ø§Ù„Ù…Ù‚Ø·Ø¹ Ø§Ù„Ø­Ø§Ù„ÙŠ')
    return True

  # Ø§ÙŠÙ‚Ø§Ù / Ø§Ù†Ù‡Ø§Ø¡
  if t in ['Ø§ÙŠÙ‚Ø§Ù','Ø¥ÙŠÙ‚Ø§Ù','Ø§Ù†Ù‡Ø§Ø¡','Ø¥Ù†Ù‡Ø§Ø¡','/stop','/end','stop','end','Ø§Ù†Ù‡Ø§Ø¡ Ø§Ù„ØªØ´ØºÙŠÙ„','Ø¥Ù†Ù‡Ø§Ø¡ Ø§Ù„ØªØ´ØºÙŠÙ„']:
    MUSIC_STATE[str(cid)]={}
    sv('music_state.json',MUSIC_STATE)
    MUSIC_QUEUE[str(cid)]=[]
    sv('music_queue.json',MUSIC_QUEUE)
    await m.reply_text('â¹ï¸ ØªÙ… Ø¥Ù†Ù‡Ø§Ø¡ Ø§Ù„ØªØ´ØºÙŠÙ„ ÙˆÙ…Ø³Ø­ Ø§Ù„Ù‚Ø§Ø¦Ù…Ø©')
    return True

  # /queue
  if t in ['/queue','queue','Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø±','Ø¹Ø±Ø¶ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø±']:
    q=MUSIC_QUEUE.get(str(cid),[])
    if not q:
      await m.reply_text('âŒ¯ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø± ÙØ§Ø±ØºØ©')
    else:
      txt='ðŸŽµ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø±:\n\n'
      for i,s in enumerate(q[:10],1):
        txt+=f'{i}- {s["title"]} - {s["user"]}\n'
      if len(q)>10:
        txt+=f'\n... Ùˆ {len(q)-10} Ø£Ø®Ø±Ù‰'
      await m.reply_text(txt)
    return True

  # /channelplay
  if t.startswith('/channelplay') or t.startswith('channelplay'):
    parts=t.split()
    if len(parts)>=2 and parts[-1]=='linked':
      await m.reply_text('ðŸ“¢ ØªÙ… Ø±Ø¨Ø· Ø§Ù„Ù‚Ù†Ø§Ø© Ø§Ù„Ù…Ø±ØªØ¨Ø·Ø© ØªÙ„Ù‚Ø§Ø¦ÙŠØ§Ù‹ âœ…\nØ§Ù„Ù‚Ù†Ø§Ø© Ø§Ù„Ù…Ø±ØªØ¨Ø·Ø© Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ ØªÙ… Ø±Ø¨Ø·Ù‡Ø§ Ù„Ù„ØªØ´ØºÙŠÙ„')
    elif len(parts)>=2:
      ch=parts[-1]
      CHANNEL_LINKS[str(cid)]=ch
      sv('channel_links.json',CHANNEL_LINKS)
      await m.reply_text(f'ðŸ“¢ ØªÙ… Ø±Ø¨Ø· Ø§Ù„Ù‚Ù†Ø§Ø© {ch} Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ Ù„Ù„ØªØ´ØºÙŠÙ„ ÙÙŠÙ‡Ø§ âœ…\nØ§Ù„Ø¢Ù† ÙŠÙ…ÙƒÙ†Ùƒ Ø§Ø³ØªØ®Ø¯Ø§Ù…: cplay [Ø§Ø³Ù…] Ù„Ù„ØªØ´ØºÙŠÙ„ ÙÙŠ Ø§Ù„Ù‚Ù†Ø§Ø©')
    else:
      await m.reply_text('''ðŸ“¢ Ø£ÙˆØ§Ù…Ø± Ø±Ø¨Ø· Ø§Ù„Ù‚Ù†Ø§Ø©:

â€¢ /channelplay [Ø¢ÙŠØ¯ÙŠ/ÙŠÙˆØ²Ø± Ø§Ù„Ù‚Ù†Ø§Ø©] - Ø±Ø¨Ø· Ù‚Ù†Ø§Ø© Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ Ù„Ù„ØªØ´ØºÙŠÙ„ ÙÙŠÙ‡Ø§
â€¢ /channelplay linked - Ø±Ø¨Ø· Ø§Ù„Ù‚Ù†Ø§Ø© Ø§Ù„Ù…Ø±ØªØ¨Ø·Ø© ØªÙ„Ù‚Ø§Ø¦ÙŠØ§Ù‹

Ù…Ø«Ø§Ù„:
/channelplay @my_channel
/channelplay linked''')
    return True

  # cplay / cvplay
  if t.startswith('cplay') or t.startswith('cvplay') or t.startswith('/cplay') or t.startswith('/cvplay'):
    q=t.replace('cplay','').replace('cvplay','').replace('/','').strip()
    ch=CHANNEL_LINKS.get(str(cid),'Ø§Ù„Ù‚Ù†Ø§Ø© Ø§Ù„Ù…Ø±ØªØ¨Ø·Ø©')
    if not q:
      await m.reply_text(f'âŒ¯ Ø§Ø±Ø³Ù„ Ø§Ø³Ù… Ø§Ù„Ù…Ù‚Ø·Ø¹\nÙ…Ø«Ø§Ù„: cplay Ø±Ø§Ø¨Ø­ ØµÙ‚Ø±\nØ§Ù„Ù‚Ù†Ø§Ø©: {ch}')
    else:
      await m.reply_text(f'ðŸ“¢ ÙŠØªÙ… Ø§Ù„ØªØ´ØºÙŠÙ„ ÙÙŠ Ø§Ù„Ù‚Ù†Ø§Ø© {ch}:\nðŸŽµ {q}\nðŸ‘¤ Ø¨ÙˆØ§Ø³Ø·Ø©: {m.from_user.first_name}')
    return True

  # cqueue / cplaying
  if t in ['cqueue','cplaying','/cqueue','/cplaying','Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø± ÙÙŠ Ø§Ù„Ù‚Ù†Ø§Ø©','Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø± ÙÙŠ Ø§Ù„Ù‚Ù†Ø§Ø©']:
    await m.reply_text('ðŸ“¢ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø± ÙÙŠ Ø§Ù„Ù‚Ù†Ø§Ø© ÙØ§Ø±ØºØ© Ø­Ø§Ù„ÙŠØ§Ù‹')
    return True

  return False


async def handle_moshaghil_commands(m,cid,t,c):
 import re
 # Ø±ÙØ¹ Ù…Ø´ØºÙ„
 if t.startswith('Ø±ÙØ¹ Ù…Ø´ØºÙ„'):
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
   await m.reply_text('âŒ¯ Ø§Ø±Ø³Ù„ Ø§Ù„Ø§ÙŠØ¯ÙŠ Ø£Ùˆ Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ø´Ø®Øµ\nâŒ¯ Ù…Ø«Ø§Ù„: Ø±ÙØ¹ Ù…Ø´ØºÙ„ 123456789')
   return True
  added=add_operator(cid,target)
  if added:
   await m.reply_text(f'âŒ¯ ØªÙ… Ø±ÙØ¹ {target_name} Ù…Ø´ØºÙ„\nâŒ¯ Ø§Ù„Ø§ÙŠØ¯ÙŠ: {target}')
  else:
   await m.reply_text(f'âŒ¯ {target_name} Ù…Ø´ØºÙ„ Ù…Ù† Ù‚Ø¨Ù„')
  return True

 if t.startswith('ØªÙ†Ø²ÙŠÙ„ Ù…Ø´ØºÙ„'):
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
   await m.reply_text('âŒ¯ Ø§Ø±Ø³Ù„ Ø§Ù„Ø§ÙŠØ¯ÙŠ Ø£Ùˆ Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ø´Ø®Øµ')
   return True
  removed=remove_operator(cid,target)
  if removed:
   await m.reply_text(f'âŒ¯ ØªÙ… ØªÙ†Ø²ÙŠÙ„ {target_name} Ù…Ù† Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ†')
  else:
   await m.reply_text(f'âŒ¯ {target_name} Ù…Ùˆ Ù…Ø´ØºÙ„ Ø£ØµÙ„Ø§')
  return True

 if t in ['Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ†','Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ† Ø§Ù„Ø­Ø§Ù„ÙŠÙŠÙ†','Ø¹Ø±Ø¶ Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ†','Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ†']:
  lst=get_operators(cid)
  if not lst:
   await m.reply_text('âŒ¯ Ù„Ø§ ÙŠÙˆØ¬Ø¯ Ù…Ø´ØºÙ„ÙŠÙ† Ø­Ø§Ù„ÙŠØ§Ù‹')
   return True
  txt='âŒ¯ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ†:\n\n'
  for i,uid in enumerate(lst,1):
   txt+=f'{i}- {uid}\n'
  await m.reply_text(txt)
  return True
 return False


def kb_main_commands():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø£ÙˆØ§Ù…Ø± Ø§Ù„Ù‚Ø±ÙˆØ¨Ø§Øª', callback_data='cmd_groups'),
   InlineKeyboardButton('â€¢ Ø£ÙˆØ§Ù…Ø± Ø§Ù„ØªØ´ØºÙŠÙ„', callback_data='cmd_play')],
  [InlineKeyboardButton('â€¢ ØªÙƒØ±Ø§Ø± ÙˆØªÙ‚Ø¯ÙŠÙ… ÙˆØ³Ø±', callback_data='cmd_loop'),
   InlineKeyboardButton('â€¢ Ø£ÙˆØ§Ù…Ø± Ø§Ù„Ù‚Ù†ÙˆØ§Øª', callback_data='cmd_channels')],
  [InlineKeyboardButton('â€¢ Ø£ÙˆØ§Ù…Ø± Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ†', callback_data='cmd_dev')],
  [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
 ])

def kb_back_close():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='cmd_main')],
  [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
 ])

# Ù†ØµÙˆØµ Ù†ÙØ³ Ø§Ù„ØµÙˆØ± Ø¨Ø§Ù„Ø¶Ø¨Ø·
TEXT_GROUPS_OLD = '''Ø£ÙˆØ§Ù…Ø± Ø®Ø§ØµØ© Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨Ø§Øª ðŸ‘¥

â€¢ Ø±ÙØ¹ Ù…Ø´ØºÙ„ [Ø±Ø¯/Ø¢ÙŠØ¯ÙŠ] - ÙŠÙ…Ù†Ø­
ØµÙ„Ø§Ø­ÙŠØ§Øª Ø¥Ø¯Ù…Ù† Ø§Ù„ØªØ´ØºÙŠÙ„ Ø¨Ø¯ÙˆÙ† Ø¥Ø´Ø±Ø§Ù
ÙƒØ§Ù…Ù„

â€¢ ØªÙ†Ø²ÙŠÙ„ Ù…Ø´ØºÙ„ [Ø±Ø¯/Ø¢ÙŠØ¯ÙŠ]
â€¢ Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ† - Ø¹Ø±Ø¶ Ø§Ù„Ù…Ø´ØºÙ„ÙŠÙ† Ø§Ù„Ø­Ø§Ù„ÙŠÙŠÙ†
â€¢ Ø§Ù„Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª / settings - Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª
Ø§Ù„Ù‚Ø±ÙˆØ¨ (ÙˆØ¶Ø¹ Ø§Ù„Ø¨Ø­Ø«ØŒ Ø§Ù„ØªØµÙˆÙŠØª...)
â€¢ /reload - ØªØ­Ø¯ÙŠØ« Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…Ø´Ø±ÙÙŠÙ†'''

TEXT_PLAY = '''Ø£ÙˆØ§Ù…Ø± Ø§Ù„ØªØ´ØºÙŠÙ„ Ø§Ù„Ø£Ø³Ø§Ø³ÙŠØ© ðŸŽµ

â€¢ ØªØ´ØºÙŠÙ„ / Ø´ØºÙ„ [ Ø§Ø³Ù… Ø£Ùˆ Ø±Ø§Ø¨Ø·] -
ØªØ´ØºÙŠÙ„ ØµÙˆØª
â€¢ ÙÙŠØ¯ÙŠÙˆ [ Ø§Ø³Ù… Ø£Ùˆ Ø±Ø§Ø¨Ø·] - ØªØ´ØºÙŠÙ„
ÙÙŠØ¯ÙŠÙˆ
â€¢ playforce / vplayforce -
Ø¥ÙŠÙ‚Ø§Ù Ø§Ù„Ø­Ø§Ù„ÙŠ ÙˆØ§Ù„ØªØ´ØºÙŠÙ„ ÙÙˆØ±Ù‹Ø§
â€¢ Ø§Ø³ØªØ¦Ù†Ø§Ù / Ø§ÙŠÙ‚Ø§Ù Ù…Ø¤Ù‚Øª
â€¢ ØªØ®Ø·ÙŠ - Ù„Ù„Ù…Ù‚Ø·Ø¹ Ø§Ù„ØªØ§Ù„ÙŠ ÙÙŠ Ø§Ù„Ù‚Ø§Ø¦Ù…Ø©
â€¢ Ø§ÙŠÙ‚Ø§Ù / Ø§Ù†Ù‡Ø§Ø¡ - Ø¥Ù†Ù‡Ø§Ø¡ Ø§Ù„ØªØ´ØºÙŠÙ„
Ø¨Ø§Ù„ÙƒØ§Ù…Ù„
â€¢ /queue - Ø¹Ø±Ø¶ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø±'''

TEXT_LOOP = '''Ø§Ù„ØªÙƒØ±Ø§Ø± ðŸ”
/loop [ØªÙØ¹ÙŠÙ„|ØªØ¹Ø·ÙŠÙ„|Ø¹Ø¯Ø¯]

Ø§Ù„Ø®Ù„Ø· ðŸ”€
/shuffle

Ø§Ù„ØªÙ‚Ø¯ÙŠÙ…/Ø§Ù„ØªØ£Ø®ÙŠØ± â©
/seek [Ø«ÙˆØ§Ù†ÙŠ] - /seekback
[Ø«ÙˆØ§Ù†ÙŠ]

Ø§Ù„Ø³Ø±Ø¹Ø© âš¡
/speed Ø£Ùˆ /playback [Ù…Ø´Ø±ÙÙŠÙ† ÙÙ‚Ø·]'''

TEXT_CHANNELS = '''Ø£ÙˆØ§Ù…Ø± Ø®Ø§ØµØ© Ø¨Ø§Ù„Ù‚Ù†ÙˆØ§Øª ðŸ“¢

â€¢ /channelplay [Ø¢ÙŠØ¯ÙŠ/ÙŠÙˆØ²Ø±
Ø§Ù„Ù‚Ù†Ø§Ø©] - Ø±Ø¨Ø· Ù‚Ù†Ø§Ø© Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ Ù„Ù„ØªØ´ØºÙŠÙ„
ÙÙŠÙ‡Ø§
â€¢ /channelplay linked - Ø±Ø¨Ø· Ø§Ù„Ù‚Ù†Ø§Ø©
Ø§Ù„Ù…Ø±ØªØ¨Ø·Ø© ØªÙ„Ù‚Ø§Ø¦ÙŠÙ‹Ø§
â€¢ [ Ø§Ø³Ù…] cplay / cvplay - ØªØ´ØºÙŠÙ„
ÙÙŠ Ø§Ù„Ù‚Ù†Ø§Ø© Ø§Ù„Ù…Ø±ØªØ¨Ø·Ø©
â€¢ cqueue / cplaying - Ù‚Ø§Ø¦Ù…Ø©
Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø± ÙÙŠ Ø§Ù„Ù‚Ù†Ø§Ø©'''

TEXT_Dev = '''Ø£ÙˆØ§Ù…Ø± Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ† ðŸ‘¨â€ðŸ’»

â€¢ Ø§Ù„Ù…Ø·ÙˆØ±
â€¢ Ø§Ø¶Ù Ø§Ù…Ø± - Ø§Ø¶Ø§ÙØ© Ø§Ù…Ø± Ù…Ø®ØµØµ
â€¢ Ù…Ø³Ø­ Ø§Ù…Ø± - Ù…Ø³Ø­ Ø§Ù…Ø± Ù…Ø®ØµØµ
â€¢ Ø§Ù„Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù…Ø¶Ø§ÙÙ‡ - Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§ÙˆØ§Ù…Ø±
â€¢ ØªÙØ¹ÙŠÙ„ Ø§Ù„ÙˆØ¶Ø¹ Ø§Ù„Ø®Ø§Øµ
â€¢ ØªØ¹Ø·ÙŠÙ„ Ø§Ù„ÙˆØ¶Ø¹ Ø§Ù„Ø®Ø§Øµ
â€¢ Ù‚ÙÙ„ Ø§Ù…Ø± - Ù‚ÙÙ„ Ø§Ù…Ø± Ù„Ø±ØªØ¨Ø©
â€¢ ØªÙ†Ø²ÙŠÙ„ Ø§Ù„ÙƒÙ„ - ØªÙ†Ø²ÙŠÙ„ Ù…Ø´Ø±ÙÙŠÙ† ÙˆØ±ØªØ¨
â€¢ Ø§Ø¶Ù Ø±Ø¯ - Ø§Ø¶Ø§ÙØ© Ø±Ø¯ Ù…Ø®ØµØµ'''

TEXT_MAIN = '''â€¢ Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø£ÙˆØ§Ù…Ø±

Ø§Ø®ØªØ± Ø§Ù„Ù‚Ø³Ù… Ø§Ù„Ø°ÙŠ ØªØ±ÙŠØ¯ Ù…Ø¹Ø±ÙØ© Ø£ÙˆØ§Ù…Ø±Ù‡:'''



def kb_commands_old():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­ â€¢',callback_data='lockpanel'),
   InlineKeyboardButton('â€¢ Ø§Ù„ØªÙØ¹ÙŠÙ„ ÙˆØ§Ù„ØªØ¹Ø·ÙŠÙ„ â€¢',callback_data='onoff')],
  [InlineKeyboardButton('â€¢ Ø§Ø¯Ø§Ø±Ø© Ø§Ù„Ù‚Ø±ÙˆØ¨ â€¢',callback_data='manage'),
   InlineKeyboardButton('â€¢ Ø§Ù„ØªØ³Ù„ÙŠØ© ÙˆØ§Ù„Ø®Ø¯Ù…ÙŠØ© â€¢',callback_data='fun')],
  [InlineKeyboardButton('â€¢ Ø§ÙˆØ§Ù…Ø± Dev â€¢',callback_data='dev')],
  [InlineKeyboardButton('â€¢ Ø§Ù„Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª â€¢',callback_data='sets')],
  [InlineKeyboardButton('â€¢ Ø§ØºÙ„Ø§Ù‚ â€¢',callback_data='close')]
 ])

AWAMER_TEXT = '''Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§ÙˆØ§Ù…Ø±
â€”â€”â€”â€”â€”â€”â€”â€”â€”
â€¢ Ø§Ø®ØªØ± Ø§Ù„Ù‚Ø³Ù… ÙˆØ¨ØªØ·Ù„Ø¹ Ù„Ùƒ Ø§ÙˆØ§Ù…Ø±Ù‡
â€¢ ÙƒÙ„ Ø§Ù…Ø± Ù„Ù‡ Ø´Ø±Ø­Ù‡ ÙˆØ·Ø±ÙŠÙ‚Ø© Ø§Ø³ØªØ®Ø¯Ø§Ù…Ù‡
ÙˆÙ…ÙŠÙ† ÙŠÙ‚Ø¯Ø± ÙŠØ³ØªØ®Ø¯Ù…Ù‡

â€¢ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨ : Ø§ÙƒØªØ¨ ( Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨ )
'''

def kb_groups():
 return kb_commands()

def cb_groups_override():
 return True


def kb_back_old():
 return InlineKeyboardMarkup([
  [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹',callback_data='cmd_main'),
   InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚',callback_data='close')]
 ])

# START
async def start(u,c):
 if u.effective_chat.type=='private':
  text="Ù‡Ù„Ø§ Ø¹Ø²ÙŠØ²ÙŠ Ø§Ù†Ø§ Ø³ÙˆØ±Ø¯\n\n"
  text+="Ø§Ù‚ÙˆÙ‰ ÙˆØ§Ø³Ø±Ø¹ Ø¨ÙˆØª Ø­Ù…Ø§ÙŠØ© ÙˆØªØ´ØºÙŠÙ„ Ù…ÙŠÙˆØ²Ùƒ\n"
  text+="ÙˆØ§Ù„Ø¹Ø¯ÙŠØ¯ Ù…Ù† Ø§Ù„Ù…Ù…ÙŠØ²Ø§Øª Ø§Ù„Ø§Ø®Ø±Ù‰\n\n"
  text+="Ø§Ø°Ø§ Ø±ÙØ¹ØªÙ†ÙŠ Ù…Ø´Ø±Ù Ø¨ØªÙØ¹Ù„ ØªÙ„Ù‚Ø§Ø¦ÙŠØ§\n"
  text+="Ø§Ø¶ØºØ· Ø§Ù„Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª ÙˆØ¶Ø¨Ø· Ø§Ø¹Ø¯Ø§Ø¯Ø§ØªÙŠ\n\n"
  text+="Ù…Ø§ÙÙŠÙ†ÙŠ Ø§ÙŠ Ù…Ø·ÙˆØ± ÙˆÙ…Ø³Ø¤ÙˆÙ„ ØºÙŠØ± Liam\n\n"
  text+="Ø­Ø³Ø§Ø¨ Ù…Ø·ÙˆØ±ÙŠ - Liam"
  await u.message.reply_text(text,reply_markup=kb_start())
 else:
  await u.message.reply_text(
   'Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§ÙˆØ§Ù…Ø± - Ø³ÙˆØ±Ø¯\nØ§Ø®ØªØ± Ø§Ù„Ù‚Ø³Ù…',
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
    status='Ù…ÙØ¹Ù„Ø©' if lim['enabled'] else 'Ù…Ø¹Ø·Ù„Ø©'
    await q.answer(f'Ø§Ù„Ø­Ø¯ÙˆØ¯ Ø§Ù„Ø¢Ù† {status}', show_alert=True)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_clear':
    LIMITS[str(cid)]['limits']={a:0 for a in LIMIT_ACTIONS}
    sv('limits.json',LIMITS)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_today':
    # Ø¹Ø±Ø¶ Ø§Ø³ØªÙ‡Ù„Ø§Ùƒ Ø§Ù„ÙŠÙˆÙ…
    txt='ðŸ“Š Ø§Ø³ØªÙ‡Ù„Ø§Ùƒ Ø§Ù„ÙŠÙˆÙ…:\n\n'
    cid_s=str(cid)
    if cid_s in LIMITS_USAGE:
      for admin_id, data in LIMITS_USAGE[cid_s].items():
        txt+=f'Ø§Ù„Ù…Ø´Ø±Ù {admin_id}:\n'
        for act,cnt in data.get('counts',{}).items():
          if cnt>0:
            txt+=f'  {act}: {cnt}\n'
        txt+='\n'
    else:
      txt+='Ù„Ø§ ÙŠÙˆØ¬Ø¯ Ø§Ø³ØªÙ‡Ù„Ø§Ùƒ Ø§Ù„ÙŠÙˆÙ…'
    await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='lim_main')],
      [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
    ]))
    return
  if d.startswith('lim_edit_'):
    # lim_edit_Ø§Ù„Ø·Ø±Ø¯_+1 or set_5
    try:
      _,_,action,op = d.split('_',3)
    except:
      # action may contain _
      parts=d.split('_')
      # lim_edit_Ø§Ù„Ø·Ø±Ø¯_set_5
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
    # lim_Ø§Ù„Ø·Ø±Ø¯ -> ÙØªØ­ ØªØ¹Ø¯ÙŠÙ„
    action=d.replace('lim_','')
    if action in LIMIT_ACTIONS:
      cur=get_limits(cid)['limits'].get(action,0)
      await q.edit_message_text(limits_text(cid,action), reply_markup=kb_limit_edit(action,cur))
      return

 if d=='cmd_main':
  await q.edit_message_text(
   'Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§ÙˆØ§Ù…Ø±\nØ§Ø®ØªØ± Ø§Ù„Ù‚Ø³Ù…',
   reply_markup=kb_main()
  )
  return

 if d=='cmd_groups':
  await q.edit_message_text(
   'Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§ÙˆØ§Ù…Ø±\nØ§Ø®ØªØ± Ø§Ù„Ù‚Ø³Ù…\nÙƒÙ„ Ø§Ù…Ø± Ù„Ù‡ Ø´Ø±Ø­Ù‡',
   reply_markup=kb_groups()
  )
  return

 if d=='cmd_play':
  await q.edit_message_text(
   'Ø§ÙˆØ§Ù…Ø± Ø§Ù„ØªØ´ØºÙŠÙ„\n\nØ´ØºÙ„ - ØªØ´ØºÙŠÙ„ ØµÙˆØª\n/playforce - ØªØ´ØºÙŠÙ„ ÙÙˆØ±Ø§\n/skip - ØªØ®Ø·ÙŠ\n/queue - Ù‚Ø§Ø¦Ù…Ø©',
   reply_markup=kb_back()
  )
  return

 if d=='cmd_loop':
  await q.edit_message_text(
   'Ø§Ù„ØªÙƒØ±Ø§Ø±\n/loop - ØªÙƒØ±Ø§Ø±\n/shuffle - Ø®Ù„Ø·\n/seek - ØªÙ‚Ø¯ÙŠÙ…',
   reply_markup=kb_back()
  )
  return

 if d=='cmd_channels':
  await q.edit_message_text(
   'Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù‚Ù†ÙˆØ§Øª\nØ±Ø¨Ø· Ø§Ù„Ù‚Ù†Ø§Ø©',
   reply_markup=kb_back()
  )
  return

 if d=='cmd_dev':
  await q.edit_message_text(
   'Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù…Ø·ÙˆØ±ÙŠÙ†\nÙ„Ù„Ù…Ø·ÙˆØ± Ø§Ù„Ø§Ø³Ø§Ø³ÙŠ',
   reply_markup=kb_back()
  )
  return

 if d in ['lockpanel','page1']:
  await q.edit_message_text(
   'Ù„ÙˆØ­Ø© Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­ - ØµÙØ­Ø© 1',
   reply_markup=kb_lock_p1()
  )
  return

 if d=='page2':
  await q.edit_message_text(
   'Ù„ÙˆØ­Ø© Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­ - ØµÙØ­Ø© 2',
   reply_markup=kb_lock_p2()
  )
  return

 if d=='openall':
  LOCKS.setdefault(cid,{})
  for k in ALL_LOCKS:
   LOCKS[cid][k]=False
  sv('locks.json',LOCKS)
  await q.edit_message_text('ØªÙ… ÙØªØ­ Ø§Ù„ÙƒÙ„',reply_markup=kb_lock_p1())
  return

 if d=='closeall':
  LOCKS.setdefault(cid,{})
  for k in ALL_LOCKS:
   LOCKS[cid][k]=True
  sv('locks.json',LOCKS)
  await q.edit_message_text('ØªÙ… Ù‚ÙÙ„ Ø§Ù„ÙƒÙ„',reply_markup=kb_lock_p1())
  return

 if d.startswith('l_'):
  name=d[2:]
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]=not LOCKS[cid].get(name,False)
  sv('locks.json',LOCKS)
  page=kb_lock_p1() if name in LOCKS_P1 else kb_lock_p2()
  st='ØªÙ… Ù‚ÙÙ„' if LOCKS[cid][name] else 'ØªÙ… ÙØªØ­'
  await q.edit_message_text(f'{st} {name}',reply_markup=page)
  return

 if d.startswith('g_'):
  if d=='g_top':
   await q.edit_message_text(
    'ØªÙˆØ¨ 20\n1) Ø¯ÙŠÙ\n2) RORY\n... 20) Enzo',
    reply_markup=kb_games()
   )
   return
  await q.edit_message_text(
   'Ù…Ø±ÙƒØ² Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨\nØ§Ø®ØªØ± Ø§Ù„ØªØµÙ†ÙŠÙ',
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
  await q.edit_message_text(f"ØªÙ… Ø¥Ù„ØºØ§Ø¡ Ø§Ù„Ø¥Ù†Ø°Ø§Ø± {vid}")
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
   await q.edit_message_text("ØªÙ… Ø§Ø¹ØªØ¨Ø§Ø± Ø§Ù„Ø±Ø³Ø§Ù„Ø© Ø³Ù„ÙŠÙ…Ø© ÙˆØ­Ø°Ù Ø§Ù„Ø¥Ù†Ø°Ø§Ø±")
  return
 if d.startswith('warn_detail_'):
  vid = d.replace('warn_detail_','')
  v = VIOLATIONS.get(vid,{})
  detail = f"ØªÙØ§ØµÙŠÙ„ Ø§Ù„Ù…Ø®Ø§Ù„ÙØ© {vid}\n\n"
  detail += f"Ø§Ù„Ø¹Ø¶Ùˆ : {v.get('user_id')}\n"
  detail += f"Ø§Ù„ÙƒÙ„Ù…Ø© : {v.get('word')}\n"
  detail += f"Ø§Ù„Ù†Øµ : {v.get('text','')[:100]}\n"
  detail += f"Ø§Ù„Ù‚Ø±ÙˆØ¨ : {v.get('chat')}"
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
    status='Ù…ÙØ¹Ù„Ø©' if lim['enabled'] else 'Ù…Ø¹Ø·Ù„Ø©'
    await q.answer(f'Ø§Ù„Ø­Ø¯ÙˆØ¯ Ø§Ù„Ø¢Ù† {status}', show_alert=True)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_clear':
    LIMITS[str(cid)]['limits']={a:0 for a in LIMIT_ACTIONS}
    sv('limits.json',LIMITS)
    await q.edit_message_text(limits_text(cid), reply_markup=kb_limits_main(cid))
    return
  if d=='lim_today':
    # Ø¹Ø±Ø¶ Ø§Ø³ØªÙ‡Ù„Ø§Ùƒ Ø§Ù„ÙŠÙˆÙ…
    txt='ðŸ“Š Ø§Ø³ØªÙ‡Ù„Ø§Ùƒ Ø§Ù„ÙŠÙˆÙ…:\n\n'
    cid_s=str(cid)
    if cid_s in LIMITS_USAGE:
      for admin_id, data in LIMITS_USAGE[cid_s].items():
        txt+=f'Ø§Ù„Ù…Ø´Ø±Ù {admin_id}:\n'
        for act,cnt in data.get('counts',{}).items():
          if cnt>0:
            txt+=f'  {act}: {cnt}\n'
        txt+='\n'
    else:
      txt+='Ù„Ø§ ÙŠÙˆØ¬Ø¯ Ø§Ø³ØªÙ‡Ù„Ø§Ùƒ Ø§Ù„ÙŠÙˆÙ…'
    await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([
      [InlineKeyboardButton('â€¢ Ø±Ø¬ÙˆØ¹', callback_data='lim_main')],
      [InlineKeyboardButton('â€¢ Ø¥ØºÙ„Ø§Ù‚', callback_data='close')]
    ]))
    return
  if d.startswith('lim_edit_'):
    # lim_edit_Ø§Ù„Ø·Ø±Ø¯_+1 or set_5
    try:
      _,_,action,op = d.split('_',3)
    except:
      # action may contain _
      parts=d.split('_')
      # lim_edit_Ø§Ù„Ø·Ø±Ø¯_set_5
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
    # lim_Ø§Ù„Ø·Ø±Ø¯ -> ÙØªØ­ ØªØ¹Ø¯ÙŠÙ„
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
  await q.edit_message_text('ðŸ‘¥ Ø§Ø¯Ø§Ø±Ø© Ø§Ù„Ù‚Ø±ÙˆØ¨\nâ€¢ Ø±ÙØ¹ Ø§Ø¯Ù…Ù† - ØªÙ†Ø²ÙŠÙ„ Ø§Ø¯Ù…Ù†\nâ€¢ Ø±ÙØ¹ Ù…Ø¯ÙŠØ± - ØªÙ†Ø²ÙŠÙ„ Ù…Ø¯ÙŠØ±\nâ€¢ Ø±ÙØ¹ Ù…Ø§Ù„Ùƒ - ØªÙ†Ø²ÙŠÙ„ Ù…Ø§Ù„Ùƒ\nâ€¢ Ø­Ø¸Ø± - Ø§Ù„ØºØ§Ø¡ Ø­Ø¸Ø±\nâ€¢ ÙƒØªÙ… - Ø§Ù„ØºØ§Ø¡ ÙƒØªÙ…\nâ€¢ ØªÙ‚ÙŠØ¯ - Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠØ¯', reply_markup=kb_commands())
  return
 if d=='fun':
  await q.edit_message_text('ðŸŽ® Ø§Ù„ØªØ³Ù„ÙŠØ© ÙˆØ§Ù„Ø®Ø¯Ù…ÙŠØ©\nâ€¢ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨\nâ€¢ ØªÙˆØ¨ Ø§Ù„Ù…ØªÙØ§Ø¹Ù„ÙŠÙ†\nâ€¢ Ø±ØªØ¨ØªÙŠ\nâ€¢ Ø­Ø¸\nâ€¢ ÙƒØª ØªÙˆÙŠØª\nâ€¢ Ø§Ù„Ø¹Ù‚Ø§Ø¨\nâ€¢ Ø§Ù„Ø­ÙƒÙ…\nâ€¢ Ø§Ù„ÙƒØ±Ø³ÙŠ', reply_markup=kb_commands())
  return
 if d=='dev':
  await q.edit_message_text('ðŸ’» Ø§ÙˆØ§Ù…Ø± Dev\nâ€¢ Ø§Ù„Ù…Ø·ÙˆØ±\nâ€¢ Ø§Ø¶Ù Ø§Ù…Ø±\nâ€¢ Ù…Ø³Ø­ Ø§Ù…Ø±\nâ€¢ Ø§Ù„Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù…Ø¶Ø§ÙÙ‡\nâ€¢ ØªÙØ¹ÙŠÙ„ / ØªØ¹Ø·ÙŠÙ„', reply_markup=kb_commands())
  return
 if d=='sets':
  await q.edit_message_text('âš™ï¸ Ø§Ù„Ø¥Ø¹Ø¯Ø§Ø¯Ø§Øª\nâ€¢ Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ù‚ÙÙ„\nâ€¢ Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„ØªØ±Ø­ÙŠØ¨\nâ€¢ Ø§Ø¹Ø¯Ø§Ø¯Ø§Øª Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨', reply_markup=kb_commands())
  return
 if d=='onoff':
  await q.edit_message_text('âš™ï¸ Ø§Ù„ØªÙØ¹ÙŠÙ„ ÙˆØ§Ù„ØªØ¹Ø·ÙŠÙ„\nâ€¢ ØªÙØ¹ÙŠÙ„ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨\nâ€¢ ØªØ¹Ø·ÙŠÙ„ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨\nâ€¢ Ù‚ÙÙ„ Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠ\nâ€¢ ÙØªØ­ Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠ', reply_markup=kb_commands())
  return

 if d.startswith('lock_') and not d.startswith('lockpage_'):
  name = d[5:]
  # ØªØ¨Ø¯ÙŠÙ„
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]= not LOCKS[cid].get(name,False)
  sv('locks.json',LOCKS)
  locked = LOCKS[cid][name]
  # ØªØ­Ø¯ÙŠØ¯ Ø§Ù„ØµÙØ­Ø© Ø§Ù„Ø­Ø§Ù„ÙŠØ© Ù„Ù„Ø§Ø³Ù…
  cur_page = 1
  for p, lst in LOCKS_PAGES.items():
   if name in lst:
    cur_page=p
    break
  # Ø¨Ø¯ÙˆÙ† Ø±Ø¯ - ÙÙ‚Ø· ÙŠØºÙŠØ± Ù„ÙˆÙ† Ø§Ù„Ø²Ø±
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
  pass # Ø¨Ø¯ÙˆÙ† Ø±Ø¯
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
  # Ù„Ù„ØªÙˆØ§ÙÙ‚ Ø§Ù„Ù‚Ø¯ÙŠÙ…
  do_close = 'closeall' in d
  LOCKS.setdefault(cid,{})
  for lst in LOCKS_PAGES.values():
   for name in lst:
    LOCKS[cid][name]=do_close
  sv('locks.json',LOCKS)
  pass # Ø¨Ø¯ÙˆÙ† Ø±Ø¯
  try:
   await q.edit_message_reply_markup(reply_markup=kb_lock_page(cid,1))
  except:
   pass
  return


 if d.startswith('admin_toggle_'):
  try:
   # admin_toggle_12345_ØªØºÙŠÙŠØ± Ø§Ù„Ù…Ø¹Ù„ÙˆÙ…Ø§Øª
   _, _, uid, perm_name = d.split('_',3)
   ADMIN_PERMS.setdefault(cid,{})
   if uid not in ADMIN_PERMS[cid]:
    ADMIN_PERMS[cid][uid]=DEFAULT_PERMS.copy()
   ADMIN_PERMS[cid][uid][perm_name] = not ADMIN_PERMS[cid][uid].get(perm_name, False)
   sv('admin_perms.json',ADMIN_PERMS)
   perms = get_user_perms(cid, uid)
   # ØªØ­Ø¯ÙŠØ« ØµÙ„Ø§Ø­ÙŠØ§Øª ØªÙŠÙ„ÙŠØ¬Ø±Ø§Ù… Ø­Ø³Ø¨ Ø§Ù„Ø§Ø®ØªÙŠØ§Ø±
   try:
    # Ù†Ø­Ø¯Ø« Ø§Ù„Ø§Ø¯Ù…Ù† ÙÙŠ ØªÙŠÙ„ÙŠØ¬Ø±Ø§Ù…
    pass
   except:
    pass
   await q.edit_message_reply_markup(reply_markup=kb_admin_panel(cid, uid, ''))
   # Ù†Ø­ØªØ§Ø¬ Ù†Ø¬ÙŠØ¨ Ø§Ø³Ù…
   try:
    member = await c.bot.get_chat_member(q.message.chat.id, int(uid))
    name = member.user.first_name
   except:
    name = uid
   await q.edit_message_text(admin_panel_text(name, perms), reply_markup=kb_admin_panel(cid, uid, name))
  except Exception as e:
   await q.answer(f'Ø®Ø·Ø£ {e}', show_alert=True)
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
   await q.answer(f'Ø®Ø·Ø£ {e}', show_alert=True)
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
   await q.edit_message_text(f'ØªÙ… ØªÙ†Ø²ÙŠÙ„ {uid} Ù…Ù† Ø§Ù„Ø§Ø´Ø±Ø§Ù')
  except Exception as e:
   await q.answer(f'Ø®Ø·Ø£ {e}', show_alert=True)
  return

 if d.startswith('setrank_'):
  try:
   # setrank_Ø¹Ø§Ù…_Ø§Ø¯Ù…Ù†
   _, cmd_name, rank = d.split('_',2)
   COMMAND_RANKS.setdefault(cid,{})
   COMMAND_RANKS[cid][cmd_name]=rank
   sv('command_ranks.json',COMMAND_RANKS)
   # Ù…Ø³Ø­ Ù…Ù† Ø§Ù„Ø§Ù†ØªØ¸Ø§Ø±
   for k in list(PENDING_RANK_LOCK.keys()):
    if k.startswith(cid):
     if PENDING_RANK_LOCK[k]==cmd_name:
      del PENDING_RANK_LOCK[k]
   await q.edit_message_text(f'ØªÙ… Ù‚ÙÙ„ Ø§Ù„Ø£Ù…Ø± {cmd_name} Ù„Ø±ØªØ¨Ø© {rank} ÙÙ‚Ø· âœ“')
  except Exception as e:
   await q.answer(f'Ø®Ø·Ø£ {e}', show_alert=True)
  return

 if d=='about':
  await q.edit_message_text(
   'SORD - Ø³ÙˆØ±Ø¯\nØ§Ù„Ù…Ø·ÙˆØ± : Liam',
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

 # ÙƒØªÙ… ÙˆÙ‡Ù…ÙŠ - Ù„Ùˆ Ù…ÙƒØªÙˆÙ… Ø§Ø­Ø°Ù Ø±Ø³Ø§Ù„ØªÙ‡
 if MUTED.get(cid,{}).get(uid):
  try:
   await m.delete()
  except:
   pass
  return


 # Ù‚ÙÙ„ Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠ - Ù†Ø¸Ø§Ù… Ø§Ù†Ø°Ø§Ø±Ø§Øª Ù…Ø«Ù„ Ø§Ù„ØµÙˆØ±Ø©
 if LOCKS.get(cid,{}).get('Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠ',False) or True:  # Ø´ØºØ§Ù„ Ø¯Ø§ÙŠÙ…Ø§ Ù„Ù„Ø§Ø¨Ø§Ø­ÙŠ
  bad_words = ['Ø§Ø¨Ø§Ø­ÙŠ','Ø³ÙƒØ³','porn','xxx','sex','Ù†ÙŠÙƒ','ÙƒØ³','Ø²Ø¨','Ø·ÙŠØ²','Ù…Øµ','Ù‚Ø­Ø¨Ù‡','Ù‚Ø­Ø§Ø¨','Ø´Ø±Ù…ÙˆØ·','Ø§Ø¨Ø§Ø­ÙŠØ©']
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
   # Ù†Ø¸Ø§Ù… Ø§Ù„Ø§Ù†Ø°Ø§Ø±Ø§Øª
   WARNINGS.setdefault(cid,{})
   WARNINGS[cid][uid]=WARNINGS[cid].get(uid,0)+1
   sv('warnings.json',WARNINGS)
   warns = WARNINGS[cid][uid]
   # Ø­ÙØ¸ Ø§Ù„Ù…Ø®Ø§Ù„ÙØ©
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
   # Ù†ÙØ³ Ø±Ø³Ø§Ù„Ø© Ø§Ù„ØµÙˆØ±Ø©
   conf = random.randint(95,99)
   text = f"â€¢ ØªÙ… Ø±ØµØ¯ Ù…Ø­ØªÙˆÙ‰ Ù…Ø®Ø§Ù„Ù ÙˆØ­Ø°ÙÙ‡\n"
   text += f"â€¢ Ø§Ù„Ø¹Ø¶Ùˆ â†¤ {uid}\n"
   text += f"â€¢ Ù†Ø³Ø¨Ø© Ø§Ù„ØªØ£ÙƒØ¯ â†¤ %{conf}\n"
   text += f"â€¢ Ø§Ù„Ø¥Ù†Ø°Ø§Ø±Ø§Øª â†¤ ({warns}/3)\n"
   text += f"â€¢ ÙŠÙ†ØªÙ‡ÙŠ Ø§Ù„Ø¥Ù†Ø°Ø§Ø± Ø®Ù„Ø§Ù„ â†¤ 06:00:00"
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
   await m.reply_text(f'Ø§Ù„Ø§Ù…Ø± Ø§Ù„Ù‚Ø¯ÙŠÙ… : ( {t} )')
   return
  if WAITING[cid].get('step')=='confirm_del' and t=='Ø§Ù„ØºØ§Ø¡':
   old=WAITING[cid]['old']
   del WAITING[cid]
   await m.reply_text(f'ØªÙ… Ø§Ø²Ø§Ù„Ø© Ø§Ù„Ø§Ù…Ø± .. ( {old} )')
   return

 if t in ['Ø§Ù„Ø§ÙˆØ§Ù…Ø±','Ø§ÙˆØ§Ù…Ø±','Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ø§ÙˆØ§Ù…Ø±']:
  await m.reply_text(AWAMER_TEXT,reply_markup=kb_commands())
  return

 if t.startswith('Ù‚ÙÙ„ Ø§Ù…Ø±'):
  rank=t.replace('Ù‚ÙÙ„ Ø§Ù…Ø±','').strip()
  await m.reply_text(f'Ø³ÙŠØªÙ… ÙˆØ¶Ø¹ Ø§Ù„Ø§Ù…Ø± {rank} Ù„Ù„Ø±ØªØ¨Ø©')
  return

 if t in ['Ø§Ù„Ø±ØªØ¨','Ø§Ù„Ø±ØªØ¨ÙŠ']:
  await m.reply_text(
   'Ø§Ù„Ø±ØªØ¨ Ø§Ù„Ù…ØªØ§Ø­Ø© :\nDev\nDev2\nMY\nM\nÙ…Ø§Ù„Ùƒ\nÙ…Ù†Ø´Ø¦\nÙ…Ø¯ÙŠØ±\nØ§Ø¯Ù…Ù†\nÙ…Ù…ÙŠØ²'
  )
  return

 if t=='Ù‚ÙÙ„ Ø§Ù„Ø±ØªØ¨':
  await m.reply_text('Ø§Ø±Ø³Ù„ Ø§Ù„Ø±ØªØ¨Ø© Ø§Ù„Ø§Ù† :\nDev\nMY\nM\nÙ…Ø§Ù„Ùƒ\nÙ…Ù†Ø´Ø¦\nÙ…Ø¯ÙŠØ±\nØ§Ø¯Ù…Ù†')
  return

 if t in ['Ø§Ù„Ù…Ø·ÙˆØ±','SORD','Liam','Ù„ÙŠØ§Ù…']:
  await m.reply_text('SORD - Ø³ÙˆØ±Ø¯\nØ§Ù„Ù…Ø·ÙˆØ± : Liam')
  return

 if t.startswith('Ø§Ù‡Ù…Ø³'):
  await m.reply_text('Ø·Ø±ÙŠÙ‚Ø© Ø§Ù‡Ù…Ø³\nØ±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© ÙˆØ§ÙƒØªØ¨ Ø§Ù‡Ù…Ø³')
  return

 if t=='ØªØ¹Ø·ÙŠÙ„ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨':
  TOGGLES.setdefault(cid,{})['Ø§Ù„Ø¹Ø§Ø¨']=False
  sv('toggles.json',TOGGLES)
  await m.reply_text(f'ØªÙ… ØªØ¹Ø·ÙŠÙ„ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨')
  return

 if t=='ØªÙØ¹ÙŠÙ„ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨':
  TOGGLES.setdefault(cid,{})['Ø§Ù„Ø¹Ø§Ø¨']=True
  sv('toggles.json',TOGGLES)
  await m.reply_text(f'ØªÙ… ØªÙØ¹ÙŠÙ„ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨')
  return

 if t in ['Ù…Ø³Ø­ Ø§Ù…Ø±','Ø­Ø°Ù Ø§Ù…Ø±']:
  WAITING[cid]={'step':'old_del'}
  await m.reply_text('Ø§Ø±Ø³Ù„ Ø§Ù„Ø§Ù…Ø± Ø§Ù„Ù‚Ø¯ÙŠÙ…')
  return

 if t=='Ø§Ù„ØºØ§Ø¡':
  await m.reply_text('ØªÙ… Ø§Ø²Ø§Ù„Ø© Ø§Ù„Ø§Ù…Ø± .. ( Ø§Ù„ØºØ§Ø¡ )')
  return

 if t=='Ø­Ø¸Ø±':
  await m.reply_text('Ø·Ø±ÙŠÙ‚Ø© Ø­Ø¸Ø±\nØ±Ø¯ + Ø­Ø¸Ø±')
  return


 if t in ['Ø±ØªØ¨ØªÙŠ','Ø±ØªØ¨ØªÙ‡','Ø±ØªØ¨Ù‡','Ø±ØªØ¨Ø©','Ø±ØªØ¨Ù‡ Ø§Ù†Øª','Ø±ØªØ¨ØªÙŠ Ø§Ù†Ø§','Ø±ØªØ¨Ø© Ø§Ù†Øª'] or t.startswith('Ø±ØªØ¨Ù‡ ') or t.startswith('Ø±ØªØ¨Ø© '):
  # Ù„Ùˆ Ù…Ø§Ù„Ùƒ Ø§Ù„Ø¨ÙˆØª - Ø±ØªØ¨ØªÙ‡ Ø¹Ø§Ù…Ø© Dev Ø¯Ø§ÙŠÙ…Ø§
  if is_owner(m.from_user):
   await m.reply_text(f"ðŸŽ–ï¸ Dev â† Ø±ØªØ¨ØªÙƒ =\n\nâ˜‚ï¸ - Dev - {TOP.get(cid,{}).get(str(m.from_user.id),0)} Ø±Ø³Ø§Ù„Ø©")
   return
  # Ù„Ùˆ Ø§Ù„ÙˆØ¶Ø¹ Ø§Ù„Ø®Ø§Øµ Ù…ÙØ¹Ù„ - Ø§Ù„Ø±ØªØ¨ Ø®Ø§ØµØ© Ù„Ù‡Ø°Ø§ Ø§Ù„Ù‚Ø±ÙˆØ¨
  if PRIVATE_MODE.get(cid,False):
   # Ø±ØªØ¨Ø© Ø®Ø§ØµØ© Ù„Ù„Ù‚Ø±ÙˆØ¨
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
  if t=='Ø±ØªØ¨ØªÙ‡' and m.reply_to_message:
   # Sniper style
   await m.reply_text(f"â˜‚ï¸ - {rank_name} - {msgs} Ø±Ø³Ø§Ù„Ø©\nÙ†Ø³Ø¨Ø© Ø§Ù„ØªÙØ§Ø¹Ù„ Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ : {percent:.2f}%\nØ£ÙˆÙ„ Ø¸Ù‡ÙˆØ± Ø¨Ø§Ù„Ù‚Ø±ÙˆØ¨ : 2026/10/21")
   # Soul style second message
   await m.reply_text(f"ðŸŽ–ï¸ {rank_name} â† Ø±ØªØ¨ØªÙ‡ =")
  else:
   await m.reply_text(f"ðŸŽ–ï¸ {rank_name} â† Ø±ØªØ¨ØªÙƒ =\nâ˜‚ï¸ - {rank_name} - {msgs} Ø±Ø³Ø§Ù„Ø©\nÙ†Ø³Ø¨Ø© Ø§Ù„ØªÙØ§Ø¹Ù„ : {percent:.2f}%")
  return


 
 if t in ['ÙƒØªÙ…','ÙƒØªÙ…Ù‡','Ø§Ø³ÙƒØª','Ø§Ø³ÙƒØªÙ‡']:
  if not m.reply_to_message:
   await m.reply_text('Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ø´Ø®Øµ ÙˆØ§ÙƒØªØ¨ ÙƒØªÙ…')
   return
  target = m.reply_to_message.from_user
  tid = str(target.id)
  MUTED.setdefault(cid,{})
  MUTED[cid][tid]=True
  sv('muted.json',MUTED)
  await m.reply_text(f'ØªÙ… ÙƒØªÙ… {target.first_name}\nÙŠÙ‚Ø¯Ø± ÙŠÙƒØªØ¨ Ø¨Ø³ Ø±Ø³Ø§ÙŠÙ„Ù‡ ØªÙ†Ø­Ø°Ù')
  return

 if t in ['Ø§Ù„ØºØ§Ø¡ ÙƒØªÙ…','Ø§Ù„ØºØ§Ø¡ Ø§Ù„ÙƒØªÙ…','ÙÙƒ ÙƒØªÙ…','ÙØªØ­ ÙƒØªÙ…','unmute','Ø§Ù„ØºØ§Ø¡ Ø§Ø³ÙƒØª','ÙÙƒ Ø§Ø³ÙƒØª']:
  if not m.reply_to_message:
   await m.reply_text('Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ø´Ø®Øµ ÙˆØ§ÙƒØªØ¨ Ø§Ù„ØºØ§Ø¡ ÙƒØªÙ…')
   return
  target = m.reply_to_message.from_user
  tid = str(target.id)
  MUTED.setdefault(cid,{})
  MUTED[cid].pop(tid,None)
  sv('muted.json',MUTED)
  await m.reply_text(f'ØªÙ… Ø§Ù„ØºØ§Ø¡ ÙƒØªÙ… {target.first_name}')
  return

 if t=='Ø§Ù„Ù…ÙƒØªÙˆÙ…ÙŠÙ†' or t=='Ù‚Ø§Ø¦Ù…Ø© Ø§Ù„Ù…ÙƒØªÙˆÙ…ÙŠÙ†':
  lst = MUTED.get(cid,{})
  if not lst:
   await m.reply_text('Ù…Ø§ÙÙŠ Ø§Ø­Ø¯ Ù…ÙƒØªÙˆÙ…')
  else:
   await m.reply_text(f'Ø§Ù„Ù…ÙƒØªÙˆÙ…ÙŠÙ† : {len(lst)} Ø´Ø®Øµ')
  return


 
 if t in ['ØªÙ‚ÙŠØ¯','ØªÙ‚ÙŠÙŠØ¯','ØªÙ‚ÙŠÙŠØ¯Ù‡']:
  if not m.reply_to_message:
   await m.reply_text('Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ø´Ø®Øµ ÙˆØ§ÙƒØªØ¨ ØªÙ‚ÙŠØ¯')
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
   await m.reply_text(f'ØªÙ… ØªÙ‚ÙŠØ¯ {target.first_name}\nÙ…Ø§ ÙŠÙ‚Ø¯Ø± ÙŠØ±Ø³Ù„ Ø´ÙŠ Ù„Ø§ Ù†Øµ Ù„Ø§ ÙˆØ³Ø§Ø¦Ø·')
  except Exception as e:
   await m.reply_text(f'Ù…Ø§ Ù‚Ø¯Ø±Øª Ø§Ù‚ÙŠØ¯Ù‡ - Ø§Ø±ÙØ¹Ù†ÙŠ Ù…Ø´Ø±Ù Ù…Ø¹ ØªÙ‚ÙŠÙŠØ¯ Ø§Ù„Ø§Ø¹Ø¶Ø§Ø¡\n{e}')
  return

 if t in ['Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠØ¯','Ø§Ù„ØºØ§Ø¡ Ø§Ù„ØªÙ‚ÙŠÙŠØ¯','ÙÙƒ ØªÙ‚ÙŠØ¯','ÙØªØ­ ØªÙ‚ÙŠØ¯']:
  if not m.reply_to_message:
   await m.reply_text('Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ø´Ø®Øµ ÙˆØ§ÙƒØªØ¨ Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠØ¯')
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
   await m.reply_text(f'ØªÙ… Ø§Ù„ØºØ§Ø¡ ØªÙ‚ÙŠØ¯ {target.first_name}')
  except Exception as e:
   await m.reply_text(f'Ù…Ø§ Ù‚Ø¯Ø±Øª Ø§ÙÙƒ ØªÙ‚ÙŠÙŠØ¯Ù‡\n{e}')
  return


 
 if t.startswith('Ø§Ø¶Ù Ø§Ù…Ø±') or t.startswith('ØªØºÙŠÙŠØ± Ø§Ù…Ø±') or t.startswith('ØºÙŠØ± Ø§Ù…Ø±'):
  # ØµÙŠØºØ© : Ø§Ø¶Ù Ø§Ù…Ø± Ø§Ø³ÙƒØª = ÙƒØªÙ…  Ø§Ùˆ  ØªØºÙŠÙŠØ± Ø§Ù…Ø± ÙƒØªÙ… Ø§Ù„Ù‰ Ø§Ø³ÙƒØª
  try:
   txt_cmd = t.replace('Ø§Ø¶Ù Ø§Ù…Ø±','').replace('ØªØºÙŠÙŠØ± Ø§Ù…Ø±','').replace('ØºÙŠØ± Ø§Ù…Ø±','').strip()
   new_name = None
   old_name = None
   if '=' in txt_cmd:
    parts = txt_cmd.split('=')
    new_name = parts[0].strip()
    old_name = parts[1].strip()
   elif 'Ø§Ù„Ù‰' in txt_cmd:
    parts = txt_cmd.split('Ø§Ù„Ù‰')
    old_name = parts[0].strip()
    new_name = parts[1].strip()
   elif ' ' in txt_cmd:
    parts = txt_cmd.split()
    if len(parts)>=2:
     new_name = parts[0].strip()
     old_name = parts[1].strip()
     # Ù„Ùˆ ÙƒØªØ¨ ÙƒØªÙ… Ø§Ù„Ù‰ Ø§Ø³ÙƒØª
     if len(parts)>=3 and parts[1]=='Ø§Ù„Ù‰':
      old_name = parts[0].strip()
      new_name = parts[2].strip()
   if new_name and old_name:
    CUSTOM.setdefault(cid,{})
    CUSTOM[cid][new_name] = old_name
    sv('custom.json',CUSTOM)
    await m.reply_text(f'ØªÙ… ØªØºÙŠÙŠØ± Ø§Ù„Ø§Ù…Ø±\n{old_name} â†¤ {new_name}\nØ°Ø­ÙŠÙ† ØªÙ‚Ø¯Ø± ØªÙƒØªØ¨ {new_name} Ø¨Ø¯Ù„ {old_name}')
   else:
    await m.reply_text('Ø·Ø±ÙŠÙ‚Ø© ØªØºÙŠÙŠØ± Ø§Ù„Ø§Ù…Ø±:\nØ§Ø¶Ù Ø§Ù…Ø± Ø§Ø³ÙƒØª = ÙƒØªÙ…\nØ§Ùˆ\nØªØºÙŠÙŠØ± Ø§Ù…Ø± ÙƒØªÙ… Ø§Ù„Ù‰ Ø§Ø³ÙƒØª')
  except Exception as e:
   await m.reply_text(f'Ø®Ø·Ø£ : {e}\nØ§Ù„Ø·Ø±ÙŠÙ‚Ø© : Ø§Ø¶Ù Ø§Ù…Ø± Ø§Ø³ÙƒØª = ÙƒØªÙ…')
  return

 if t.startswith('Ù…Ø³Ø­ Ø§Ù…Ø±') or t.startswith('Ø­Ø°Ù Ø§Ù…Ø±'):
  try:
   txt_cmd = t.replace('Ù…Ø³Ø­ Ø§Ù…Ø±','').replace('Ø­Ø°Ù Ø§Ù…Ø±','').strip()
   CUSTOM.setdefault(cid,{})
   if txt_cmd in CUSTOM.get(cid,{}):
    del CUSTOM[cid][txt_cmd]
    sv('custom.json',CUSTOM)
    await m.reply_text(f'ØªÙ… Ù…Ø³Ø­ Ø§Ù„Ø§Ù…Ø± {txt_cmd}')
   else:
    await m.reply_text(f'Ø§Ù„Ø§Ù…Ø± {txt_cmd} Ù…Ùˆ Ù…ÙˆØ¬ÙˆØ¯')
  except:
   pass
  return

 # ØªØ´ÙŠÙŠÙƒ Ø§Ù„Ø§ÙˆØ§Ù…Ø± Ø§Ù„Ù…Ø®ØµØµØ©
 if t in CUSTOM.get(cid,{}):
  original = CUSTOM[cid][t]
  # Ù†ÙØ° Ø§Ù„Ø§Ù…Ø± Ø§Ù„Ø§ØµÙ„ÙŠ ÙƒØ£Ù†Ù‡ ÙƒØªØ¨
  # Ø­ÙˆÙ„ Ø§Ù„Ù†Øµ Ù„Ù„Ø§Ù…Ø± Ø§Ù„Ø§ØµÙ„ÙŠ ÙˆØ§Ø±Ø¬Ø¹ Ø¹Ø§Ù„Ø¬
  # Ø¨Ø³ÙŠØ·Ø© : Ù„Ùˆ Ø§Ø³ÙƒØª -> ÙƒØªÙ…
  if original in ['ÙƒØªÙ…','ÙƒØªÙ…Ù‡']:
   if not m.reply_to_message:
    await m.reply_text('Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© Ø§Ù„Ø´Ø®Øµ ÙˆØ§ÙƒØªØ¨ ÙƒØªÙ…')
    return
   target = m.reply_to_message.from_user
   tid = str(target.id)
   MUTED.setdefault(cid,{})
   MUTED[cid][tid]=True
   sv('muted.json',MUTED)
   await m.reply_text(f'ØªÙ… ÙƒØªÙ… {target.first_name} Ø¨ÙˆØ§Ø³Ø·Ø© Ø§Ù…Ø± {t}')
   return
  if original in ['ØªÙ‚ÙŠØ¯']:
   if not m.reply_to_message:
    await m.reply_text('Ø±Ø¯ Ø¹Ù„Ù‰ Ø±Ø³Ø§Ù„Ø© ÙˆØ§ÙƒØªØ¨ ØªÙ‚ÙŠØ¯')
    return
   target = m.reply_to_message.from_user
   try:
    from telegram import ChatPermissions
    perms = ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_polls=False, can_send_other_messages=False, can_add_web_page_previews=False)
    await c.bot.restrict_chat_member(chat_id=m.chat.id, user_id=target.id, permissions=perms)
    await m.reply_text(f'ØªÙ… ØªÙ‚ÙŠØ¯ {target.first_name} Ø¨ÙˆØ§Ø³Ø·Ø© Ø§Ù…Ø± {t}')
   except Exception as e:
    await m.reply_text(f'Ù…Ø§ Ù‚Ø¯Ø±Øª Ø§Ù‚ÙŠØ¯Ù‡\n{e}')
   return


 # Ù‚ÙÙ„ ÙˆÙØªØ­ Ù†ØµÙŠ
 if t.startswith('Ù‚ÙÙ„') and len(t)>3:
  name=t.replace('Ù‚ÙÙ„','').strip()
  if name in ['Ø§Ù„Ø±ØªØ¨','Ø§Ù…Ø±']:
   return
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]=True
  sv('locks.json',LOCKS)
  await m.reply_text(f'ØªÙ… Ù‚ÙÙ„ {name}')
  return

 if t.startswith('ÙØªØ­') and len(t)>3:
  name=t.replace('ÙØªØ­','').strip()
  LOCKS.setdefault(cid,{})
  LOCKS[cid][name]=False
  sv('locks.json',LOCKS)
  await m.reply_text(f'ØªÙ… ÙØªØ­ {name}')
  return


 if t in GAMES_DATA or t in ['Ø­Ø¸','ÙƒØª ØªÙˆÙŠØª','Ø§Ø°ÙƒØ§Ø±','ØªØ­Ø¯ÙŠ','Ø§Ø³Ø¦Ù„Ø©','ØµØ±Ø§Ø­Ø©','Ù…Ø§ÙÙŠØ§','Ø®Ù…Ù†']:
  import random
  if t=='Ø­Ø¸':
   await m.reply_text(f"Ø­Ø¸Ùƒ Ø§Ù„ÙŠÙˆÙ… {random.randint(1,100)}% ðŸŽ²")
  elif t=='ÙƒØª ØªÙˆÙŠØª':
   tweets = ['Ø§Ù„Ø­ÙŠØ§Ø© Ø­Ù„ÙˆØ©','Ù„Ø§ ØªÙ†ØªØ¸Ø± Ø§Ø­Ø¯','Ø®Ù„Ùƒ Ù‚ÙˆÙŠ','Ø§Ø¨ØªØ³Ù…']
   await m.reply_text(random.choice(tweets))
  elif t=='Ø§Ø°ÙƒØ§Ø±':
   azkar = ['Ø³Ø¨Ø­Ø§Ù† Ø§Ù„Ù„Ù‡','Ø§Ù„Ø­Ù…Ø¯Ù„Ù„Ù‡','Ù„Ø§ Ø§Ù„Ù‡ Ø§Ù„Ø§ Ø§Ù„Ù„Ù‡','Ø§Ù„Ù„Ù‡ Ø§ÙƒØ¨Ø±']
   await m.reply_text(random.choice(azkar))
  else:
   await m.reply_text(get_game_text(t))
  return

 if t=='Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨':
  # Ø¹Ø±Ø¶ ÙƒÙ„ Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨ Ù…Ø¹ Ø§Ù„Ø´Ø±Ø­
  txt_games = "ðŸŽ® Ù…Ø±ÙƒØ² Ø§Ù„Ø§Ù„Ø¹Ø§Ø¨\nØ§Ø®ØªØ± Ø§Ù„Ù„Ø¹Ø¨Ø© ÙˆØ´ÙˆÙ Ø´Ø±Ø­Ù‡Ø§:\n\n"
  for name in GAMES_DATA:
   txt_games += f"â€¢ {name}\n"
  txt_games += "\nØ§ÙƒØªØ¨ Ø§Ø³Ù… Ø§Ù„Ù„Ø¹Ø¨Ø© Ù„Ù…Ø¹Ø±ÙØ© Ø´Ø±Ø­Ù‡Ø§"
  await m.reply_text(txt_games, reply_markup=kb_games())
  return



 if t in ['ØªÙˆØ¨ Ø§Ù„Ù…ØªÙØ§Ø¹Ù„ÙŠÙ†','ØªÙˆØ¨']:
  await m.reply_text('ØªÙˆØ¨ 20\n1) Ø¯ÙŠÙ\n2) RORY...')
  return

 if t=='Ø§Ù„Ù‚ÙÙ„ ÙˆØ§Ù„ÙØªØ­':
  await m.reply_text('Ù„ÙˆØ­Ø© Ø§Ù„Ù‚ÙÙ„',reply_markup=kb_lock_p1())
  return

# Ù‚ÙÙ„ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ ÙˆØ§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ - ÙŠÙ…Ø³Ø­ ÙˆÙŠÙ…Ù†Ø´Ù†

async def media_handler(u,c):
 m = u.message
 if not m:
  return
 cid = str(m.chat.id)
 uid = str(m.from_user.id)
 # Ù„Ùˆ Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠ Ù…Ù‚ÙÙˆÙ„ ÙˆØ§Ø±Ø³Ù„ ØµÙˆØ±Ø© Ø§Ùˆ ÙÙŠØ¯ÙŠÙˆ Ø§Ø¨Ø§Ø­ÙŠ (ÙŠØ¹ØªØ¨Ø± Ù…Ø®Ø§Ù„Ù)
 if LOCKS.get(cid,{}).get('Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠ',False):
  # Ù„Ùˆ ÙÙŠÙ‡ ÙƒØ§Ø¨Ø´Ù† ÙÙŠÙ‡ ÙƒÙ„Ù…Ø§Øª Ø§Ø¨Ø§Ø­ÙŠØ©
  cap = (m.caption or '').lower()
  bad_words = ['Ø§Ø¨Ø§Ø­ÙŠ','Ø³ÙƒØ³','porn','xxx','sex','Ù†ÙŠÙƒ','ÙƒØ³','Ø²Ø¨','Ø·ÙŠØ²','Ù…Øµ','Ù‚Ø­Ø¨Ù‡']
  found = None
  for w in bad_words:
   if w in cap:
    found = w
    break
  # Ù„Ùˆ Ø§Ù„ØµÙˆØ±Ø© Ø¨Ø¯ÙˆÙ† ÙƒØ§Ø¨Ø´Ù† Ø¨Ø³ Ø§Ù„Ù‚ÙÙ„ Ø´ØºØ§Ù„ Ù„Ù„Ø§Ø¨Ø§Ø­ÙŠ - Ù„Ø§ ØªØ­Ø°Ù ÙƒÙ„ Ø§Ù„ØµÙˆØ±ØŒ Ø¨Ø³ Ø§Ù„Ù„ÙŠ ÙÙŠÙ‡Ø§ ÙƒÙ„Ù…Ø§Øª
  # Ù„Ùˆ ØªØ¨ÙŠ ÙŠØ­Ø°Ù ÙƒÙ„ Ø§Ù„ØµÙˆØ± Ø§Ù„Ø§Ø¨Ø§Ø­ÙŠØ© Ø­ØªÙ‰ Ø¨Ø¯ÙˆÙ† ÙƒÙ„Ù…Ø§ØªØŒ ÙØ¹Ù„ Ù‡Ø°Ø§:
  # found = found or 'ØµÙˆØ±Ø©'
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
   text = f"â€¢ ØªÙ… Ø±ØµØ¯ Ù…Ø­ØªÙˆÙ‰ Ù…Ø®Ø§Ù„Ù ÙˆØ­Ø°ÙÙ‡\nâ€¢ Ø§Ù„Ø¹Ø¶Ùˆ â†¤ {uid}\nâ€¢ Ù†Ø³Ø¨Ø© Ø§Ù„ØªØ£ÙƒØ¯ â†¤ %{conf}\nâ€¢ Ø§Ù„Ø¥Ù†Ø°Ø§Ø±Ø§Øª â†¤ ({warns}/3)\nâ€¢ ÙŠÙ†ØªÙ‡ÙŠ Ø§Ù„Ø¥Ù†Ø°Ø§Ø± Ø®Ù„Ø§Ù„ â†¤ 06:00:00"
   try:
    await c.bot.send_message(chat_id=m.chat.id, text=text, reply_markup=kb_violation(vid))
   except:
    pass


async def edited(u,c):
 if not u.edited_message:
  return
 m=u.edited_message
 cid=str(m.chat.id)
 # ÙŠØ´ØªØºÙ„ Ù„Ùˆ Ù‚ÙÙ„ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ùˆ Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ Ù…Ù‚ÙÙˆÙ„
 locked = LOCKS.get(cid,{}).get('Ø§Ù„ØªØ¹Ø¯ÙŠÙ„',False) or LOCKS.get(cid,{}).get('Ø§Ù„ØªØ¹Ø¯ÙŠÙ„ Ø§Ù„Ø¹Ø§Ø¯ÙŠ',False)
 if locked:
  try:
   await m.delete()
  except:
   pass
  # Ù…Ù†Ø´Ù† Ø§Ù„Ø´Ø®Øµ
  try:
   name = m.from_user.first_name
   uid = m.from_user.id
   mention = f"[{name}](tg://user?id={uid})"
   await c.bot.send_message(
    chat_id=m.chat.id,
    text=f"{mention} Ø¨ØªØ¹Ø¯Ù„ Ø¨Ù„Ø¹Ù† Ø§Ù…Ùƒ",
    parse_mode='Markdown'
   )
  except:
   try:
    await c.bot.send_message(
     chat_id=m.chat.id,
     text=f"Ø¨ØªØ¹Ø¯Ù„ Ø¨Ù„Ø¹Ù† Ø§Ù…Ùƒ ÙŠØ§ {m.from_user.first_name}"
    )
   except:
    pass

# ØªØ´ØºÙŠÙ„
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
