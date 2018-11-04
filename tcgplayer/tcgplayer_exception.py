class TCGplayerException(Exception):

    def __init__(self, exception):
        self.exception = exception

    def get_exception(self):
        return self.get_exception