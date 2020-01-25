# kcauto  Copyright (C) 2017  Minyoung Choi

from time import strftime
import platform
import subprocess
from tools.multiconsole import Sender
import random
from subprocess import Popen, CREATE_NEW_CONSOLE

class Logger(object):
    def __init__(self, debug=False):
        self.debugging = debug
        self.console_port = random.randint(9000, 24500)
        self.receiver = None
        self.open_receiver()
        self.sender = Sender(self.console_port)
    
    def enable_debugging(self):
        self.debugging = True

    def disable_debugging(self):
        self.debugging = False

    def open_receiver(self):
        self.receiver = Popen(['python', './tools/multiconsole.py', '-p', str(self.console_port)], creationflags=CREATE_NEW_CONSOLE)

    @staticmethod
    def format_time():
        return Color.turquoise + "[{}] ".format(strftime("%Y-%m-%d %H:%M:%S"))

    def message(self, _msg):
        self.sender.send("{}{}{}".format(self.format_time(), Color.blue + _msg , Color.END))

    def success(self, _msg):
        self.sender.send("{}{}{}".format(self.format_time(), Color.green + _msg , Color.END))

    def warning(self, _msg):
        self.sender.send("{}{}{}".format(self.format_time(), Color.yellow + _msg , Color.END))

    def error(self, _msg):
        self.sender.send("{}{}{}".format(self.format_time(), Color.red + _msg , Color.END))

    def info(self, _msg):
        self.sender.send("{}{}{}".format(self.format_time(), Color.turquoise + _msg , Color.END))

    def debug(self, _msg):
        if self.debugging:
            self.sender.send("{}{}{}".format(self.format_time(), Color.grey + _msg , Color.END))

class Color(object):
    red = '\033[0m\033[91m'
    green = '\033[0m\033[92m'
    yellow = '\033[0m\033[93m'
    blue = '\033[0m\033[94m'
    purple = '\033[0m\033[95m'
    black = '\033[0m\033[30m'
    grey = '\033[0m\033[37m'
    turquoise = '\033[0m\033[96m'
    UNDERLINE = '\033[4m'
    HIGHLIGHT = '\033[7m'
    END = '\033[0m'