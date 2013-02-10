import risk.errors.input

FORMAT="[%s: %s] >>> "

def risk_input(msg, stage="RISK"):
    user_input = raw_input(FORMAT % (stage, msg))
    if user_input == 'quit':
        raise risk.errors.input.UserQuitInput()
    else:
        return user_input

