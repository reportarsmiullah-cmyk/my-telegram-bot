from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember, LabeledPrice
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                           CallbackQueryHandler, PreCheckoutQueryHandler, filters, ContextTypes)
import logging
from datetime import datetime, timedelta
import random

# ================================================
# د BratiSmartBot Token — دلته ستا Token واچوه
# ================================================
TOKEN    = "8848428754:AAGTH8CArF-0MnR78z9Sr_pXFd3Y450mvTk"
ADMIN_ID = 8609291779
EXTRA_ADMINS = {}  # {uid: {"name":..., "perms": set()}}

REQUIRED_CHANNELS = [
    "@RareHackers_Official",
    "@samiullaHacker",
    "@AfghanRefaqat",
    "@kanalsazrobot",
    "@jhnxjozicjkck",
    "@afghan_chat_zone",
]
CHANNEL_LOCK = True

logging.basicConfig(level=logging.INFO)
users   = {}
banned  = set()
reports = {}
CONNECT_COST = 5

STARS_PACKAGES = {
    "s30":  {"stars": 30,  "coins": 30,  "label": "30 ⭐ = 30 💰"},
    "s100": {"stars": 100, "coins": 120, "label": "100 ⭐ = 120 💰"},
    "s250": {"stars": 250, "coins": 320, "label": "250 ⭐ = 320 💰"},
    "s500": {"stars": 500, "coins": 700, "label": "500 ⭐ = 700 💰"},
}

PROVINCES = {
    "af": ["کابل","هرات","کندهار","بلخ","ننګرهار","کندز","غزني","بغلان",
           "بدخشان","تخار","پکتیا","پکتیکا","خوست","لوګر","وردګ","پروان",
           "کاپیسا","پنجشیر","بامیان","دایکندي","غور","بادغیس","فراه",
           "نیمروز","هلمند","ارزګان","زابل","سمنګان","سرپل","جوزجان",
           "فاریاب","نورستان","کنړ","لغمان"],
    "ir": ["تهران","اصفهان","مشهد","شیراز","تبریز","اهواز","کرمانشاه",
           "ارومیه","رشت","زاهدان","همدان","کرمان","اراک","یزد","قم",
           "قزوین","سنندج","بندرعباس","گرگان","ساری","بیرجند","ایلام",
           "بجنورد","شهرکرد","یاسوج","خرم‌آباد","زنجان","اردبیل","بوشهر","گیلان"],
    "us": ["New York","Los Angeles","Chicago","Houston","Phoenix",
           "Philadelphia","San Antonio","San Diego","Dallas","San Jose",
           "Austin","Jacksonville","Fort Worth","Columbus","Charlotte",
           "Indianapolis","Seattle","Denver","Washington DC","Nashville",
           "Oklahoma City","El Paso","Boston","Portland","Las Vegas",
           "Memphis","Louisville","Baltimore","Milwaukee","Albuquerque"],
}

BAD_WORDS = ["کص","کیر","کونی","جنده","fuck","sex","porn","خر","سپي","بي ناموسه"]

ALL_PERMS = {"broadcast","find_user","give_coins","remove_coins","ban",
             "unban","warn","msg_user","user_list","active_chats",
             "ratings","channel_lock","reports"}

WELCOME_STICKER = "CAACAgIAAxkBAAIBmWV0xxxxxxxxxxxxxxxxxxxxxxxxxAAr8BAAJWnbFKAAE"

# ================================================
# ۳ ژبې
# ================================================
T_DATA = {
    "ps": {
        "welcome"    : (
            "🇦🇫✨━━━━━━━━━━━━━━━━━━✨🇦🇫\n\n"
            "🌟  اَفـغـان  نـاشـنـاس  چـَټ  🌟\n\n"
            "🇦🇫✨━━━━━━━━━━━━━━━━━━✨🇦🇫\n\n"
            "👋  ښـه  راغـلاسـت  ګـرانـه  دوسـت!\n\n"
            "🔐  پـیـغـامـونـه  بـشـپـړ  پـټ  دي\n"
            "🌍  د  افـغـانـستـان  هـر  ګـوټ  سـره  وصـل  شـه\n"
            "💬  نـاشـنـاس  خـبـرې  وکـړه  —  بـې  خـطـره!\n"
            "🎁  ډالـۍ:  30 💰  سـکـې\n\n"
            "━━━━━━━━━━━━━━\n"
            "🌍  هـیـواد  وټـاکـه:"
        ),
        "sel_gender" : "👇  جـنـسـیـت  وټـاکـه:",
        "male"       : "👨  هـلـک  یـم  💪",
        "female"     : "👩  نـجـلـۍ  یـم  🌸",
        "sel_age"    : "📅  عـمـر  وټـاکـه:",
        "sel_prov"   : "📍  ولایـت  وټـاکـه:",
        "enter_name" : "📛  نـوم  ولـیـکـه:\n🎓 سـتـوډنـټ→نـوم+S\n🌍 بـهـر→نـوم+A",
        "done"       : "🎉  ثـبـت  بـشـپـړ  شـو!\n🎁  30  سـکـه  ومـومـلـه!",
        "menu"       : "🏠  مـیـنـو:",
        "connected"  : "🎉  وصـل  شـوئ!",
        "chat_end"   : "❌  چـټ  پـای  تـه  ورسـیـد\n⭐  امـتـیـاز  ورکـړئ:",
        "waiting"    : "⏳  انـتـظـار  کـوئ...",
        "no_coins"   : "❌  کـافـي  سـکـې  نـلـرې!",
        "banned"     : "⛔  تـاسـو  بـلاک  یـاسـت",
        "join_ch"    : "⚠️  لـومـړی  کـانـالـونـه  جـویـن  کـړه:",
        "check_join" : "✅  جـویـن  مـې  وکـړ",
        "back"       : "🔙  شـاتـه",
        "cancel_w"   : "❌  انـتـظـار  لـغـوه  کـړه",
        "random"     : "🎲  شـانـسـي  وصـل  ━━  وړیـا  🆓",
        "special"    : "🔗  ځـانـګـړی  وصـل",
        "my_fav"     : "⭐  زمـا  ځـانـګـړي  کـسـان",
        "no_chat"    : "🚫  بـې  چـټ  کـسـان",
        "liked_me"   : "❤️  خـوښـوونـکـي",
        "my_hist"    : "📜  زمـا  وروسـتـي  چـټـونـه",
        "invite"     : "👥  بـلـنـه  ━━  +10 💰",
        "daily"      : "🎁  ورځـنـۍ  جـایـزه  ━━  +5 💰",
        "help"       : "😊  لارښـود",
        "feedback"   : "📮  وړانـدیـز",
        "anon_link"  : "📧  نـاشـنـاس  لـیـنـک",
        "profile"    : "👤  پـروفایـل",
        "coins_lbl"  : "💰  سـکـې",
        "girls"      : "👩  نـجـونـې",
        "boys"       : "👨  هـلـکـان",
        "same_age"   : "👥  هـم  زولـي",
        "same_prov"  : "🏛  هـم  ولایـتـي",
        "same_city"  : "🏠  هـم  ښـاریـان",
        "new_u"      : "🆕  نـوي  کـاروونـکـي",
        "top_r"      : "❤️  لـوړ  امـتـیـاز",
        "night"      : "🌙  د  شـپـې  کـسـان",
        "students"   : "🎓  سـتـوډنـټـان",
        "abroad"     : "🌍  بـهـرنـي",
        "vip"        : "💎  VIP",
        "recent"     : "🔄  وروسـتـي  مـخـاطـب",
        "nearby"     : "📍  نـژدې  کـسـان",
        "search"     : "🔍  لـټـون",
        "next_p"     : "⏭  بـل  کـس  🔀",
        "stop_ch"    : "❌  چـټ  بـنـد",
        "report"     : "🚨  راپـور",
        "direct"     : "📩  مـسـتـقـیـم  پـیـغـام",
        "view_prof"  : "👤  د  مـخـاطـب  پـروفایـل",
        "like"       : "❤️  خـوښـول",
        "fav"        : "⭐  ځـانـګـړي",
        "chg_lang"   : "🌍  ژبـه  بـدل  کـړه",
        "country_s"  : "🌍  هـیـواد  وټـاکـه:",
        "lang_s"     : "🗣  ژبـه  وټـاکـه:",
        "warning"    : "⚠️  خـبـرداری!",
        "report_ok"  : "🚨  راپـور  ثـبـت  شـو",
        "buy_coins"  : "💳  د  سـکـو  اخـیـسـتـل",
        "prof_viewed": "👁  مـخـاطـب  ستـا  پـروفایـل  وکـتـل!",
    },
    "fa": {
        "welcome"    : (
            "🌟  چت  ناشناس  افغانی  🌟\n\n"
            "👋  خوش  آمدید!\n"
            "🔐  پیام‌ها  کاملاً  محرمانه\n"
            "🎁  هدیه:  30 💰  سکه\n\n"
            "🌍  کشور  را  انتخاب  کنید:"
        ),
        "sel_gender" : "👇  جنسیت  را  انتخاب  کنید:",
        "male"       : "👨  پسر  هستم  💪",
        "female"     : "👩  دختر  هستم  🌸",
        "sel_age"    : "📅  سن  را  انتخاب  کنید:",
        "sel_prov"   : "📍  استان  را  انتخاب  کنید:",
        "enter_name" : "📛  نام  بنویسید:\n🎓 دانشجو→نام+S\n🌍 خارج→نام+A",
        "done"       : "🎉  ثبت‌نام  کامل  شد!\n🎁  30  سکه  هدیه!",
        "menu"       : "🏠  منو:",
        "connected"  : "🎉  متصل  شدید!",
        "chat_end"   : "❌  چت  پایان  یافت\n⭐  امتیاز  بدهید:",
        "waiting"    : "⏳  در  حال  انتظار...",
        "no_coins"   : "❌  سکه  کافی  ندارید!",
        "banned"     : "⛔  شما  مسدود  شده‌اید",
        "join_ch"    : "⚠️  ابتدا  در  کانال‌ها  عضو  شوید:",
        "check_join" : "✅  عضو  شدم",
        "back"       : "🔙  برگشت",
        "cancel_w"   : "❌  لغو  انتظار",
        "random"     : "🎲  اتصال  تصادفی  ━━  رایگان  🆓",
        "special"    : "🔗  اتصال  ویژه",
        "my_fav"     : "⭐  افراد  مورد  علاقه",
        "no_chat"    : "🚫  افراد  بدون  چت",
        "liked_me"   : "❤️  کسانی  که  لایک  کردند",
        "my_hist"    : "📜  آخرین  چت‌های  من",
        "invite"     : "👥  دعوت  ━━  +10 💰",
        "daily"      : "🎁  جایزه  روزانه  ━━  +5 💰",
        "help"       : "😊  راهنما",
        "feedback"   : "📮  پیشنهاد",
        "anon_link"  : "📧  لینک  ناشناس",
        "profile"    : "👤  پروفایل",
        "coins_lbl"  : "💰  سکه",
        "girls"      : "👩  دختران",
        "boys"       : "👨  پسران",
        "same_age"   : "👥  هم‌سن",
        "same_prov"  : "🏛  هم‌استانی",
        "same_city"  : "🏠  هم‌شهری",
        "new_u"      : "🆕  کاربران  جدید",
        "top_r"      : "❤️  امتیاز  بالا",
        "night"      : "🌙  شب‌زنده‌ها",
        "students"   : "🎓  دانشجویان",
        "abroad"     : "🌍  خارج  از  کشور",
        "vip"        : "💎  VIP",
        "recent"     : "🔄  آخرین  مخاطب",
        "nearby"     : "📍  افراد  نزدیک",
        "search"     : "🔍  جستجو",
        "next_p"     : "⏭  نفر  بعدی  🔀",
        "stop_ch"    : "❌  بستن  چت",
        "report"     : "🚨  گزارش",
        "direct"     : "📩  پیام  مستقیم",
        "view_prof"  : "👤  پروفایل  مخاطب",
        "like"       : "❤️  لایک",
        "fav"        : "⭐  علاقه‌مند",
        "chg_lang"   : "🌍  تغییر  زبان",
        "country_s"  : "🌍  کشور  را  انتخاب  کنید:",
        "lang_s"     : "🗣  زبان  را  انتخاب  کنید:",
        "warning"    : "⚠️  هشدار!",
        "report_ok"  : "🚨  گزارش  ثبت  شد",
        "buy_coins"  : "💳  خرید  سکه",
        "prof_viewed": "👁  کسی  پروفایل  شما  را  دید!",
    },
    "en": {
        "welcome"    : (
            "🌟  Afghan  Anonymous  Chat  🌟\n\n"
            "👋  Welcome!\n"
            "🔐  Messages  are  private\n"
            "🎁  Gift:  30 💰  coins\n\n"
            "🌍  Select  your  country:"
        ),
        "sel_gender" : "👇  Select  gender:",
        "male"       : "👨  I'm  Male  💪",
        "female"     : "👩  I'm  Female  🌸",
        "sel_age"    : "📅  Select  your  age:",
        "sel_prov"   : "📍  Select  your  region:",
        "enter_name" : "📛  Write  your  name:\n🎓 Student→name+S\n🌍 Abroad→name+A",
        "done"       : "🎉  Registration  complete!\n🎁  You  got  30  coins!",
        "menu"       : "🏠  Menu:",
        "connected"  : "🎉  Connected!",
        "chat_end"   : "❌  Chat  ended\n⭐  Rate  your  partner:",
        "waiting"    : "⏳  Waiting...",
        "no_coins"   : "❌  Not  enough  coins!",
        "banned"     : "⛔  You  are  banned",
        "join_ch"    : "⚠️  First  join  the  channels:",
        "check_join" : "✅  I  joined",
        "back"       : "🔙  Back",
        "cancel_w"   : "❌  Cancel  wait",
        "random"     : "🎲  Random  Connect  ━━  Free  🆓",
        "special"    : "🔗  Special  Connect",
        "my_fav"     : "⭐  My  Favorites",
        "no_chat"    : "🚫  No-chat  users",
        "liked_me"   : "❤️  Who  liked  me",
        "my_hist"    : "📜  My  recent  chats",
        "invite"     : "👥  Invite  ━━  +10 💰",
        "daily"      : "🎁  Daily  Bonus  ━━  +5 💰",
        "help"       : "😊  Help",
        "feedback"   : "📮  Feedback",
        "anon_link"  : "📧  Anonymous  Link",
        "profile"    : "👤  Profile",
        "coins_lbl"  : "💰  Coins",
        "girls"      : "👩  Girls",
        "boys"       : "👨  Boys",
        "same_age"   : "👥  Same  Age",
        "same_prov"  : "🏛  Same  Region",
        "same_city"  : "🏠  Same  City",
        "new_u"      : "🆕  New  Users",
        "top_r"      : "❤️  Top  Rated",
        "night"      : "🌙  Night  Owls",
        "students"   : "🎓  Students",
        "abroad"     : "🌍  Abroad",
        "vip"        : "💎  VIP",
        "recent"     : "🔄  Recent  Contact",
        "nearby"     : "📍  Nearby",
        "search"     : "🔍  Search",
        "next_p"     : "⏭  Next  🔀",
        "stop_ch"    : "❌  End  Chat",
        "report"     : "🚨  Report",
        "direct"     : "📩  Direct  Message",
        "view_prof"  : "👤  Partner  Profile",
        "like"       : "❤️  Like",
        "fav"        : "⭐  Favorite",
        "chg_lang"   : "🌍  Change  Language",
        "country_s"  : "🌍  Select  your  country:",
        "lang_s"     : "🗣  Select  language:",
        "warning"    : "⚠️  Warning!",
        "report_ok"  : "🚨  Report  submitted",
        "buy_coins"  : "💳  Buy  Coins",
        "prof_viewed": "👁  Someone  viewed  your  profile!",
    },
}

