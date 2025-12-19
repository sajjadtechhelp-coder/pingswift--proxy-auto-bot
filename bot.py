import telebot
import requests
import schedule
import time
import threading
import os
from flask import Flask

# Flask server to keep the bot alive on Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Bot Credentials
TOKEN = '8267236108:AAFihi1iqTXa_ngwqnjMipWiZOwi35DEMU0'
CHAT_ID = '@PingSwift_Proxy' 

bot = telebot.TeleBot(TOKEN)

def get_proxies():
    proxies = []
    try:
        r1 = requests.get('https://mtpro.xyz/api/?type=mtproto').json()
        if isinstance(r1, list): proxies.extend(r1)
        r2 = requests.get('https://mtpro.xyz/api/?type=socks').json()
        if isinstance(r2, list): proxies.extend(r2)
    except:
        pass
    return proxies[:4]

def send_update():
    data = get_proxies()
    if data:
        message = "🔄 **PingSwift Auto Proxy Update**\n\n"
        for i, p in enumerate(data, 1):
            link = p.get('link') or p.get('proxy_link')
            if link: message += f"{i}. 🔗 `{link}`\n\n"
        try:
            bot.send_message(CHAT_ID, message, parse_mode="Markdown")
        except:
            pass

schedule.every(30).minutes.do(send_update)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Start Web Server for Render
    threading.Thread(target=run_web_server).start()
    # Send first update immediately
    send_update()
    # Start Scheduler
    threading.Thread(target=run_scheduler, daemon=True).start()
    print("Bot started...")
    bot.infinity_polling()
