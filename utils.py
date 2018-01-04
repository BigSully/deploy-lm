import logging, os

def get_logger(name):
    format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.get_logger(name)
    logger.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(format)
    logger.addHandler(consoleHandler)

    if not os.path.exists("logs"): os.makedirs("logs")
    fileHandler = logging.FileHandler("deploy.log")
    fileHandler.setFormatter(format)
    logger.addHandler(fileHandler)

    return logger