def T(uid, key):
    lang = users.get(uid, {}).get("lang", "ps")
    return T_DATA.get(lang, T_DATA["ps"]).get(key, key)

def get_lang(uid):
    return users.get(uid, {}).get("lang", "ps")

def is_admin(uid):
    return uid == ADMIN_ID or uid in EXTRA_ADMINS

def has_perm(uid, perm):
    if uid == ADMIN_ID: return True
    return perm in EXTRA_ADMINS.get(uid, {}).get("perms", set())

def btn(text, data):
    return InlineKeyboardButton(text, callback_data=data)

# ================================================
# کیبوردونه
# ================================================

def country_kb():
    return InlineKeyboardMarkup([
        [btn("🇦🇫  افغانستان", "country_af")],
        [btn("🇮🇷  ایران", "country_ir")],
        [btn("🇺🇸  امریکا  /  بهر  /  Abroad", "country_us")],
    ])

def lang_kb(country="af"):
    if country == "ir":
        order = [("🇮🇷  فارسی","lang_fa"),("🇦🇫  پښتو","lang_ps"),("🇺🇸  English","lang_en")]
    elif country == "us":
        order = [("🇺🇸  English","lang_en"),("🇦🇫  پښتو","lang_ps"),("🇮🇷  فارسی","lang_fa")]
    else:
        order = [("🇦🇫  پښتو","lang_ps"),("🇮🇷  فارسی","lang_fa"),("🇺🇸  English","lang_en")]
    return InlineKeyboardMarkup([[btn(t,d)] for t,d in order])

def main_menu(uid):
    c = CONNECT_COST
    rows = [
        [btn(T(uid,"random"), "random_connect")],
        [btn(f"{T(uid,'special')}  ━━  {c} 💰", "connect_menu")],
        [btn(f"{T(uid,'girls')}  ━━  {c} 💰","users_female"),
         btn(f"{T(uid,'boys')}  ━━  {c} 💰","users_male")],
        [btn(f"{T(uid,'my_fav')}  ━━  {c} 💰","my_favorites"),
         btn(f"{T(uid,'no_chat')}  ━━  {c} 💰","no_chat_users")],
        [btn(f"{T(uid,'liked_me')}  ━━  {c} 💰","liked_me"),
         btn(f"{T(uid,'my_hist')}  ━━  وړیا","my_history")],
        [btn(T(uid,"help"),"help"),
         btn(T(uid,"profile"),"profile"),
         btn(T(uid,"coins_lbl"),"coins")],
        [btn(T(uid,"anon_link"),"my_link"),
         btn(T(uid,"feedback"),"feedback")],
        [btn(T(uid,"invite"),"invite"),
         btn(T(uid,"daily"),"daily_bonus")],
        [btn(T(uid,"chg_lang"),"change_lang"),
         btn("📞  پشتیبانی  /  Support","support")],
    ]
    if is_admin(uid):
        rows.append([btn("🛠  ━━  ادمین  پنل  ━━  🛠","open_admin")])
    return InlineKeyboardMarkup(rows)
