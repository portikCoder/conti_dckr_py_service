# handlers = [logging.StreamHandler()]
# {logging.getLogger('root').addHandler(handler) for handler in handlers}
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s',
)
logging.info('Logger setup is done')
