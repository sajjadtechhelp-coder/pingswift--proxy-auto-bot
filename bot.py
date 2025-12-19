import telebot
import requests
import schedule
import time
import threading

# Pre-configured Credentials
TOKEN = '8267236108:AAFihi1iqTXa_ngwqnjMipWiZOwi35DEMU0'
CHAT_ID = '@PingSwift_Proxy' 

bot = telebot.TeleBot(TOKEN)

def get_proxies():
    proxies = []
    try:
        # Fetching from API 1: MTProto
        r1 = requests.get('https://mtpro.xyz/api/?type=mtproto').json()
        if isinstance(r1, list):
            proxies.extend(r1)
        
        # Fetching from API 2: SOCKS
        r2 = requests.get('https://mtpro.xyz/api/?type=socks').json()
        if isinstance(r2, list):
            proxies.extend(r2)
    except Exception as e:
        print(f"API Error: {e}")
    
    # Return first 4 proxies
    return proxies[:4]

def send_update():
    data = get_proxies()
    if data:
        message = "🔄 **PingSwift Auto Proxy Update**\n\n"
        for i, p in enumerate(data, 1):
            link = p.get('link') or p.get('proxy_link')
            if link:
                message += f"{i}. 🔗 `{link}`\n\n"
        
        try:
            bot.send_message(CHAT_ID, message, parse_mode="Markdown")
            print("Update posted to channel.")
        except Exception as e:
            print(f"Post Error: {e}")

# Task: Run every 30 minutes
schedule.every(30).minutes.do(send_update)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "PingSwift Bot is fully active! 🚀\nAutomated updates are set for @PingSwift_Proxy.")

if __name__ == "__main__":
    # Send the first update immediately when the bot starts
    send_update()
    
    # Start timer thread
    threading.Thread(target=run_scheduler, daemon=True).start()
    print("Bot is running...")
    bot.infinity_polling()
