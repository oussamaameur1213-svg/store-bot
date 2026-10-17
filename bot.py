import os
import threading
from flask import Flask
import telebot

# 1. إعداد سيرفر Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot is running successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. إعداد بوت تلغرام
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت المتجر! 🛒\nكيف يمكنني مساعدتك اليوم؟")

def run_bot():
    bot.infinity_polling()

# 3. تشغيل البوت والسيرفر معاً في الخلفية
if __name__ == "__main__":
    # تشغيل استماع تلغرام في خيط منفصل
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # تشغيل سيرفر Flask في الخيط الرئيسي ليستجيب لـ Render
    run_flask()
