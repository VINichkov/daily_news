import logging


logger = logging.getLogger('daily_news')
logger.setLevel(logging.DEBUG)


fileHandler = logging.FileHandler('./share/example.log')
ch = logging.StreamHandler()


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fileHandler)
