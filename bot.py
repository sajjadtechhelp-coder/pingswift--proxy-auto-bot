import telebot
import requests
import schedule
import time
import threading

# Aapka Bot Token
TOKEN = '8267236108:AAFihi1iqTXa_ngwqnjMipWiZOwi35DEMU0'
# YAAD SE: Niche @YourChannelUsername ki jagah apna channel username likhein
# Misal ke taur par: CHAT_ID = '@PingSwift_Proxies'
CHAT_ID = '@YourChannelUsername' 

bot = telebot.TeleBot(TOKEN)

def get_proxies():
    proxies = []
    try:
        # Dono APIs se data lena
        r1 = requests.get('https://mtpro.xyz/api/?type=mtproto').json()
        proxies.extend(r1)
        r2 = requests.get('https://mtpro.xyz/api/?type=socks').json()
        proxies.extend(r2)
    except:
        pass
    return proxies[:4] # Sirf pehli 4 proxies

def send_update():
    data = get_proxies()
    if data:
        msg = "🔄 **PingSwift Auto Update (30 Mins)**\n\n"
        for i, p in enumerate(data, 1):
            link = p.get('link') or p.get('proxy_link')
            msg += f"{i}. 🔗 `{link}`\n\n"
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

# Timer set karna (Har 30 minute baad)
schedule.every(30).minutes.do(send_update)

def run_timer():
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "PingSwift Bot Online! Proxies har 30 min baad aapke channel mein khud jayengi.")

if __name__ == "__main__":
    threading.Thread(target=run_timer, daemon=True).start()
    print("Bot is starting...")
    bot.infinity_polling()
