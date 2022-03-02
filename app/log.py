import logging
import os

logger = logging.getLogger('daily_news')
if os.getenv('LOG_LEVEL') == 'debug':
    logger.setLevel(logging.DEBUG)
else:     logger.setLevel(logging.INFO)


fileHandler = logging.FileHandler('./share/example.log')
ch = logging.StreamHandler()


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fileHandler)
