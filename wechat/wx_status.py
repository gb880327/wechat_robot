# python3
from enum import Enum, unique


@unique
class Status(Enum):
    no_login = 0,
    qr = 1,
    logout = 2,
    success = 3,
    error = 4


class WxStatus:

    def __init__(self):
        self.status = Status.no_login
        self.userInfo = {}
        self.friends = []
        self.new_friends = []

    def update(self, status):
        self.status = status

    def get(self):
        return self.status
