#hii guys more changes

import logging

LEVEL_DEBUG    = logging.DEBUG
LEVEL_WARNING  = logging.WARNING
LEVEL_ERROR    = logging.ERROR
LEVEL_CRITICAL = logging.CRITICAL

LEVEL_DEFAULT  = LEVEL_DEBUG

OUTPUT_CONSOLE = 0
OUTPUT_FILE = 1

log_format = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(format = log_format)

logger = logging.getLogger('risk')
logger.setLevel(LEVEL_DEBUG)

def set_output(destination):
    if not hasattr(set_output, 'file_handler'):
       set_output.file_handler = logging.FileHandler('log.txt')

    if destination == OUTPUT_FILE:
        logger.addHandler(set_output.file_handler)
    elif set_output.file_handler in logger.handlers:
        logger.removeHandler(set_output.file_handler)

def set_verbosity_level(level):
    logger.setLevel(level)
		
def debug(msg):
    logger.debug(msg)
		
def warn(msg):
    logger.warn(msg)

def error(msg):
    logger.error(msg)

def critical(msg):
    logger.critical(msg)
	
if __name__ == '__main__':
    debug('test debug default')
    warn('test warn default')
    set_output(OUTPUT_CONSOLE)
    debug('test debug console')
    warn('test warn console')
    set_output(OUTPUT_FILE)
    debug('test debug file')
    warn('test warn file')
