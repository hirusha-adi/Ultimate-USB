class UltimateUSBError(Exception):
    "Base Exception for other exceptions"
    pass


class WifiPasswordError(UltimateUSBError):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return '{msg}'.format(msg=self.message)
        else:
            return 'Unable to run the Wifi-Password module'
