# kcauto  Copyright (C) 2017  Minyoung Choi

from time import strftime
import platform
import subprocess

class Logger(object):
    def __init__(self, debug=False):
        if platform.system().lower() == 'windows':
            subprocess.call('', shell=True)
        self.debugging = debug
    
    def enable_debugging(self):
        self.debugging = True

    def disable_debugging(self):
        self.debugging = False

    @staticmethod
    def format_time():
        return Color.turquoise + "[{}] ".format(strftime("%Y-%m-%d %H:%M:%S"))

    def message(self, _msg):
        print("{}{}{}".format(self.format_time(), Color.blue + _msg , Color.END))

    def success(self, _msg):
        print("{}{}{}".format(self.format_time(), Color.green + _msg , Color.END))

    def warning(self, _msg):
        print("{}{}{}".format(self.format_time(), Color.yellow + _msg , Color.END))

    def error(self, _msg):
        print("{}{}{}".format(self.format_time(), Color.red + _msg , Color.END))

    def info(self, _msg):
        print("{}{}{}".format(self.format_time(), Color.turquoise + _msg , Color.END))

    def debug(self, _msg):
        if self.debugging:
            print("{}{}{}".format(self.format_time(), Color.grey + _msg , Color.END))

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