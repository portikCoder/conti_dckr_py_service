import logging


def init():

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(levelname)s:%(message)s',
    )
    logging.info('Logger setup is done')
