import requests
from bs4 import BeautifulSoup
from telegram import Bot
import schedule
import time
import os

def check_product_status(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    # 檢查是否存在class為'g-btn btn-cart'的按鈕
    button_element = soup.find('button', class_='g-btn btn-cart')
    if button_element:
        print('商品已開放訂購！')
        return True
    print('商品尚未開放訂購！')
    return False

def send_telegram_message(message, token, chat_id):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

# 獲取chat_id
def get_chat_id(token):
    response = requests.get(f'https://api.telegram.org/bot{token}/getUpdates')
    data = response.json()
    if 'result' in data and len(data['result']) > 0:
        return data['result'][0]['message']['chat']['id']
    else:
        raise Exception('No messages found. Please send a message to your bot and try again.')

PRODUCT_URL = os.environ.get('PRODUCT_URL', 'https://www.5music.com.tw/CDList-C.asp?cdno=445425679120')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '7110618214:AAGSwNTTPnC0VaJLgrGApc9Vw2KKfK89ESg')
CHAT_ID = get_chat_id(TELEGRAM_TOKEN)  # 獲取你的Chat ID

def job():
    if check_product_status(PRODUCT_URL):
        send_telegram_message("商品已開放訂購！", TELEGRAM_TOKEN, CHAT_ID)

schedule.every(1).minutes.do(job)  # 每10分鐘檢查一次

while True:
    schedule.run_pending()
    time.sleep(1)
