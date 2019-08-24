# encoding: utf-8
from __future__ import print_function
import sys

RED = "\033[1;31m"
YLW = "\033[1;33m"
CLR = "\033[0m"


class Printer:

    def __init__(self):
        pass

    def message(self, msg):
        print(msg)

    def error(self, msg):
        print(RED, 'ERR: ', msg, CLR, sep='', file=sys.stderr)

    def warn(self, msg):
        print(YLW, 'WRN: ', msg, CLR, sep='', file=sys.stderr)