def connect_menu_kb(uid):
    c = CONNECT_COST
    return InlineKeyboardMarkup([
        [btn(T(uid,"random"),"random_connect")],
        [btn(f"{T(uid,'girls')}  ━━  {c} 💰","users_female"),
         btn(f"{T(uid,'boys')}  ━━  {c} 💰","users_male")],
        [btn(f"{T(uid,'same_age')}  ━━  {c} 💰","same_age"),
         btn(f"{T(uid,'same_prov')}  ━━  {c} 💰","same_province")],
        [btn(f"{T(uid,'same_city')}  ━━  {c} 💰","same_city")],
        [btn(f"{T(uid,'new_u')}  ━━  {c} 💰","new_users"),
         btn(f"{T(uid,'top_r')}  ━━  {c} 💰","top_likes")],
        [btn(f"{T(uid,'night')}  ━━  {c} 💰","night_users")],
        [btn(f"{T(uid,'students')}  ━━  {c} 💰","student_users"),
         btn(f"{T(uid,'abroad')}  ━━  {c} 💰","abroad_users")],
        [btn(f"{T(uid,'vip')}  ━━  {c} 💰","vip_users"),
         btn(f"{T(uid,'recent')}  ━━  وړیا","recent_chat")],
        [btn(f"{T(uid,'nearby')}  ━━  {c} 💰","near_me"),
         btn(f"{T(uid,'search')}  ━━  {c} 💰","search_name")],
        [btn(f"{T(uid,'my_fav')}  ━━  {c} 💰","my_favorites"),
         btn(f"{T(uid,'no_chat')}  ━━  {c} 💰","no_chat_users")],
        [btn(f"{T(uid,'liked_me')}  ━━  {c} 💰","liked_me"),
         btn(f"{T(uid,'my_hist')}  ━━  وړیا","my_history")],
        [btn(T(uid,"back"),"menu")],
    ])

def chat_menu(uid):
    l = get_lang(uid)
    ml = "مینو" if l=="ps" else "منو" if l=="fa" else "Menu"
    return InlineKeyboardMarkup([
        [btn(T(uid,"next_p"),"next"), btn(T(uid,"stop_ch"),"stop")],
        [btn(T(uid,"report"),"report"), btn(f"{T(uid,'direct')}  💰","send_direct")],
        [btn(f"{T(uid,'view_prof')}  🔎","info")],
        [btn(T(uid,"like"),"like_partner"), btn(T(uid,"fav"),"fav_partner")],
        [btn(f"🏠  {ml}","menu")],
    ])

def gender_kb(uid):
    return InlineKeyboardMarkup([
        [btn(T(uid,"male"),"gender_male")],
        [btn(T(uid,"female"),"gender_female")],
    ])

def age_kb():
    rows = []
    for i in range(15,51,5):
        rows.append([btn(f"  {j}  ",f"age_{j}") for j in range(i,min(i+5,51))])
    return InlineKeyboardMarkup(rows)

def province_kb(uid):
    country = users.get(uid,{}).get("country","af")
    provs   = PROVINCES.get(country, PROVINCES["af"])
    rows = []
    for i in range(0,len(provs),2):
        row = [btn(f"  {provs[i]}  ",f"prov_{i}")]
        if i+1 < len(provs):
            row.append(btn(f"  {provs[i+1]}  ",f"prov_{i+1}"))
        rows.append(row)
    return InlineKeyboardMarkup(rows)

def stars_kb(target_uid):
    return InlineKeyboardMarkup([
        [btn("⭐1",f"gs_{target_uid}_1"),btn("⭐⭐2",f"gs_{target_uid}_2"),
         btn("⭐⭐⭐3",f"gs_{target_uid}_3")],
        [btn("⭐⭐⭐⭐4",f"gs_{target_uid}_4"),
         btn("⭐⭐⭐⭐⭐5",f"gs_{target_uid}_5")],
        [btn("⏭  Skip","skip_rating")],
    ])

def admin_menu_kb():
    return InlineKeyboardMarkup([
        [btn("📊  آمار","adm_stats")],
        [btn("📢  همګاني  پیغام","adm_broadcast")],
        [btn("🔍  د  کاربر  معلومات","adm_find_user")],
        [btn("💰  سکې  لیږل","adm_give_coins"),
         btn("💸  سکې  کمول","adm_remove_coins")],
        [btn("🚫  بلاک","adm_ban_input"),
         btn("✅  انبلاک","adm_unban_input")],
        [btn("⚠️  اخطار  ورکول","adm_warn_user"),
         btn("📩  پیغام  کاربر  ته","adm_msg_user")],
        [btn("📋  د  کاربرانو  لیست","adm_user_list")],
        [btn("💬  اوسني  چټونه","adm_active_chats")],
        [btn("⭐  د  ستورو  لیست","adm_ratings"),
         btn("🎁  ستوري  لیږل","adm_send_rating")],
        [btn("👮  ادمین  اضافه","adm_add_admin"),
         btn("❌  ادمین  حذف","adm_rem_admin")],
        [btn("📜  د  ادمینانو  لیست","adm_list_admins")],
        [btn("🔐  د  ادمین  اجازې","adm_set_perms")],
        [btn("🔒  کانال  قفل  ON/OFF","adm_ch_lock"),
         btn("📋  راپورونه","adm_reports")],
        [btn("📢  کانالونو  لیست","adm_channels")],
        [btn("🔙  مینو","menu")],
    ])

def channel_join_kb(not_joined, uid):
    rows = []
    for i,ch in enumerate(not_joined):
        rows.append([InlineKeyboardButton(
            f"📢  کانال  {i+1}  —  {ch}",
            url=f"https://t.me/{ch.replace('@','')}"
        )])
    rows.append([btn(T(uid,"check_join"),"check_join")])
    return InlineKeyboardMarkup(rows)

def perms_kb(target_uid):
    cur  = EXTRA_ADMINS.get(target_uid,{}).get("perms",set())
    rows = [[btn(f"{'✅' if p in cur else '❌'}  {p}",f"tperm_{target_uid}_{p}")] for p in sorted(ALL_PERMS)]
    rows.append([btn("🔙  شاته","adm_list_admins")])
    return InlineKeyboardMarkup(rows)

def back_admin():
    return InlineKeyboardMarkup([[btn("🔙  شاته","adm_back")]])

# ================================================
# کمکي
# ================================================

def check_coins(uid, cost):
    if users[uid].get("coins",0) < cost: return False
    users[uid]["coins"] -= cost; return True

async def get_not_joined(uid, context):
    if not CHANNEL_LOCK: return []
    nj = []
    for ch in REQUIRED_CHANNELS:
        try:
            m = await context.bot.get_chat_member(ch, uid)
            if m.status not in [ChatMember.MEMBER,ChatMember.ADMINISTRATOR,ChatMember.OWNER]:
                nj.append(ch)
        except: nj.append(ch)
    return nj

def new_user(name):
    return {
        "gender":None,"province":None,"age":None,"city":"",
        "coins":30,"vip":False,"state":"idle","name":name,
        "partner":None,"last_daily":datetime.now()-timedelta(days=2),
        "chats":0,"likes":0,"refs":0,"blocked":[],
        "step":"country","recent":[],"joined":datetime.now(),
        "anon_link":f"anon_{random.randint(100000,999999)}",
        "ratings":[],"avg_rating":5.0,"waiting_filter":None,
        "last_chat_partner":None,"is_student":False,"is_abroad":False,
        "lang":"ps","country":"af","favorites":[],"liked_by":[],
        "warnings":0,"chat_history":[], "photo_id": None,
    }

def gstr(usr, viewer_uid):
    l = get_lang(viewer_uid)
    g = usr.get("gender","?")
    if l=="ps": return "👨 هلک" if g=="male" else "👩 نجلۍ"
    if l=="fa": return "👨 پسر" if g=="male" else "👩 دختر"
    return "👨 Male" if g=="male" else "👩 Female"

# ================================================
# چټ بندول
# ================================================

async def stop_chat(uid, context, query):
    if uid not in users or users[uid].get("state") != "chatting":
        if query:
            try: await query.edit_message_text(T(uid,"menu"), reply_markup=main_menu(uid))
            except: pass
        return
    pid = users[uid]["partner"]
    users[uid].update({"state":"idle","partner":None,"last_chat_partner":pid})
    for a,b in [(uid,pid),(pid,uid) if pid else (None,None)]:
        if a and b:
            users[a].setdefault("chat_history",[])
            if b not in users[a]["chat_history"]: users[a]["chat_history"].insert(0,b)
            users[a]["chat_history"] = users[a]["chat_history"][:20]
    if pid and pid in users:
        users[pid].update({"state":"idle","partner":None,"last_chat_partner":uid})
        try: await context.bot.send_message(pid, T(pid,"chat_end"), reply_markup=stars_kb(uid))
        except: pass
    msg = T(uid,"chat_end")
    kb  = stars_kb(pid) if pid else main_menu(uid)
    if query:
        try: await query.edit_message_text(msg, reply_markup=kb)
        except: pass
    else:
        try: await context.bot.send_message(uid, msg, reply_markup=kb)
        except: pass

# ================================================
# چټ موندل
# ================================================

