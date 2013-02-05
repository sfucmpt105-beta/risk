FORMAT="[%s: %s] >>> "

def risk_input(msg, stage="RISK"):
    return raw_input(FORMAT % (stage, msg))
