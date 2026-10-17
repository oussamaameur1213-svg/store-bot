import os
import threading
from flask import Flask
import telebot

# 1. إعداد سيرفر Flask للحفاظ على عمل البوت في Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# 2. تشغيل السيرفر الخفيف
keep_alive()

# 3. جلب التوكن وتشغيل البوت
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت المتجر! 🛒\nكيف يمكنني مساعدتك اليوم؟")

# 4. بدء استقبال الرسائل من تلغرام
bot.infinity_polling()