async def find_chat(uid, context, ftype, query, cost=0):
    u = users[uid]
    if u.get("state") == "chatting":
        try: await query.edit_message_text(T(uid,"menu"), reply_markup=chat_menu(uid))
        except: pass
        return
    if u.get("step") != "done":
        try: await query.edit_message_text(T(uid,"menu"), reply_markup=main_menu(uid))
        except: pass
        return
    if cost > 0 and not check_coins(uid, cost):
        try: await query.edit_message_text(T(uid,"no_coins"), reply_markup=main_menu(uid))
        except: pass
        return
    now_h = datetime.now().hour
    cands = []
    for pid,pu in users.items():
        if pid==uid or pu.get("step")!="done" or pu.get("state")!="waiting": continue
        if pid in u.get("blocked",[]) or uid in pu.get("blocked",[]): continue
        if pid in banned: continue
        if ftype=="female_only"   and pu.get("gender")!="female": continue
        if ftype=="male_only"     and pu.get("gender")!="male": continue
        if ftype=="same_age"      and abs(pu.get("age",0)-u.get("age",0))>3: continue
        if ftype=="same_province" and pu.get("province")!=u.get("province"): continue
        if ftype=="same_city"     and pu.get("city","")!=u.get("city",""): continue
        if ftype=="new_users"     and (datetime.now()-pu.get("joined",datetime.now())).days>=7: continue
        if ftype=="near_me"       and pu.get("province")!=u.get("province"): continue
        if ftype=="night_users"   and not (22<=now_h or now_h<5): continue
        if ftype=="student_users" and not pu.get("is_student"): continue
        if ftype=="abroad_users"  and not pu.get("is_abroad"): continue
        if ftype=="vip_users"     and not pu.get("vip"): continue
        if ftype=="recent_chat"   and pid not in u.get("recent",[]): continue
        if ftype=="my_favorites"  and pid not in u.get("favorites",[]): continue
        if ftype=="no_chat"       and pu.get("chats",0)>0: continue
        if ftype=="liked_me"      and uid not in pu.get("liked_by",[]): continue
        if ftype=="my_history"    and pid not in u.get("chat_history",[]): continue
        cands.append(pid)
    if ftype=="top_likes":
        cands.sort(key=lambda p: users[p].get("avg_rating",0), reverse=True)
    else:
        random.shuffle(cands)
    if not cands:
        users[uid]["state"]="waiting"; users[uid]["waiting_filter"]=ftype
        try:
            await query.edit_message_text(T(uid,"waiting"),
                reply_markup=InlineKeyboardMarkup([[btn(T(uid,"cancel_w"),"cancel_wait")]]))
        except: pass
        return
    pid = cands[0]
    users[uid].update({"state":"chatting","partner":pid,"chats":u.get("chats",0)+1,"waiting_filter":None})
    users[pid].update({"state":"chatting","partner":uid,"chats":users[pid].get("chats",0)+1,"waiting_filter":None})
    for a,b in [(uid,pid),(pid,uid)]:
        users[a].setdefault("recent",[])
        if b not in users[a]["recent"]: users[a]["recent"].append(b)
    p  = users[pid]
    ct = f"\n💰 {cost}" if cost > 0 else ""
    await context.bot.send_message(uid,
        f"{T(uid,'connected')}{ct}\n\n━━━━━━━━━━━━━━\n"
        f"{gstr(p,uid)}  |  🎂 {p.get('age','?')}  |  📍 {p.get('province','?')}\n━━━━━━━━━━━━━━",
        reply_markup=chat_menu(uid))
    await context.bot.send_message(pid,
        f"{T(pid,'connected')}\n\n━━━━━━━━━━━━━━\n"
        f"{gstr(u,pid)}  |  🎂 {u.get('age','?')}  |  📍 {u.get('province','?')}\n━━━━━━━━━━━━━━",
        reply_markup=chat_menu(pid))

# ================================================
# د پروفایل متن جوړول
# ================================================

def profile_text(uid, target_uid=None):
    tid = target_uid or uid
    u   = users.get(tid, {})
    l   = get_lang(uid)
    g   = gstr(u, uid)
    tags = []
    if u.get("vip"):         tags.append("💎 VIP")
    if u.get("is_student"):  tags.append("🎓")
    if u.get("is_abroad"):   tags.append("🌍")
    days = (datetime.now() - u.get("joined",datetime.now())).days
    title = T(uid,"profile") if not target_uid else T(uid,"view_prof")
    return (
        f"{title}\n\n━━━━━━━━━━━━━━\n"
        f"📛 {u.get('name','?')}\n"
        f"{g}  |  🎂 {u.get('age','?')}  |  📍 {u.get('province','?')}\n"
        f"{'  '.join(tags)}\n"
        f"⭐ {u.get('avg_rating',5.0)}/5  |  ❤️ {u.get('likes',0)}\n"
        f"💬 {u.get('chats',0)}  |  💰 {u.get('coins',0)}\n"
        f"📅 {days}d\n━━━━━━━━━━━━━━"
    )

# ================================================
# /start
# ================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    args = context.args
    if uid in banned:
        await update.message.reply_text("⛔"); return
    nj = await get_not_joined(uid, context)
    if nj:
        await update.message.reply_text(
            T(uid,"join_ch")+"\n\n"+"\n".join([f"📢 {c}" for c in nj]),
            reply_markup=channel_join_kb(nj, uid)); return
    if args and args[0].startswith("ref_"):
        try:
            ref_id = int(args[0].split("_")[1])
            if ref_id!=uid and ref_id in users and uid not in users:
                users[ref_id]["coins"]+=10; users[ref_id]["refs"]+=1
                try: await context.bot.send_message(ref_id,"🎉 +10 💰")
                except: pass
        except: pass
    elif args and args[0].startswith("anon_"):
        target = next((t for t,u in users.items() if u.get("anon_link")==args[0]),None)
        if target:
            if uid not in users: users[uid]=new_user(update.effective_user.first_name or "User")
            users[uid]["state"]="waiting_anon_msg"; users[uid]["anon_target"]=target
            await update.message.reply_text("📩 (1 💰):"); return
    if uid not in users:
        users[uid]=new_user(update.effective_user.first_name or "User")
        try: await update.message.reply_sticker(sticker=WELCOME_STICKER)
        except: pass
        await update.message.reply_text(T(uid,"welcome"), reply_markup=country_kb())
    else:
        u=users[uid]; step=u.get("step","country")
        if step=="country":    await update.message.reply_text(T(uid,"country_s"), reply_markup=country_kb())
        elif step=="lang":     await update.message.reply_text(T(uid,"lang_s"), reply_markup=lang_kb(u.get("country","af")))
        elif step=="gender":   await update.message.reply_text(T(uid,"sel_gender"), reply_markup=gender_kb(uid))
        elif step=="age":      await update.message.reply_text(T(uid,"sel_age"), reply_markup=age_kb())
        elif step=="province": await update.message.reply_text(T(uid,"sel_prov"), reply_markup=province_kb(uid))
        elif step=="name":     await update.message.reply_text(T(uid,"enter_name"))
        else:                  await update.message.reply_text(T(uid,"menu"), reply_markup=main_menu(uid))

async def lang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users: users[uid]=new_user(update.effective_user.first_name or "User")
    await update.message.reply_text(T(uid,"lang_s"), reply_markup=lang_kb(users[uid].get("country","af")))

async def admin_cmd(update, context):
    uid=update.effective_user.id
    if not is_admin(uid): await update.message.reply_text("❌"); return
    if uid not in users:
        users[uid]=new_user(update.effective_user.first_name or "Admin"); users[uid]["step"]="done"
    users[uid]["state"]="idle"
    await update.message.reply_text("🛠  ادمین  پنل:", reply_markup=admin_menu_kb())

async def ban_cmd(update,context):
    if not is_admin(update.effective_user.id): return
    if not context.args: return
    try:
        t=int(context.args[0]); banned.add(t)
        if t in users: users[t]["state"]="idle"
        await update.message.reply_text(f"🚫 {t}")
        try: await context.bot.send_message(t,"⛔")
        except: pass
    except: pass

async def unban_cmd(update,context):
    if not is_admin(update.effective_user.id): return
    if not context.args: return
    try:
        t=int(context.args[0]); banned.discard(t)
        await update.message.reply_text(f"✅ {t}")
        try: await context.bot.send_message(t,"✅ /start")
        except: pass
    except: pass

async def daily_cmd(update,context):
    uid=update.effective_user.id
    if uid not in users: return
    u=users[uid]; now=datetime.now()
    if now-u.get("last_daily",now-timedelta(days=2))>=timedelta(hours=24):
        u["coins"]+=5; u["last_daily"]=now
        await update.message.reply_text(f"🎁 +5 💰 → {u['coins']}")
    else:
        wait=timedelta(hours=24)-(now-u["last_daily"])
        h,m=wait.seconds//3600,(wait.seconds%3600)//60
        await update.message.reply_text(f"⏰ {h}h {m}m")

# ================================================
# ادمین هندلر
# ================================================

