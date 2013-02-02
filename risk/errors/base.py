class RiskGameError(RuntimeError):
    def __init__(self, msg):
        RuntimeError.__init__(self, msg)
