###############################################################################
## logging utilities
#
_LEVEL_DEBUG=3
_LEVEL_WARN=2
_LEVEL_ERR=1
_LEVEL_NORMAL=_LEVEL_ERR

LOG_LEVEL = _LEVEL_NORMAL

def debug(msg):
    if LOG_LEVEL >= _LEVEL_DEBUG:
        print "[DEBUG] %s" % msg

def warn(msg):
    if LOG_LEVEL >= _LEVEL_WARN:
        print "[WARN] %s" % msg

def error(msg):
    if LOG_LEVEL >= _LEVEL_ERR:
        print "[ERROR] %s" % msg

def critical(msg):
    print "[CRITICAL] %s" % msg
