import logging

OUTPUT_CONSOLE = 0
OUTPUT_FILE = 1

log_format = '%(asctime)s - %(message)s'
logging.basicConfig(format = log_format)

logger = logging.getLogger('risk')
file_handler = logging.FileHandler('log.txt')

def set_output(destination):
    if destination == OUTPUT_FILE:
        logger.addHandler(file_handler)
    else:
        logger.removeHandler(file_handler)

def set_verbosity_level(level):
    logger.setLevel(level)
		
def debug(msg):
    logging.debug('%s' %msg)
		
def warn(msg):
    logging.warn('%s' %msg)

def error(msg):
    logging.error('%s' %msg)

def critical(msg):
    logging.critical('%s' %msg)
	
if __name__ == '__main__':
    debug('test')
    warn('test')
    set_output(1)
    debug('test')
    warn('test')
    set_output(0)
    debug('test')
    warn('test')