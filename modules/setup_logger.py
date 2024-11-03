import logging
import logging.handlers
from typing import Union, Literal


def setup_logger():
    file_log = logging.handlers.RotatingFileHandler("logs/main.log", maxBytes=5000000, backupCount=10)
    console_out = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, handlers=(file_log, console_out),
                        format="%(asctime)s %(levelname)s %(message)s", force=True)
    logging.info('setup_logger')


def special_logger(name: str, level: Literal[50, 40, 30, 20, 10, 0] = logging.INFO, to_console: bool = False):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    file_handler = logging.handlers.RotatingFileHandler(f"logs/{name}.log", maxBytes=5000000, backupCount=10)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    if to_console:
        console_out = logging.StreamHandler()
        logger.addHandler(console_out)

    return logger