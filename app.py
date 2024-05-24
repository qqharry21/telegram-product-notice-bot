import requests
from bs4 import BeautifulSoup
from telegram import Bot
import schedule
import time
import os
import logging

# 設置日誌記錄
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_product_status(url):
    logger.info('Checking product status...')
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    # 檢查是否存在class為'g-btn btn-cart'的按鈕
    button_element = soup.find('button', class_='g-btn btn-cart')
    if button_element:
        logger.info('Product is available for purchase.')
        return True
    logger.info('Product is not available for purchase.')
    return False

def send_telegram_message(message, token, chat_id):
    logger.info('Sending Telegram message...')
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

# 獲取chat_id
def get_chat_id(token):
    logger.info('Getting chat ID...')
    response = requests.get(f'https://api.telegram.org/bot{token}/getUpdates')
    data = response.json()
    if 'result' in data and len(data['result']) > 0:
        return data['result'][0]['message']['chat']['id']
    else:
        raise Exception('No messages found. Please send a message to your bot and try again.')

PRODUCT_URL = os.environ.get('PRODUCT_URL', 'https://www.5music.com.tw/CDList-C.asp?cdno=445425679120')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '7110618214:AAGSwNTTPnC0VaJLgrGApc9Vw2KKfK89ESg')
CHAT_ID = get_chat_id(TELEGRAM_TOKEN)

def job():
    if check_product_status(PRODUCT_URL):
        send_telegram_message("商品已開放訂購！", TELEGRAM_TOKEN, CHAT_ID)

# 設置定時任務，每20秒檢查一次
schedule.every(20).seconds.do(job)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_scheduler()
