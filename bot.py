import os
import threading
from flask import Flask
import telebot
from telebot import types

# --------------------------------------------------
# 1. إعداد سيرفر Flask للحفاظ على عمل البوت 24/7 على Render
# --------------------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "🚀 Crypto Store Bot is 100% Active!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --------------------------------------------------
# 2. إعداد بوت تلغرام وبيانات الكريبتو الخاصة بك
# --------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = os.environ.get("ADMIN_ID", "")

# 💳 بيانات الاستقبال الخاصة بك
BINANCE_PAY_ID = "763055980"
USDT_TRC20_WALLET = "TFt1x5ooY7LM3ehdx5iJoiFSPGGVismyX4"

user_orders = {}

# --------------------------------------------------
# 3. كتالوج الشحن للألعاب والتطبيقات (بالعملات الرقمية USDT)
# --------------------------------------------------
CATALOG = {
    "pubg": {
        "name": "🔥 بوبجي موبايل (PUBG UC)",
        "items": {
            "pubg_60": {"title": "60 UC", "price": 1.1},
            "pubg_325": {"title": "325 UC", "price": 5.2},
            "pubg_660": {"title": "660 UC", "price": 10.0},
            "pubg_1800": {"title": "1800 UC", "price": 25.0}
        }
    },
    "freefire": {
        "name": "💎 فري فاير (Free Fire)",
        "items": {
            "ff_110": {"title": "110 جوهرة 💎", "price": 1.2},
            "ff_580": {"title": "580 جوهرة 💎", "price": 5.5},
            "ff_1080": {"title": "1080 جوهرة 💎", "price": 10.5},
            "ff_weekly": {"title": "اشتراك أسبوعي 📅", "price": 2.4}
        }
    },
    "ludo": {
        "name": "🎲 يلا لودو & Ludo King",
        "items": {
            "ludo_d500": {"title": "500 مجوهرات Yalla Ludo", "price": 2.8},
            "ludo_d1000": {"title": "1000 مجوهرات Yalla Ludo", "price": 5.5},
            "ludo_king": {"title": "كوينز Ludo King", "price": 3.0}
        }
    },
    "tiktok": {
        "name": "🪙 عملات تيك توك (TikTok Coins)",
        "items": {
            "tt_350": {"title": "350 عملة 🪙", "price": 5.0},
            "tt_700": {"title": "700 عملة 🪙", "price": 9.8},
            "tt_1400": {"title": "1400 عملة 🪙", "price": 19.5}
        }
    },
    "apps": {
        "name": "📲 Bigo Live & Netflix & Roblox",
        "items": {
            "bigo_d": {"title": "ماسات Bigo Live", "price": 6.0},
            "roblox_r": {"title": "800 Robux (Roblox)", "price": 11.0},
            "netflix_m": {"title": "اشتراك Netflix (شهر)", "price": 12.0}
        }
    }
}

# --------------------------------------------------
# 4. الأزرار والقوائم الرئيسية
# --------------------------------------------------
def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_catalog = types.KeyboardButton("🎮 جميع الألعاب والتطبيقات")
    btn_wallet = types.KeyboardButton("🪙 عنوان الدفع (Binance Pay / USDT)")
    btn_support = types.KeyboardButton("📞 الدعم والاتصال")
    markup.add(btn_catalog)
    markup.add(btn_wallet, btn_support)
    return markup

# --------------------------------------------------
# 5. معالجة الرسائل
# --------------------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"أهلاً بك يا {message.from_user.first_name} في متجر الشحن الرقمي الفوري ⚡\n\n"
        "💳 **طريقة الدفع المعتمدة:** USDT / Binance Pay فقط.\n"
        "اختر القسم المطلوب للشحن مباشرة من الأزرار:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "🎮 جميع الألعاب والتطبيقات")
