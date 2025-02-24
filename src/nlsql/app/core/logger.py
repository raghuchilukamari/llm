import logging

def get_logger(__name__):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    return logger