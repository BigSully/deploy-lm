import argparse
import json
import logging, os

def get_logger(name):
    format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(format)
    logger.addHandler(console_handler)

    #if not os.path.exists("logs"): os.makedirs("logs")
    file_handler = logging.FileHandler("deploy.log")
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)

    return logger

def get_option():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-p', '--localPackage', help='path for the jaz file')
    args = vars(parser.parse_args())
    return args


def get_config():
    configs = json.load(open('config.json'))
    opt_dict=get_option()
    configs = {**configs, **opt_dict}  ## merge two dict

    return configs