def show_all_services(message):
    markup = types.InlineKeyboardMarkup()
    for cat_id, data in CATALOG.items():
        markup.add(types.InlineKeyboardButton(text=data["name"], callback_data=f"cat_{cat_id}"))
    bot.send_message(message.chat.id, "اختر اللعبة أو التطبيق المطلوب للشحن:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "🪙 عنوان الدفع (Binance Pay / USDT)")
def show_crypto_wallet(message):
    wallet_info = (
        "🪙 **تفاصيل الاستقبال المباشر بالعملات الرقمية:**\n\n"
        f"🔸 **Binance Pay ID:** `{BINANCE_PAY_ID}`\n"
        f"🔹 **USDT Wallet (TRC20):** `{USDT_TRC20_WALLET}`\n\n"
        "⚡ يتم تأكيد الشحنات فور التأكد من وصول التحويل."
    )
    bot.send_message(message.chat.id, wallet_info, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: msg.text == "📞 الدعم والاتصال")
def show_support_info(message):
    bot.send_message(message.chat.id, "لأي استفسار أو مساعدة خاصة حول الشحن، تواصل مباشرة مع الإدارة.")

# --------------------------------------------------
# 6. معالجة اختيارات الشحن والـ ID
# --------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def show_items(call):
    cat_id = call.data.split("_")[1]
    cat_data = CATALOG.get(cat_id)
    
    if cat_data:
        markup = types.InlineKeyboardMarkup()
        for item_id, item in cat_data["items"].items():
            btn_text = f"{item['title']} | 💵 {item['price']} USDT"
            markup.add(types.InlineKeyboardButton(text=btn_text, callback_data=f"item_{cat_id}_{item_id}"))
        
        bot.edit_message_text(f"اختر الباقة لـ {cat_data['name']}:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("item_"))
def process_item(call):
    _, cat_id, item_id = call.data.split("_", 2)
    item_data = CATALOG[cat_id]["items"][item_id]
    
    user_orders[call.message.chat.id] = {
        "title": item_data["title"],
        "price": item_data["price"]
    }
    
    msg = bot.send_message(
        call.message.chat.id, 
        f"🎯 **الباقة:** {item_data['title']}\n"
        f"💰 **السعر:** {item_data['price']} USDT\n\n"
        "يرجى كتابة **معرّف الحساب / Player ID** الخاص بك للشحن الآن:"
    )
    bot.register_next_step_handler(msg, get_player_id)

def get_player_id(message):
    chat_id = message.chat.id
    if chat_id in user_orders:
        user_orders[chat_id]["player_id"] = message.text
        
        pay_msg = (
            "💳 **معلومات إتمام الدفع:**\n\n"
            f"💵 **المبلغ:** `{user_orders[chat_id]['price']} USDT`\n"
            f"🔸 **Binance Pay ID:** `{BINANCE_PAY_ID}`\n"
            f"🔹 **عنوان TRC20:** `{USDT_TRC20_WALLET}`\n\n"
            "بعد إتمام التحويل، أرسل **رقم المعاملة (TxID / Order ID)** أو صورة إيصال التحويل هنا فوراً لتأكيد طلبك:"
        )
        msg = bot.send_message(chat_id, pay_msg, parse_mode="Markdown")
        bot.register_next_step_handler(msg, finalize_crypto_order)

def finalize_crypto_order(message):
    chat_id = message.chat.id
    if chat_id in user_orders:
        order = user_orders[chat_id]
        tx_info = message.text
        
        summary = (
            "✅ **تم تسليم بيانات الطلب والدفع بنجاح!**\n\n"
            f"📦 الباقة: {order['title']}\n"
            f"🎯 Player ID: `{order['player_id']}`\n"
            f"💰 المبلغ المطلوب: {order['price']} USDT\n"
            f"🧾 الإثبات: `{tx_info}`\n\n"
            "⚡ جاري التحقق وتمرير الشحنة لحسابك فوراً."
        )
        bot.send_message(chat_id, summary, parse_mode="Markdown")
        
        # إشعار فوري لك على تلغرام
        if ADMIN_ID:
            admin_alert = (
                "🚨 **طلب شحن جديد بالكريبتو!**\n"
                f"👤 الزبون: @{message.from_user.username or message.from_user.first_name}\n"
                f"📦 الخدمة: {order['title']}\n"
                f"🎯 Player ID: `{order['player_id']}`\n"
                f"💰 المبلغ: {order['price']} USDT\n"
                f"🧾 إثبات الدفع: `{tx_info}`"
            )
            try:
                bot.send_message(ADMIN_ID, admin_alert, parse_mode="Markdown")
            except Exception as e:
                print(f"Admin Notify Error: {e}")
                
        del user_orders[chat_id]

# --------------------------------------------------
# 7. تشغيل الخيوط (Threading)
# --------------------------------------------------
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    run_flask()
