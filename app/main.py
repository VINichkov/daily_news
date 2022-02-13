import config
import schedule
import time
from services import SendToTelegram, GetNewFeedsFromSites


def get_feeds():
    GetNewFeedsFromSites().call()


def send():
    SendToTelegram().call()


schedule.every(10).minutes.do(get_feeds)
schedule.every(30).seconds.do(send)

while True:
    schedule.run_pending()
    time.sleep(10)
