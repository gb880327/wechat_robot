# python3
import os
import threading
import time

import itchat
from itchat.content import *
from sanic.log import logger

from wechat.robot import robot
from .wx_status import WxStatus, Status


class WxThead(threading.Thread):

    def __init__(self, wx: WxStatus):
        threading.Thread.__init__(self)
        self.wx = wx
        self.qr_path = "./page/qrcode.png"
        self.waitForConfirm = False

    def run(self):
        self.login()
        itchat.run()

    def login(self):
        def exit_callback():
            if os.path.exists(self.qr_path):
                os.remove(self.qr_path)
            if os.path.exists("./itchat.pkl"):
                os.remove("./itchat.pkl")
            self.wx.update(Status.logout)
            logger.info("==========exit=============")
            raise Exception("logout")

        def qr_callback(uuid, status, qrcode):
            with open(self.qr_path, "wb") as f:
                f.write(qrcode)
                self.wx.update(Status.qr)
                logger.info("==========login============")

        def open_qr():
            for get_count in range(10):
                logger.info('Getting uuid')
                uuid = itchat.get_QRuuid()
                while uuid is None:
                    uuid = itchat.get_QRuuid()
                    time.sleep(1)
                logger.info('Getting QR Code')
                if itchat.get_QR(uuid, qrCallback=qr_callback):
                    break
                elif get_count >= 9:
                    self.wx.update(Status.error)
                    logger.info('Failed to get QR Code, please restart the program')
            logger.info('Please scan the QR Code')
            return uuid

        uuid = open_qr()
        while 1:
            status = itchat.check_login(uuid)
            print("========" + status + "========")
            if status == '200':
                self.wx.update(Status.success)
                break
            elif status == '201':
                if self.waitForConfirm:
                    logger.info('Please press confirm')
                    self.waitForConfirm = True
            elif status == '408':
                logger.info('Reloading QR Code')
                uuid = open_qr()
                self.waitForConfirm = False
        self.wx.userInfo = itchat.web_init()
        itchat.show_mobile_login()
        itchat.get_friends(True)
        itchat.start_receiving(exit_callback)

        @itchat.msg_register(TEXT, isFriendChat=True)
        def text_reply(msg):
            rep = robot(msg.Content) + "[智能管家]"
            itchat.send_msg(rep, msg.FromUserName)

        @itchat.msg_register(FRIENDS)
        def friend_reply(msg):
            itchat.add_friend(**msg['Text'])
            self.wx.new_friends.append(msg)
