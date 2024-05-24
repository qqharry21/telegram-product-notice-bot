import requests
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
import schedule
import time
from flask import Flask, request
import os

app = Flask(__name__)

def check_product_status(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    # 檢查是否存在class為'g-btn btn-cart'的按鈕
    button_element = soup.find('button', class_='g-btn btn-cart')
    if button_element:
        print('FOUND')
        return True
    return False

def send_telegram_message(message, token, chat_id):
    bot = Bot(token=token)
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))

# 獲取chat_id
def get_chat_id(token):
    response = requests.get(f'https://api.telegram.org/bot{token}/getUpdates')
    data = response.json()
    if 'result' in data and len(data['result']) > 0:
        return data['result'][0]['message']['chat']['id']
    else:
        raise Exception('No messages found. Please send a message to your bot and try again.')

PRODUCT_URL = 'https://www.5music.com.tw/CDList-C.asp?cdno=445425679120'
TELEGRAM_TOKEN = '7110618214:AAGSwNTTPnC0VaJLgrGApc9Vw2KKfK89ESg'  # 替換為你的Telegram Bot權杖
CHAT_ID = get_chat_id(TELEGRAM_TOKEN)  # 獲取你的Chat ID

def job():
    if check_product_status(PRODUCT_URL):
        send_telegram_message("商品已開放訂購！", TELEGRAM_TOKEN, CHAT_ID)

# Flask route to trigger the job manually
@app.route('/check', methods=['GET'])
def check():
    job()
    return "Check completed."

schedule.every(1).minutes.do(job)  # 每1分鐘檢查一次

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    import threading
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
