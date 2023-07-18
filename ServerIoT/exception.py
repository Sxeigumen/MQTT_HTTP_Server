"""Собственные исключения, для красоты сервера"""
class DefinitionTypeError(Exception):
    def __init__(self):
        self.type_error = "400(Bad Request)"


class LocalBdOverflow(Exception):
    def __init__(self):
        self.type_error = "501(Bd Overflow)"


class NotInitSmartphone(Exception):
    def __init__(self):
        self.type_error = "401(Not Init)"

class ConnectAlreadyHave(Exception):
    def __init__(self):
        self.type_error = '402(Already had pair)'

class NotDeviceInDb(Exception):
    def __init__(self):
        self.type_error = '404(Device not in db)'