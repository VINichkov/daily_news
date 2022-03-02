import config
import schedule
import time
from services import SendToTelegram, GetNewFeedsFromSites, Clear
from log import logger
import traceback


def get_feeds():
    try:
        logger.info('Start: service GetNewFeedsFromSites')
        GetNewFeedsFromSites().call()
    except Exception:
        logger.error('Ошибка:\n', traceback.format_exc())


def send():
    try:
        logger.info('Start: service SendToTelegram')
        SendToTelegram().call()
    except Exception:
        logger.error('Ошибка:\n', traceback.format_exc())

def clear():
    try:
        logger.info('Start: service Clear')
        Clear().call()
    except Exception:
        logger.error('Ошибка:\n', traceback.format_exc())


schedule.every(10).minutes.do(get_feeds)
schedule.every(30).seconds.do(send)
schedule.every(1).days.do(clear)

while True:
    schedule.run_pending()
    time.sleep(10)