async def handle_admin(query, uid, data, context):
    global CHANNEL_LOCK
    if data in ("open_admin","adm_back"):
        await query.edit_message_text("🛠  ادمین  پنل:", reply_markup=admin_menu_kb())
    elif data=="adm_stats":
        t=len(users); cc=sum(1 for u in users.values() if u.get("state")=="chatting")
        wc=sum(1 for u in users.values() if u.get("state")=="waiting")
        m=sum(1 for u in users.values() if u.get("gender")=="male")
        f=sum(1 for u in users.values() if u.get("gender")=="female")
        af=sum(1 for u in users.values() if u.get("country")=="af")
        ir=sum(1 for u in users.values() if u.get("country")=="ir")
        us=sum(1 for u in users.values() if u.get("country")=="us")
        await query.edit_message_text(
            f"📊  آمار\n\n👥 {t}  |  💬 {cc//2}  |  ⏳ {wc}\n"
            f"👨 {m}  |  👩 {f}  |  🚫 {len(banned)}\n"
            f"🇦🇫 {af}  |  🇮🇷 {ir}  |  🌍 {us}\n"
            f"👮 {len(EXTRA_ADMINS)+1}  |  🔒 {'✅' if CHANNEL_LOCK else '❌'}",
            reply_markup=back_admin())
    elif data=="adm_user_list":
        if not has_perm(uid,"user_list"): await query.answer("❌",show_alert=True); return
        text="📋  لیست:\n\n"
        for tid,tu in sorted(users.items(),key=lambda x:x[1].get("joined",datetime.min),reverse=True)[:20]:
            g="👨" if tu.get("gender")=="male" else "👩"
            bst="🚫" if tid in banned else "✅"
            v="💎" if tu.get("vip") else ""
            text+=f"{bst}{v}{g} `{tid}` {tu.get('name','?')} — 💰{tu.get('coins',0)} ⚠️{tu.get('warnings',0)}\n"
        await query.edit_message_text(text, reply_markup=back_admin())
    elif data=="adm_warn_user":
        if not has_perm(uid,"warn"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("⚠️  آیدي  ولیکه:"); users[uid]["state"]="adm_warn_input"
    elif data=="adm_msg_user":
        if not has_perm(uid,"msg_user"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("📩  آیدي|پیغام:"); users[uid]["state"]="adm_msg_input"
    elif data=="adm_remove_coins":
        if not has_perm(uid,"remove_coins"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("💸  آیدي/مقدار:"); users[uid]["state"]="adm_rm_coins"
    elif data=="adm_add_admin":
        if uid!=ADMIN_ID: await query.answer("❌",show_alert=True); return
        await query.edit_message_text("👮  آیدي  ولیکه:"); users[uid]["state"]="adm_add_adm"
    elif data=="adm_rem_admin":
        if uid!=ADMIN_ID: await query.answer("❌",show_alert=True); return
        await query.edit_message_text("❌  آیدي  ولیکه:"); users[uid]["state"]="adm_del_adm"
    elif data=="adm_list_admins":
        text=f"📜  ادمینان:\n\n👑 `{ADMIN_ID}`\n\n"
        for aid,info in EXTRA_ADMINS.items():
            text+=f"👮 `{aid}` {info.get('name','?')}\n🔐 {', '.join(info.get('perms',set())) or '—'}\n\n"
        await query.edit_message_text(text if EXTRA_ADMINS else text+"نشته", reply_markup=back_admin())
    elif data=="adm_set_perms":
        if uid!=ADMIN_ID: await query.answer("❌",show_alert=True); return
        await query.edit_message_text("🔐  آیدي  ولیکه:"); users[uid]["state"]="adm_perms_input"
    elif data.startswith("tperm_"):
        if uid!=ADMIN_ID: await query.answer("❌",show_alert=True); return
        parts=data.split("_",2); target=int(parts[1]); perm=parts[2]
        if target in EXTRA_ADMINS:
            ps=EXTRA_ADMINS[target].get("perms",set())
            ps.discard(perm) if perm in ps else ps.add(perm)
            EXTRA_ADMINS[target]["perms"]=ps
        await query.edit_message_text(f"🔐 `{target}`:", reply_markup=perms_kb(target))
    elif data=="adm_broadcast":
        if not has_perm(uid,"broadcast"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("📢  پیغام  ولیکه:"); users[uid]["state"]="adm_broadcast"
    elif data=="adm_find_user":
        if not has_perm(uid,"find_user"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("🔍  آیدي  ولیکه:"); users[uid]["state"]="adm_find_uid"
    elif data=="adm_give_coins":
        if not has_perm(uid,"give_coins"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("💰  آیدي/مقدار:"); users[uid]["state"]="adm_give_coins"
    elif data=="adm_ban_input":
        if not has_perm(uid,"ban"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("🚫  آیدي:"); users[uid]["state"]="adm_ban_input"
    elif data=="adm_unban_input":
        if not has_perm(uid,"unban"): await query.answer("❌",show_alert=True); return
        await query.edit_message_text("✅  آیدي:"); users[uid]["state"]="adm_unban_input"
    elif data=="adm_active_chats":
        pairs,seen=[],set()
        for tid,tu in users.items():
            if tu.get("state")=="chatting" and tid not in seen:
                pid=tu.get("partner")
                if pid and pid in users:
                    seen.update([tid,pid])
                    g1="👨" if tu.get("gender")=="male" else "👩"
                    g2="👨" if users[pid].get("gender")=="male" else "👩"
                    pairs.append(f"{g1}`{tid}` ↔ {g2}`{pid}`")
        await query.edit_message_text(
            f"💬  ({len(pairs)}):\n\n"+"\n".join(pairs[:30]) if pairs else "💬  نشته",
            reply_markup=back_admin())
    elif data=="adm_ratings":
        rated=sorted([(t,u) for t,u in users.items() if u.get("ratings")],
            key=lambda x:x[1].get("avg_rating",0),reverse=True)
        if not rated: await query.edit_message_text("⭐ نشته",reply_markup=admin_menu_kb()); return
        text="⭐  لیست:\n\n"
        for tid,tu in rated[:20]:
            g="👨" if tu.get("gender")=="male" else "👩"
            text+=f"{g} {tu.get('name','?')} — {tu.get('avg_rating',0)}/5\n"
        await query.edit_message_text(text, reply_markup=back_admin())
    elif data=="adm_send_rating":
        await query.edit_message_text("🎁  آیدي/ستوري:"); users[uid]["state"]="adm_send_rating"
    elif data=="adm_ch_lock":
        if not has_perm(uid,"channel_lock"): await query.answer("❌",show_alert=True); return
        CHANNEL_LOCK=not CHANNEL_LOCK
        await query.edit_message_text(f"🔒 {'✅' if CHANNEL_LOCK else '❌'}", reply_markup=admin_menu_kb())
    elif data=="adm_channels":
        text="📢  کانالونه:\n\n"
        for i,ch in enumerate(REQUIRED_CHANNELS,1): text+=f"{i}. {ch}\n"
        await query.edit_message_text(text, reply_markup=back_admin())
    elif data=="adm_reports":
        if not has_perm(uid,"reports"): await query.answer("❌",show_alert=True); return
        if not reports: await query.edit_message_text("📋 نشته",reply_markup=admin_menu_kb()); return
        text="🚨  راپورونه:\n\n"
        for rid,cnt in sorted(reports.items(),key=lambda x:x[1],reverse=True)[:20]:
            mk="🚫" if rid in banned else "✅"
            text+=f"{mk} `{rid}` ({users.get(rid,{}).get('name','?')}): {cnt}\n"
        await query.edit_message_text(text, reply_markup=back_admin())
    elif data.startswith("adm_ban_target_"):
        target=int(data.split("_")[-1])
        if target in banned:
            banned.discard(target)
            try: await context.bot.send_message(target,"✅ /start")
            except: pass
            await query.edit_message_text(f"✅ {target}", reply_markup=admin_menu_kb())
        else:
            banned.add(target)
            if target in users: users[target]["state"]="idle"
            try: await context.bot.send_message(target,"⛔")
            except: pass
            await query.edit_message_text(f"🚫 {target}", reply_markup=admin_menu_kb())

# ================================================
# کالبک هندلر
# ================================================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query; uid=query.from_user.id; data=query.data
    await query.answer()
    if data.startswith("country_"):
        if uid not in users: users[uid]=new_user(query.from_user.first_name or "User")
        country=data.split("_")[1]; users[uid]["country"]=country
        users[uid]["lang"]="fa" if country=="ir" else "en" if country=="us" else "ps"
        users[uid]["step"]="lang"
        await query.edit_message_text(T(uid,"lang_s"), reply_markup=lang_kb(country)); return
    if data.startswith("lang_"):
        if uid not in users: users[uid]=new_user(query.from_user.first_name or "User")
        users[uid]["lang"]=data.split("_")[1]; users[uid]["step"]="gender"
        await query.edit_message_text(T(uid,"sel_gender"), reply_markup=gender_kb(uid)); return
    if data=="change_lang":
        country=users.get(uid,{}).get("country","af")
        await query.edit_message_text(T(uid,"lang_s"), reply_markup=lang_kb(country)); return
    if data=="check_join":
        nj=await get_not_joined(uid,context)
        if not nj: await query.edit_message_text("✅\n\n/start")
        else:
            await query.edit_message_text(
                T(uid,"join_ch")+"\n\n"+"\n".join([f"📢 {c}" for c in nj]),
                reply_markup=channel_join_kb(nj,uid))
        return
    if data.startswith("adm_") or data=="open_admin" or data.startswith("tperm_"):
        if not is_admin(uid): await query.answer("❌",show_alert=True); return
        if uid not in users:
            users[uid]=new_user(query.from_user.first_name or "Admin"); users[uid]["step"]="done"
        await handle_admin(query,uid,data,context); return
    if uid not in users: await query.edit_message_text("/start"); return
    u=users[uid]
    if u.get("step")!="done":
        ok=data in ("menu","check_join","skip_rating") or \
           data.startswith(("gender_","age_","prov_","gs_","country_","lang_"))
        if not ok: await query.answer("❌",show_alert=True); return
    if data.startswith("gender_"):
        u["gender"]=data.split("_")[1]; u["step"]="age"
        await query.edit_message_text(T(uid,"sel_age"), reply_markup=age_kb())
    elif data.startswith("age_"):
        u["age"]=int(data.split("_")[1]); u["step"]="province"
        await query.edit_message_text(T(uid,"sel_prov"), reply_markup=province_kb(uid))
    elif data.startswith("prov_"):
        country=u.get("country","af"); provs=PROVINCES.get(country,PROVINCES["af"])
        u["province"]=provs[int(data.split("_")[1])]; u["step"]="name"
        await query.edit_message_text(T(uid,"enter_name"))
    elif data.startswith("gs_"):
        parts=data.split("_"); target=int(parts[1]); stars=int(parts[2])
        if target in users:
            users[target].setdefault("ratings",[]).append({"from":uid,"stars":stars})
            all_s=[r["stars"] for r in users[target]["ratings"]]
            users[target]["avg_rating"]=round(sum(all_s)/len(all_s),1)
            users[target]["likes"]=len(all_s)
            try: await context.bot.send_message(target,f"⭐ {'⭐'*stars} ({stars}/5)\n{users[target]['avg_rating']}/5")
            except: pass
            # د امتیاز ورکولو وروسته +2 سکه
            users[uid]["coins"] = users[uid].get("coins",0) + 2
        await query.edit_message_text(f"✅ {'⭐'*stars}\n+2 💰", reply_markup=main_menu(uid))
    elif data=="skip_rating": await query.edit_message_text(T(uid,"menu"), reply_markup=main_menu(uid))
    elif data=="menu":        await query.edit_message_text(T(uid,"menu"), reply_markup=main_menu(uid))
    elif data=="connect_menu":await query.edit_message_text("👇", reply_markup=connect_menu_kb(uid))
    elif data=="random_connect":   await find_chat(uid,context,"random",query,0)
    elif data=="users_female":     await find_chat(uid,context,"female_only",query,CONNECT_COST)
    elif data=="users_male":       await find_chat(uid,context,"male_only",query,CONNECT_COST)
    elif data=="same_age":         await find_chat(uid,context,"same_age",query,CONNECT_COST)
    elif data=="same_province":    await find_chat(uid,context,"same_province",query,CONNECT_COST)
    elif data=="new_users":        await find_chat(uid,context,"new_users",query,CONNECT_COST)
    elif data=="top_likes":        await find_chat(uid,context,"top_likes",query,CONNECT_COST)
    elif data=="near_me":          await find_chat(uid,context,"near_me",query,CONNECT_COST)
    elif data=="night_users":      await find_chat(uid,context,"night_users",query,CONNECT_COST)
    elif data=="student_users":    await find_chat(uid,context,"student_users",query,CONNECT_COST)
    elif data=="abroad_users":     await find_chat(uid,context,"abroad_users",query,CONNECT_COST)
    elif data=="vip_users":        await find_chat(uid,context,"vip_users",query,CONNECT_COST)
    elif data=="recent_chat":      await find_chat(uid,context,"recent_chat",query,0)
    elif data=="my_favorites":     await find_chat(uid,context,"my_favorites",query,CONNECT_COST)
    elif data=="no_chat_users":    await find_chat(uid,context,"no_chat",query,CONNECT_COST)
    elif data=="liked_me":         await find_chat(uid,context,"liked_me",query,CONNECT_COST)
    elif data=="my_history":       await find_chat(uid,context,"my_history",query,0)
    elif data=="same_city":
        if not u.get("city"):
            await query.edit_message_text("🏠:"); u["state"]="waiting_city_set"
        else: await find_chat(uid,context,"same_city",query,CONNECT_COST)
    elif data=="search_name":
        if not check_coins(uid,CONNECT_COST):
            await query.edit_message_text(T(uid,"no_coins"),reply_markup=main_menu(uid)); return
        await query.edit_message_text("🔍:"); u["state"]="waiting_name"
    elif data=="cancel_wait":
        u["state"]="idle"; u["waiting_filter"]=None
        await query.edit_message_text(T(uid,"menu"), reply_markup=main_menu(uid))
    elif data=="stop":  await stop_chat(uid,context,query)
    elif data=="next":
        await stop_chat(uid,context,None)
        await find_chat(uid,context,"random",query,0)
    elif data=="report":
        if u.get("state")=="chatting":
            pid=u["partner"]; reports[pid]=reports.get(pid,0)+1
            await query.answer(T(uid,"report_ok"),show_alert=True)
            if reports[pid]>=3:
                banned.add(pid); await stop_chat(pid,context,None)
                try: await context.bot.send_message(pid,"⛔")
                except: pass
    elif data=="send_direct":
        if u.get("state")=="chatting":
            await query.edit_message_text(f"{T(uid,'direct')} (1 💰):")
            u["state"]="waiting_direct_msg"
    elif data=="like_partner":
        if u.get("state")=="chatting":
            pid=u["partner"]
            if pid in users:
                users[pid].setdefault("liked_by",[])
                if uid not in users[pid]["liked_by"]:
                    users[pid]["liked_by"].append(uid)
                    users[pid]["likes"]=len(users[pid]["liked_by"])
                    await query.answer("❤️ +1",show_alert=True)
                else: await query.answer("❤️",show_alert=True)
    elif data=="fav_partner":
        if u.get("state")=="chatting":
            pid=u["partner"]; u.setdefault("favorites",[])
            if pid not in u["favorites"]:
                u["favorites"].append(pid); await query.answer("⭐ ✅",show_alert=True)
            else: await query.answer("⭐",show_alert=True)
    elif data=="info":
        if u.get("state")=="chatting" and u["partner"] in users:
            pid  = u["partner"]
            p    = users[pid]
            text = profile_text(uid, pid)
            # د مخاطب ته خبرتیا — ستا پروفایل وکتل شو
            try:
                viewer_name = u.get("name","?")
                viewer_g    = gstr(u, pid)
                notify_text = (
                    f"{T(pid,'prof_viewed')}\n\n"
                    f"━━━━━━━━━━━━━━\n"
                    f"📛 {viewer_name}\n"
                    f"{viewer_g}  |  🎂 {u.get('age','?')}  |  📍 {u.get('province','?')}\n"
                    f"━━━━━━━━━━━━━━"
                )
                await context.bot.send_message(pid, notify_text)
            except: pass

            # ── د مخاطب عکس لیدل ──
            # لومړی د روباټ database کې ثبت شوی عکس وګوره
            photo_id = p.get("photo_id")

            # که database کې نه وي، د Telegram API نه واخله
            if not photo_id:
                try:
                    photos = await context.bot.get_user_profile_photos(pid, limit=1)
                    if photos and photos.photos:
                        photo_id = photos.photos[0][-1].file_id
                        # ثبت کړه چې بیا کار وکړو
                        users[pid]["photo_id"] = photo_id
                except: pass

            if photo_id:
                try:
                    await context.bot.send_photo(
                        chat_id=uid, photo=photo_id,
                        caption=text, reply_markup=chat_menu(uid))
                    return
                except: pass

            # که عکس نه وي — د عکس اضافه کولو پیشنهاد
            l = get_lang(pid)
            no_photo_hint = (
                "\n\n📸  مخاطب  لاهم  عکس  نه  دی  ثبت  کړی" if get_lang(uid)=="ps" else
                "\n\n📸  مخاطب  هنوز  عکس  ثبت  نکرده" if get_lang(uid)=="fa" else
                "\n\n📸  Partner  has  no  photo  yet"
            )
            await query.edit_message_text(text + no_photo_hint, reply_markup=chat_menu(uid))

    elif data=="profile":
        text = profile_text(uid)

        # ── د خپل عکس لیدل ──
        photo_id = u.get("photo_id")

        # که database کې نه وي، د Telegram نه واخله
        if not photo_id:
            try:
                photos = await context.bot.get_user_profile_photos(uid, limit=1)
                if photos and photos.photos:
                    photo_id = photos.photos[0][-1].file_id
                    users[uid]["photo_id"] = photo_id
            except: pass

        online = sum(1 for x in users.values() if x.get("state") in ["waiting","chatting"])
        full_text = text + f"\n🟢 {online}"

        # د عکس اپلوډ کولو پیشنهاد
        l = get_lang(uid)
        photo_hint = (
            "\n\n📸  د  عکس  اضافه  کولو  لپاره  یو  عکس  راواستوه" if l=="ps" else
            "\n\n📸  برای  افزودن  عکس،  یک  تصویر  ارسال  کنید" if l=="fa" else
            "\n\n📸  Send  a  photo  to  add  profile  picture"
        )

        if photo_id:
            try:
                await context.bot.send_photo(
                    chat_id=uid, photo=photo_id,
                    caption=full_text, reply_markup=main_menu(uid))
                return
            except: pass

        await query.edit_message_text(
            full_text + photo_hint, reply_markup=main_menu(uid))
    elif data=="coins":
        coins_guide = (
            "\n\n━━━━━━━━━━━━━━\n"
            + (
                "💰  د  سکو  اخیستلو  لارښود:\n\n"
                "🎁  ورځنۍ  جایزه:  +5\n"
                "👥  بلنه:  +10  هر  کس\n"
                "⭐  امتیاز  ورکول:  +2\n\n"
                "💳  د  پیسو  سره:\n"
                "100 💰 = 1$\n500 💰 = 4$\n1000 💰 = 7$\n\n"
                "📞  ادمین:  @ShadowByte_0"
                if get_lang(uid)=="ps" else
                "💰  راهنمای  خرید  سکه:\n\n"
                "🎁  جایزه  روزانه:  +5\n"
                "👥  دعوت:  +10  هر  نفر\n"
                "⭐  امتیاز:  +2\n\n"
                "💳  خرید  با  پول:\n"
                "100 💰 = 1$\n500 💰 = 4$\n1000 💰 = 7$\n\n"
                "📞  ادمین:  @ShadowByte_0"
                if get_lang(uid)=="fa" else
                "💰  Coin  Guide:\n\n"
                "🎁  Daily:  +5\n"
                "👥  Invite:  +10\n"
                "⭐  Rating:  +2\n\n"
                "💳  Buy  coins:\n"
                "100 💰 = $1\n500 💰 = $4\n1000 💰 = $7\n\n"
                "📞  Admin:  @ShadowByte_0"
            )
        )
        await query.edit_message_text(
            f"{T(uid,'coins_lbl')}: {u.get('coins',0)}" + coins_guide,
            reply_markup=InlineKeyboardMarkup([
                [btn("⭐  Stars  💎","buy_stars_menu")],
                [btn(T(uid,"back"),"menu")]]))
    elif data=="buy_stars_menu":
        rows=[[btn(p["label"],f"buy_{k}")] for k,p in STARS_PACKAGES.items()]
        rows.append([btn(T(uid,"back"),"coins")])
        await query.edit_message_text("⭐:", reply_markup=InlineKeyboardMarkup(rows))
    elif data.startswith("buy_"):
        pkg_id=data[4:]
        if pkg_id not in STARS_PACKAGES: await query.answer("❌",show_alert=True); return
        pkg=STARS_PACKAGES[pkg_id]
        try:
            await context.bot.send_invoice(
                chat_id=uid,title=f"💰 {pkg['coins']}",description=f"{pkg['coins']} coins",
                payload=f"coins_{pkg['coins']}_{uid}",currency="XTR",
                prices=[LabeledPrice(pkg["label"],pkg["stars"])],
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅",pay=True)]]))
        except Exception as e: await query.answer(f"❌{str(e)[:50]}",show_alert=True)
    elif data=="daily_bonus":
        now=datetime.now(); last=u.get("last_daily",now-timedelta(days=2))
        if now-last>=timedelta(hours=24):
            u["coins"]+=5; u["last_daily"]=now
            await query.edit_message_text(f"🎁 +5 💰 → {u['coins']}", reply_markup=main_menu(uid))
        else:
            wait=timedelta(hours=24)-(now-last)
            h,m=wait.seconds//3600,(wait.seconds%3600)//60
            await query.edit_message_text(f"⏰ {h}h {m}m", reply_markup=main_menu(uid))
    elif data=="my_link":
        bot=await context.bot.get_me()
        link=f"https://t.me/{bot.username}?start={u.get('anon_link')}"
        await query.edit_message_text(f"📧\n\n`{link}`", reply_markup=main_menu(uid))
    elif data=="invite":
        bot=await context.bot.get_me()
        link=f"https://t.me/{bot.username}?start=ref_{uid}"
        await query.edit_message_text(f"👥\n\n`{link}`\n🎁 +10 💰", reply_markup=main_menu(uid))
    elif data=="feedback":
        await query.edit_message_text("📮  @ShadowByte_0", reply_markup=main_menu(uid))
    elif data=="support":
        l = get_lang(uid)
        if l=="ps":
            sp = "\n".join([
                "📞  پشتیبانی","","━━━━━━━━━━━━━━",
                "🔹  د  ستونزو  لپاره:","👤  @ShadowByte_0","",
                "🔹  د  سکو  اخیستل:","👤  @ShadowByte_0","",
                "🔹  د  بلاک  لرې  کولو:","👤  @ShadowByte_0","",
                "━━━━━━━━━━━━━━","⏰  ځواب:  24  ساعته"
            ])
            cb = "📩  ادمین  سره  اړیکه"
        elif l=="fa":
            sp = "\n".join([
                "📞  پشتیبانی","","━━━━━━━━━━━━━━",
                "🔹  برای  مشکلات:","👤  @ShadowByte_0","",
                "🔹  خرید  سکه:","👤  @ShadowByte_0","",
                "🔹  رفع  مسدودیت:","👤  @ShadowByte_0","",
                "━━━━━━━━━━━━━━","⏰  زمان  پاسخ:  24  ساعت"
            ])
            cb = "📩  تماس  با  ادمین"
        else:
            sp = "\n".join([
                "📞  Support","","━━━━━━━━━━━━━━",
                "🔹  For  issues:","👤  @ShadowByte_0","",
                "🔹  Buy  coins:","👤  @ShadowByte_0","",
                "🔹  Unban  request:","👤  @ShadowByte_0","",
                "━━━━━━━━━━━━━━","⏰  Response  time:  24h"
            ])
            cb = "📩  Contact  Admin"
        await query.edit_message_text(
            sp,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(cb, url="https://t.me/ShadowByte_0")],
                [btn(T(uid,"back"),"menu")]
            ])
        )

    elif data=="help":
        l=get_lang(uid)
        if l=="ps":
            ht=(
                "😊  لارښـود  —  د  روبـاټ  کـارولـو  طـریـقـه\n\n"
                "🇦🇫✨━━━━━━━━━━━━━━━━━━✨🇦🇫\n\n"
                "📌  پـیـل  کـولـو  لـپـاره:\n"
                "━━━━━━━━━━━━━━\n"
                "۱.  /start  ولـیـکـه\n"
                "۲.  هـیـواد  وټـاکـه\n"
                "۳.  ژبـه  وټـاکـه\n"
                "۴.  جـنـسـیـت  وټـاکـه\n"
                "۵.  عـمـر  وټـاکـه\n"
                "۶.  ولایـت  وټـاکـه\n"
                "۷.  نـوم  ولـیـکـه\n"
                "✅  بشپړ!\n\n"
                "━━━━━━━━━━━━━━\n"
                "🔗  د  وصل  ډولونه:\n"
                "━━━━━━━━━━━━━━\n"
                "🎲  شانسي  —  وړیا\n"
                "👩  نجونې  —  5 💰\n"
                "👨  هلکان  —  5 💰\n"
                "⭐  ځانګړي  —  5 💰\n"
                "🚫  بې  چټ  —  5 💰\n"
                "❤️  خوښوونکي  —  5 💰\n"
                "📜  وروستي  —  وړیا\n\n"
                "━━━━━━━━━━━━━━\n"
                "💰  د  سکو  اخیستل:\n"
                "━━━━━━━━━━━━━━\n"
                "🎁  ورځنۍ:  +5\n"
                "👥  بلنه:  +10\n"
                "⭐  امتیاز:  +2\n\n"
                "━━━━━━━━━━━━━━\n"
                "🔒  قوانین:\n"
                "━━━━━━━━━━━━━━\n"
                "✔  کنځل  منع  دی\n"
                "✔  3  اخطار  =  بلاک\n\n"
                "🗣  ژبه  بدلول:  /lang\n"
                "📞  @ShadowByte_0"
            )
        elif l=="fa":
            ht=(
                "😊  راهنما\n\n"
                "🇮🇷✨━━━━━━━━━━━━━━━━━━✨🇮🇷\n\n"
                "📌  برای  شروع:\n"
                "━━━━━━━━━━━━━━\n"
                "۱.  /start  بزنید\n"
                "۲.  کشور  انتخاب\n"
                "۳.  زبان  انتخاب\n"
                "۴.  جنسیت  انتخاب\n"
                "۵.  سن  انتخاب\n"
                "۶.  استان  انتخاب\n"
                "۷.  نام  بنویسید\n"
                "✅  آماده!\n\n"
                "━━━━━━━━━━━━━━\n"
                "🔗  روش‌های  اتصال:\n"
                "━━━━━━━━━━━━━━\n"
                "🎲  تصادفی  —  رایگان\n"
                "👩  دختران  —  5 💰\n"
                "👨  پسران  —  5 💰\n"
                "⭐  مورد  علاقه  —  5 💰\n"
                "🚫  بدون  چت  —  5 💰\n"
                "❤️  لایک‌کرده  —  5 💰\n"
                "📜  تاریخچه  —  رایگان\n\n"
                "━━━━━━━━━━━━━━\n"
                "💰  کسب  سکه:\n"
                "━━━━━━━━━━━━━━\n"
                "🎁  روزانه:  +5\n"
                "👥  دعوت:  +10\n"
                "⭐  امتیاز:  +2\n\n"
                "━━━━━━━━━━━━━━\n"
                "🔒  قوانین:\n"
                "━━━━━━━━━━━━━━\n"
                "✔  فحاشی  ممنوع\n"
                "✔  3  هشدار  =  مسدود\n\n"
                "🗣  تغییر  زبان:  /lang\n"
                "📞  @ShadowByte_0"
            )
        else:
            ht=(
                "😊  Help\n\n"
                "🇺🇸✨━━━━━━━━━━━━━━━━━━✨🇺🇸\n\n"
                "📌  Getting  started:\n"
                "━━━━━━━━━━━━━━\n"
                "1.  Type  /start\n"
                "2.  Select  country\n"
                "3.  Select  language\n"
                "4.  Select  gender\n"
                "5.  Select  age\n"
                "6.  Select  region\n"
                "7.  Write  name\n"
                "✅  Ready!\n\n"
                "━━━━━━━━━━━━━━\n"
                "🔗  Connection  types:\n"
                "━━━━━━━━━━━━━━\n"
                "🎲  Random  —  Free\n"
                "👩  Girls  —  5 💰\n"
                "👨  Boys  —  5 💰\n"
                "⭐  Favorites  —  5 💰\n"
                "🚫  No-chat  —  5 💰\n"
                "❤️  Who  liked  —  5 💰\n"
                "📜  History  —  Free\n\n"
                "━━━━━━━━━━━━━━\n"
                "💰  Earn  coins:\n"
                "━━━━━━━━━━━━━━\n"
                "🎁  Daily:  +5\n"
                "👥  Invite:  +10\n"
                "⭐  Rating:  +2\n\n"
                "━━━━━━━━━━━━━━\n"
                "🔒  Rules:\n"
                "━━━━━━━━━━━━━━\n"
                "✔  No  bad  words\n"
                "✔  3  warnings  =  ban\n\n"
                "🗣  Change  language:  /lang\n"
                "📞  @ShadowByte_0"
            )
        await query.edit_message_text(ht, reply_markup=main_menu(uid))

# ================================================
# پیغام هندلر
# ================================================

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    u  =users.get(uid,{})

    # د عکس ثبتول — کله چې کاربر عکس لیږي
    if update.message.photo:
        if uid in users:
            photo_id = update.message.photo[-1].file_id
            users[uid]["photo_id"] = photo_id
            lang = get_lang(uid)
            ok_msg = (
                "✅  عکس  ثبت  شو!  اوس  ستا  پروفایل  کې  ښکاري." if lang=="ps" else
                "✅  عکس  ثبت  شد!  در  پروفایل  شما  نمایش  داده  می‌شود." if lang=="fa" else
                "✅  Photo  saved!  It  will  show  in  your  profile."
            )
            await update.message.reply_text(ok_msg)
        return

    text = update.message.text or ""
    if uid not in users:
        await update.message.reply_text("/start"); return

    step  = u.get("step","")
    state = u.get("state","")
    lang  = get_lang(uid)

    # د نوم ثبت
    if step == "name":
        raw  = text.strip()
        name = raw.rstrip("SAsa")
        if len(name)<2 or len(name)>20:
            await update.message.reply_text("❌ 2-20"); return
        u["name"]=name; u["is_student"]=raw.endswith(("S","s")); u["is_abroad"]=raw.endswith(("A","a"))
        u["step"]="done"
        await update.message.reply_text(
            f"{T(uid,'done')}\n📛 {name}  |  🎂 {u.get('age','?')}  |  📍 {u.get('province','?')}\n\n"
            + ("📸  عکس  هم  لیږلی  شې  (اختیاري):" if lang=="ps" else
               "📸  می‌توانید  عکس  هم  ارسال  کنید  (اختیاری):" if lang=="fa" else
               "📸  You  can  also  send  a  photo  (optional):"),
            reply_markup=main_menu(uid)); return

    # ادمین حالتونه
    if is_admin(uid):
        st=state
        if st=="adm_broadcast":
            ok=fail=0
            for tid in list(users.keys()):
                if tid==uid: continue
                try: await context.bot.send_message(tid,f"📢\n\n{text}"); ok+=1
                except: fail+=1
            u["state"]="idle"
            await update.message.reply_text(f"✅{ok}  ❌{fail}", reply_markup=admin_menu_kb()); return
        if st=="adm_give_coins":
            try:
                t2,am=int(text.split("/")[0].strip()),int(text.split("/")[1].strip())
                if t2 in users:
                    users[t2]["coins"]+=am
                    await update.message.reply_text(f"✅+{am}→{t2}", reply_markup=admin_menu_kb())
                    try: await context.bot.send_message(t2,f"🎁+{am} 💰")
                    except: pass
                else: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_rm_coins":
            try:
                t2,am=int(text.split("/")[0].strip()),int(text.split("/")[1].strip())
                if t2 in users:
                    users[t2]["coins"]=max(0,users[t2]["coins"]-am)
                    await update.message.reply_text(f"✅-{am}←{t2}", reply_markup=admin_menu_kb())
                    try: await context.bot.send_message(t2,f"💸-{am} 💰")
                    except: pass
                else: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_warn_input":
            try:
                t2=int(text.strip())
                if t2 in users:
                    users[t2]["warnings"]=users[t2].get("warnings",0)+1
                    w=users[t2]["warnings"]
                    await update.message.reply_text(f"⚠️{t2}—{w}", reply_markup=admin_menu_kb())
                    try: await context.bot.send_message(t2,f"⚠️ {T(t2,'warning')}\n{w}/3")
                    except: pass
                    if w>=3:
                        banned.add(t2)
                        if t2 in users: users[t2]["state"]="idle"
                        try: await context.bot.send_message(t2,"⛔")
                        except: pass
                else: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_msg_input":
            try:
                parts=text.split("|",1); t2=int(parts[0].strip()); msg=parts[1].strip()
                if t2 in users:
                    await context.bot.send_message(t2,f"📩\n\n{msg}")
                    await update.message.reply_text(f"✅→{t2}", reply_markup=admin_menu_kb())
                else: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌  آیدي|پیغام", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_add_adm":
            try:
                t2=int(text.strip()); name=users.get(t2,{}).get("name","?")
                EXTRA_ADMINS[t2]={"name":name,"perms":set()}
                await update.message.reply_text(f"👮+{t2}", reply_markup=admin_menu_kb())
                try: await context.bot.send_message(t2,"👮 ادمین شوئ!")
                except: pass
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_del_adm":
            try:
                t2=int(text.strip()); EXTRA_ADMINS.pop(t2,None)
                await update.message.reply_text(f"❌-{t2}", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_perms_input":
            try:
                t2=int(text.strip())
                if t2 in EXTRA_ADMINS:
                    await update.message.reply_text(f"🔐{t2}:", reply_markup=perms_kb(t2))
                else: await update.message.reply_text("❌  ادمین  نه  دی", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_ban_input":
            try:
                t2=int(text.strip()); banned.add(t2)
                if t2 in users: users[t2]["state"]="idle"
                await update.message.reply_text(f"🚫{t2}", reply_markup=admin_menu_kb())
                try: await context.bot.send_message(t2,"⛔")
                except: pass
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_unban_input":
            try:
                t2=int(text.strip()); banned.discard(t2)
                await update.message.reply_text(f"✅{t2}", reply_markup=admin_menu_kb())
                try: await context.bot.send_message(t2,"✅ /start")
                except: pass
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_find_uid":
            try:
                t2=int(text.strip())
                if t2 in users:
                    tu=users[t2]; g="👨" if tu.get("gender")=="male" else "👩"
                    bst="🚫" if t2 in banned else "✅"
                    await update.message.reply_text(
                        f"👤\n🆔`{t2}`\n{g}{tu.get('name','?')}\n"
                        f"🎂{tu.get('age','?')}|📍{tu.get('province','?')}\n"
                        f"💰{tu.get('coins',0)}|💬{tu.get('chats',0)}|⚠️{tu.get('warnings',0)}\n"
                        f"⭐{tu.get('avg_rating',5)}/5|{bst}",
                        reply_markup=InlineKeyboardMarkup([
                            [btn("🚫" if t2 not in banned else "✅",f"adm_ban_target_{t2}")],
                            [btn("🔙","adm_back")]]))
                else: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return
        if st=="adm_send_rating":
            try:
                parts=text.strip().split("/"); t2=int(parts[0].strip()); stars=int(parts[1].strip())
                if not 1<=stars<=5: raise ValueError
                if t2 in users:
                    users[t2].setdefault("ratings",[]).append({"from":uid,"stars":stars})
                    all_s=[r["stars"] for r in users[t2]["ratings"]]
                    users[t2]["avg_rating"]=round(sum(all_s)/len(all_s),1)
                    await update.message.reply_text(f"✅{'⭐'*stars}", reply_markup=admin_menu_kb())
                    try: await context.bot.send_message(t2,f"⭐{'⭐'*stars}")
                    except: pass
                else: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            except: await update.message.reply_text("❌", reply_markup=admin_menu_kb())
            u["state"]="idle"; return

    # عادي کاروونکي
    if state=="waiting_name":
        found=[p for p,pu in users.items()
               if text.lower() in pu.get("name","").lower() and pu.get("state")=="waiting" and p!=uid]
        if found:
            pid=found[0]
            users[uid].update({"state":"chatting","partner":pid,"chats":u.get("chats",0)+1})
            users[pid].update({"state":"chatting","partner":uid,"chats":users[pid].get("chats",0)+1})
            await context.bot.send_message(uid,T(uid,"connected"),reply_markup=chat_menu(uid))
            await context.bot.send_message(pid,T(pid,"connected"),reply_markup=chat_menu(pid))
        else: await update.message.reply_text("❌",reply_markup=main_menu(uid))
        u["state"]="idle"; return

    if state=="waiting_direct_msg":
        pid=u.get("partner")
        if pid and pid in users:
            if users[pid].get("coins",0)>=1:
                users[pid]["coins"]-=1
                await context.bot.send_message(pid,f"📩\n\n{text}\n\n-1💰")
                await update.message.reply_text("✅",reply_markup=chat_menu(uid))
            else: await update.message.reply_text("❌",reply_markup=chat_menu(uid))
        u["state"]="chatting"; return

    if state=="waiting_anon_msg":
        target=u.get("anon_target")
        if target and target in users:
            if u.get("coins",0)>=1:
                u["coins"]-=1
                await context.bot.send_message(target,f"📩\n\n{text}")
                await update.message.reply_text("✅")
            else: await update.message.reply_text("❌")
        u["state"]="idle"; return

    if state=="waiting_city_set":
        u["city"]=text.strip(); u["state"]="idle"
        await update.message.reply_text(f"✅{text.strip()}",reply_markup=main_menu(uid)); return

    if state!="chatting":
        await update.message.reply_text(T(uid,"menu"),reply_markup=main_menu(uid)); return

    if any(w in text.lower() for w in BAD_WORDS):
        await update.message.reply_text("⚠️"); return

    try: await context.bot.copy_message(users[uid]["partner"],uid,update.message.message_id)
    except: await stop_chat(uid,context,None)

# ================================================
# Stars تادیه
# ================================================

async def pre_checkout(update,context):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update,context):
    uid=update.effective_user.id
    payload=update.message.successful_payment.invoice_payload
    try:
        coins=int(payload.split("_")[1])
        if uid in users:
            users[uid]["coins"]+=coins
            await update.message.reply_text(
                f"✅+{coins}💰→{users[uid]['coins']}💰",reply_markup=main_menu(uid))
    except: pass

# ================================================
# MAIN
# ================================================

def main():
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("admin",admin_cmd))
    app.add_handler(CommandHandler("ban",ban_cmd))
    app.add_handler(CommandHandler("unban",unban_cmd))
    app.add_handler(CommandHandler("daily",daily_cmd))
    app.add_handler(CommandHandler("lang",lang_cmd))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT,successful_payment))
    app.add_handler(MessageHandler(filters.PHOTO,handle_msg))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND,handle_msg))
    print("✅  روباټ  چلیږي...")
    app.run_polling()

if __name__=="__main__":
    main()
